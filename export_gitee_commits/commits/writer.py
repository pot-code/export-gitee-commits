from os import PathLike

import structlog

from .commit import Commit, CommitsDataFrame

log = structlog.get_logger()


class ExcelWriter:
    def __init__(self):
        self.__commits: list[Commit] = []

    def append(self, commits):
        self.__commits += commits

    def save(self, output_path: PathLike):
        df = CommitsDataFrame(self.__commits)
        df.format_date()
        df.format_message()
        df.group()
        df.sort_by_date()
        df.remap_columns()
        df.export_to_excel(output_path)
        log.info("save commits to %s", output_path, total=len(self.__commits))
