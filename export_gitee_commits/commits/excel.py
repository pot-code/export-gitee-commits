from os import PathLike
from typing import Iterable

import pandas as pd
import structlog
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

from .commit import Commit

log = structlog.get_logger()


class CommitWorkbook:
    def __init__(self, df: DataFrame):
        wb = Workbook()
        ws = wb.active
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
        self.__workbook = wb

    def format_cells(self):
        ws = self.__workbook.active
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 100

        for row in ws.iter_rows(max_col=4):
            row[0].alignment = Alignment(vertical='top')
            row[1].alignment = Alignment(vertical='top')
            row[2].alignment = Alignment(vertical='top')
            row[3].alignment = Alignment(vertical='top', wrap_text=True)

    def save(self, path: PathLike):
        self.__workbook.save(path)


class CommitsDataFrame:
    def __init__(self, commits: Iterable[Commit]):
        self.__df = pd.DataFrame(commits)

    def format_date(self):
        self.__df['date'] = self.__df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    def format_message(self):
        self.__df['message'] = self.__df['message'].apply(lambda x: x.replace('\n', ''))

    def group(self):
        def number_messages(messages: list[str]):
            return [f'{i + 1}. {msg}' for i, msg in enumerate(messages)]

        grouped_df = self.__df.groupby(['uid', 'author', 'date'])['message'].agg(
            lambda x: '\n'.join(number_messages(x)))
        self.__df = grouped_df.reset_index()

    def sort_by_date(self, ascending: bool = False):
        self.__df = self.__df.sort_values(by='date', ascending=ascending)

    def remap_columns(self):
        self.__df = self.__df.rename(columns={'author': '作者', 'date': '日期', 'message': '提交信息'})

    @property
    def dataframe(self):
        return self.__df
