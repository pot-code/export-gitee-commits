from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
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


class CommitsDataFrame:
    def __init__(self, commits: list[Commit]):
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

    def export_to_excel(self, output):
        self.__df.to_excel(output, sheet_name="Sheet1", index=False)
