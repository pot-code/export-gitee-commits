from os import PathLike
from typing import List

import pandas as pd

from .iter import Commit


class CommitsDataFrame:
    def __init__(self, commits: List[Commit]):
        self.__df = pd.DataFrame(commits)

    def format_date(self):
        self.__df['date'] = self.__df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    def format_message(self):
        self.__df['message'] = self.__df['message'].apply(lambda x: x.replace('\n', ''))

    def group_by_date(self):
        def number_messages(messages: List[str]):
            return [f'{i + 1}. {msg}' for i, msg in enumerate(messages)]

        grouped_df = self.__df.groupby(['uid', 'author', 'date'])['message'].agg(
            lambda x: '\n'.join(number_messages(x)))
        self.__df = grouped_df.reset_index()

    def sort_by_date(self, ascending: bool = False):
        self.__df = self.__df.sort_values(by='date', ascending=ascending)

    def remap_columns(self):
        self.__df = self.__df.rename(columns={'author': '作者', 'date': '日期', 'message': '提交信息'})

    def export_to_excel(self, output):
        self.__df.to_excel(output, sheet_name="Sheet1", index=False)


class CommitsExcelWriter:
    def __init__(self):
        self.__commits: list[Commit] = []

    def append(self, commits):
        self.__commits += commits

    def save(self, output_path: PathLike):
        df = CommitsDataFrame(self.__commits)
        df.format_date()
        df.format_message()
        df.group_by_date()
        df.sort_by_date()
        df.remap_columns()
        df.export_to_excel(output_path)
