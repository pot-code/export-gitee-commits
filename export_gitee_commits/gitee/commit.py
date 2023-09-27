from dataclasses import dataclass
from datetime import datetime

from .api import get_commits


@dataclass
class Commit:
    uid: int
    author: str
    date: datetime
    message: str


class CommitFetcher:
    def __init__(self, owner, repo, params=None):
        self.__total_page = 1
        self.__page = 1
        self.__owner = owner
        self.__repo = repo
        self.__params = params

    def __iter__(self):
        return self

    def __next__(self):
        if self.__page > self.__total_page:
            raise StopIteration

        res = get_commits(self.__owner, self.__repo, params={
            "page": self.__page,
            **self.__params,
        })
        headers = res.headers
        self.__total_page = int(headers.get("total_page"), 10)
        self.__page += 1
        return [Commit(
            uid=e["author"]['id'],
            author=e["author"]['name'],
            date=datetime.fromisoformat(e['commit']['author']['date']),
            message=e["commit"]['message'],
        ) for e in res.json()]
