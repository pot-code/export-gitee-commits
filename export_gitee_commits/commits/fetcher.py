import structlog

from .api import get_commits
from .commit import Commit

log = structlog.get_logger()


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
        data = res.json()
        log.info('fetched commit', page=self.__page - 1, total_page=self.__total_page, size=len(data))
        return [Commit.from_raw_data(e) for e in data]
