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
    def __init__(self, owner, repo, **params):
        self.total_page = 1
        self.page = 1
        self.owner = owner
        self.repo = repo
        self.params = params

    def __iter__(self):
        return self

    def __next__(self):
        if self.page > self.total_page:
            raise StopIteration

        res = get_commits(self.owner, self.repo, params={
            "page": self.page,
            **self.params,
        })
        headers = res.headers
        self.total_page = int(headers.get("total_page"), 10)
        self.page += 1
        return [Commit(
            uid=e["author"]['id'],
            author=e["author"]['name'],
            date=datetime.fromisoformat(e['commit']['author']['date']),
            message=e["commit"]['message'],
        ) for e in res.json()]
