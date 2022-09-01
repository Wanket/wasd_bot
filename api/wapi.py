import asyncio
from asyncio import CancelledError, Future
from concurrent import futures
from datetime import datetime
from threading import Thread
from typing import Optional

import inject
import socketio
from aiohttp import ClientSession
from dateutil.parser import isoparse

from api.iwapi import IWapi
from api.utils import hash_message
from model.bot import Bot
from model.user_message import UserMessage
from util.ilogger import ILogger


class Wapi(IWapi):
    def __init__(self):
        self._logger = inject.instance(ILogger)
        self._bot = inject.instance(Bot)

        self._event_loop = asyncio.new_event_loop()
        self._start_event_loop_thread()

        asyncio.run_coroutine_threadsafe(self._load_stream_data_loop(), self._event_loop)

        self._http_client = ClientSession(loop=self._event_loop)

        self._socket = asyncio.run_coroutine_threadsafe(self._setup_socket(), self._event_loop).result()
        self._socket_task: Optional[Future[None]] = None

        self._token: Optional[str] = None
        self._channel_name: Optional[str] = None

        self._jwt: Optional[str] = None

        self._channel_id: Optional[int] = None
        self._stream_id: Optional[int] = None
        self._streamer_id: Optional[int] = None

        self._game_name: Optional[str] = None
        self._stream_started_date: Optional[datetime] = None

    def send_message(self, text: str):
        async def test():
            await self._socket.emit("message", {
                "channelId": self._channel_id,
                "hash": hash_message(),
                "jwt": self._jwt,
                "message": text,
                "streamId": self._stream_id,
                "streamerId": self._streamer_id,
            })

        asyncio.run_coroutine_threadsafe(
            test(), self._event_loop
        )

    def ban_user(self, user_id: int):
        asyncio.run_coroutine_threadsafe(self._ban_user_impl(user_id), self._event_loop)

    def get_stream_time(self) -> int:
        return int((datetime.utcnow() - self._stream_started_date.replace(tzinfo=None)).total_seconds())

    def get_game_name(self) -> str:
        return self._game_name

    def start_listen(self, token: str, channel_name: str):
        self._token = token
        self._channel_name = channel_name

        self._socket_task = asyncio.run_coroutine_threadsafe(self._start_listen_impl(), self._event_loop)

    def stop_listen(self):
        try:
            self._event_loop.call_soon_threadsafe(self._socket_task.cancel)

            self._socket_task.result()
        except (CancelledError, futures.CancelledError):
            self._logger.info(f"{self.__class__.__name__}: stop listen")
        except Exception as e:
            self._logger.exception(f"{self.__class__.__name__}: got error while stopping listen: {e}")
        finally:
            if self._socket.connected:
                asyncio.run_coroutine_threadsafe(self._socket.disconnect(), self._event_loop).result()

    def _start_event_loop_thread(self):
        def start_event_loop():
            asyncio.set_event_loop(self._event_loop)

            self._event_loop.run_forever()

        Thread(target=start_event_loop).start()

    async def _start_listen_impl(self):
        while True:
            self._logger.info(f"{self.__class__.__name__}: loading stream data")

            while not await self._load_stream_data(load_jwt=True):
                await asyncio.sleep(1)

            self._logger.info(f"{self.__class__.__name__}: stream data loaded")

            try:
                self._logger.info(f"{self.__class__.__name__}: connecting to chat")

                await self._socket_loop()
            except (CancelledError, futures.CancelledError):
                raise
            except Exception as e:
                self._logger.exception(f"{self.__class__.__name__}: got error in socket loop, error: {e}, reconnecting in 1 second")

                await asyncio.sleep(1)
            finally:
                if self._socket.connected:
                    await self._socket.disconnect()

    async def _ban_user_impl(self, user_id: int):
        async with self._http_client.put(
                f"https://wasd.tv/api/channels/{self._channel_id}/banned-users",
                headers={"Authorization": f"Token {self._token}"},
                json={
                    "user_id": user_id,
                    "stream_id": self._stream_id,
                    "keep_messages": True,
                    "duration": 1
                }) as response:
            if response.status != 200 and response.status != 403:
                self._logger.error(f"{self.__class__.__name__}: failed to ban user, status: {response.status}")

    async def _load_stream_data_loop(self):
        while True:
            if self._socket.connected and not await self._load_stream_data(load_jwt=False):
                self._logger.info(f"{self.__class__.__name__}: cannot update stream data, retrying in 1 minute")

            await asyncio.sleep(60)

    async def _load_stream_data(self, load_jwt: bool) -> bool:
        try:
            if load_jwt:
                async with self._http_client.post(f"https://wasd.tv/api/auth/chat-token",
                                                  headers={"Authorization": f"Token {self._token}"}) as response:
                    if response.status // 100 != 2:
                        self._logger.error(
                            f"{self.__class__.__name__}: failed to get chat token,"
                            f" status: {response.status}, data: {await response.text()}, retrying in 1 second"
                        )

                        return False

                    self._jwt = (await response.json())["result"]

            async with self._http_client.get(f"https://wasd.tv/api/v2/broadcasts/public?channel_name={self._channel_name}") as response:
                if response.status != 200:
                    self._logger.error(
                        f"{self.__class__.__name__}: failed to load stream data,"
                        f" status: {response.status}, data: {await response.text()}, retrying in 1 second"
                    )

                    return False

                channel_info = await response.json()

            if not channel_info["result"]["channel"]["channel_is_live"]:
                self._logger.info(f"{self.__class__.__name__}: channel {self._channel_name} is not live, rechecking in 1 second")

                return False

            channel_id = channel_info["result"]["channel"]["channel_id"]
            stream_id = channel_info["result"]["media_container"]["media_container_streams"][0]["stream_id"]
            streamer_id = channel_info["result"]["channel"]["user_id"]
            game_name = channel_info["result"]["media_container"]["game"]["game_name"]
            stream_started_date = isoparse(channel_info["result"]["media_container"]["published_at"])

            self._channel_id = channel_id
            self._stream_id = stream_id
            self._streamer_id = streamer_id
            self._game_name = game_name
            self._stream_started_date = stream_started_date

            return True
        except (CancelledError, futures.CancelledError):
            raise
        except Exception as e:
            self._logger.exception(f"{self.__class__.__name__}: got error while loading stream data, error: {e}, retrying in 1 second")

            return False

    async def _socket_loop(self):
        await self._socket.connect("wss://chat.wasd.tv")

        await self._socket.wait()

    async def _setup_socket(self):
        socket = socketio.AsyncClient()

        @socket.event
        async def connect():
            self._logger.info(f"{self.__class__.__name__}: connected to chat")

            await self._socket.emit("join", {
                "channelId": self._channel_id,
                "streamId": self._stream_id,
                "jwt": self._jwt,
                "excludeStickers": True,
            })

        @socket.event
        async def disconnect():
            self._logger.info(f"{self.__class__.__name__}: disconnected from chat")

        @socket.event
        async def connect_error(data):
            self._logger.error(f"{self.__class__.__name__}: connect error, data: {data}")

        @socket.event
        async def joined(data):
            self._logger.info(f"{self.__class__.__name__}: joined to chat, data: {data}")

        @socket.event
        async def message(data):
            self._bot.on_message(UserMessage(user_id=int(data["user_id"]), user_name=data["user_login"], text=data["message"]))

        @socket.event
        async def highlighted_message(data):
            self._bot.on_message(UserMessage(user_id=int(data["user_id"]), user_name=data["user_login"], text=data["message"]))

        return socket
