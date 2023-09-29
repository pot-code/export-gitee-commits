from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

import structlog

log = structlog.get_logger()


class CommitResponseObject:
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

    @property
    def uid(self):
        return self.__get_author().get('id')

    @property
    def author_name(self):
        return self.__get_author().get('name')

    @property
    def commit_message(self):
        return self.__get_commit().get('message')

    @property
    def commit_date(self):
        return self.__get_commit()['author']['date']


@dataclass
class Commit:
    uid: int | str
    author: str
    date: datetime
    message: str

    @staticmethod
    def from_raw_data(data):
        h = CommitResponseObject(data)
        c = Commit(
            uid=h.uid, author=h.author_name,
            date=datetime.fromisoformat(h.commit_date),
            message=h.commit_message
        )
        log.debug('transformed commit', commit=c)
        return c
