from datetime import datetime

from model.util.idatetime import IDateTime


class DateTime(IDateTime):
    def now(self) -> datetime:
        return datetime.now()

    def utcnow(self) -> datetime:
        return datetime.utcnow()
