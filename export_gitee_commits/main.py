import argparse
import logging
from pathlib import Path

import structlog

from .commits import CommitWorkbook, CommitsDataFrame, CommitFetcher, CommitFilterManager, CommitMessageFilter

log = structlog.get_logger()

parser = argparse.ArgumentParser(prog="export-gitee-commits", description='导出 gitee 提交历史')
parser.add_argument('owner', metavar='OWNER', type=str, help='仓库所属用户')
parser.add_argument('repo', metavar="REPO", type=str, help='仓库名称')
parser.add_argument('-o', '--output', type=str, required=True, help='导出 Excel 文件路径')
parser.add_argument('-t', '--token', type=str, help='gitee 第三方授权 token')
parser.add_argument('-a', '--author', type=str, help='限定提交用户')
parser.add_argument('-b', '--branch', type=str, help='仓库分支名')
parser.add_argument('-s', '--since', type=str, help='开始日期（ISO 8601）')
parser.add_argument('-u', '--until', type=str, help='结束日期（ISO 8601）')
parser.add_argument('-v', '--verbose', action='store_true', help='诊断输出')


def main():
    args = parser.parse_args()
    if not args.verbose:
        structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))

    commits = []
    fm = CommitFilterManager([CommitMessageFilter()])
    for c in CommitFetcher(args.owner, args.repo, params={
        "access_token": args.token,
        "author": args.author,
        "since": args.since,
        "until": args.until,
        "sha": args.branch
    }):
        commits += filter(fm.apply, c)

    df = CommitsDataFrame(commits)
    df.format_message()
    df.format_date()
    df.group()
    df.sort_by_date()
    df.remap_columns()

    wb = CommitWorkbook(df.dataframe)
    wb.format_cells()
    wb.save(Path(args.output))
    log.info('save commits to %s', args.output)
