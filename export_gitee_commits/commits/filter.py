import structlog

from .commit import Commit

log = structlog.get_logger()


class CommitFilter:
    def filter(self, commit: Commit):
        return True


class CommitMessageFilter(CommitFilter):
    def filter(self, commit: Commit):
        r = not commit.message.startswith('Merge')
        log.debug("apply filter", filter_name=self.__class__.__name__, message=commit.message, result=r)
        return r


class CommitFilterManager:
    def __init__(self, filters: list[CommitFilter]):
        self.__filters = filters

    def apply(self, commit: Commit):
        return all(f.filter(commit) for f in self.__filters)
