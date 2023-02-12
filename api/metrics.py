from enum import Enum


class WapiMetrics(Enum):
    SEND_MESSAGE_COUNT = "send_message_count"
    SEND_MESSAGE_LENGTH = "send_message_length"

    BAN_USER_COUNT = "ban_user_count"

    SEND_STICKER_COUNT = "send_sticker_count"

    EVENT_COUNT = "event_count"

    ERRORS_COUNT = "errors_count"
