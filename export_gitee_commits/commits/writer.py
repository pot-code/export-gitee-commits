from os import PathLike

import structlog
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

from .commit import Commit, CommitsDataFrame

log = structlog.get_logger()


class CommitWorkbook:
    def __init__(self):
        self.__workbook = Workbook()

    def add_data(self, df: DataFrame):
        ws = self.__workbook.active

        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

    def format_cells(self):
        ws = self.__workbook.active
        ws.column_dimensions['A'].alignment = Alignment(vertical='top', wrap_text=False)
        ws.column_dimensions['B'].alignment = Alignment(vertical='top', wrap_text=False)
        ws.column_dimensions['C'].alignment = Alignment(vertical='top', wrap_text=False)
        ws.column_dimensions['D'].alignment = Alignment(vertical='top', wrap_text=True)

    def save(self, path: PathLike):
        self.__workbook.save(path)


class ExcelWriter:
    def __init__(self):
        self.__commits: list[Commit] = []

    def append(self, commits):
        self.__commits += commits

    def save(self, output_path: PathLike):
        if len(self.__commits) == 0:
            log.warning("no commits to write")
            return

        df = CommitsDataFrame(self.__commits)
        df.format_date()
        df.format_message()
        df.group()
        df.sort_by_date()
        df.remap_columns()

        wb = CommitWorkbook()
        wb.add_data(df.dataframe)
        wb.format_cells()
        wb.save(output_path)
        log.info("save commits to %s", output_path, total=len(self.__commits))
