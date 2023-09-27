from typing import List

import pandas as pd

from .commit import CommitFetcher


def msg_aggregation(messages: List[str]):
    return [f'{i + 1}. {msg}' for i, msg in enumerate(messages)]


class GiteeCommits:
    def __init__(self):
        self.__commits = []

    def append(self, commits):
        self.__commits += commits

    def save(self):
        df = self.__create_data_frame()
        df.to_excel("./output.xlsx", sheet_name='Sheet1', index=False)

    def __create_data_frame(self):
        df = pd.DataFrame(self.__commits)
        df['message'] = df['message'].apply(lambda x: x.replace('\n', ''))
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        grouped_df = df.groupby(['uid', 'author', 'date'])['message'].agg(
            lambda x: '\n'.join(msg_aggregation(x)))
        grouped_df = grouped_df.reset_index()
        sorted_df = grouped_df.sort_values(by='date', ascending=False)
        result_df = sorted_df.rename(columns={'author': '作者', 'date': '日期', 'message': '提交信息'})
        return result_df


gc = GiteeCommits()
for c in CommitFetcher("ascend", "modelzoo", params={
    "author": "王姜奔"
}):
    gc.append(c)
gc.save()
