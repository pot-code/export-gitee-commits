from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

import structlog

log = structlog.get_logger()


class CommitResponseHelper:
    def __init__(self, data):
        self.__data = data

    def __get_author(self):
        a = self.__data.get('author')
        if a is not None:
            return defaultdict(str, a)
        c = self.__get_commit()
        return c['author']

    def __get_commit(self):
        return self.__data.get('commit')

    def get_uid(self):
        return self.__get_author().get('id')

    def get_author_name(self):
        return self.__get_author().get('name')

    def get_commit_message(self):
        return self.__get_commit().get('message')

    def get_commit_date(self):
        return self.__get_commit()['author']['date']


@dataclass
class Commit:
    uid: int | str
    author: str
    date: datetime
    message: str

    @staticmethod
    def from_raw_data(data):
        log.debug('transform response data to Commit', data=data)
        h = CommitResponseHelper(data)
        return Commit(
            uid=h.get_uid(),
            author=h.get_author_name(),
            date=datetime.fromisoformat(h.get_commit_date()),
            message=h.get_commit_message()
        )
