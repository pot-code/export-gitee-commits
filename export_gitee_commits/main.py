import argparse
import logging
from pathlib import Path

import structlog

from .commits import fetcher, writer

parser = argparse.ArgumentParser(prog="export-gitee-commits", description='导出 gitee 提交历史')
parser.add_argument('owner', metavar='OWNER', type=str, help='仓库所属用户')
parser.add_argument('repo', metavar="REPO", type=str, help='仓库名称')
parser.add_argument('-o', '--output', type=str, required=True, help='导出 Excel 文件路径')
parser.add_argument('-t', '--token', type=str, help='gitee 第三方授权 token')
parser.add_argument('-a', '--author', type=str, help='限定提交用户')
parser.add_argument('-v', '--verbose', action='store_true', help='诊断输出')


def main():
    args = parser.parse_args()
    if not args.verbose:
        structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))

    cw = writer.CommitsExcelWriter()
    for c in fetcher.CommitFetcher(args.owner, args.repo, params={
        "access_token": args.token,
        "author": args.author
    }):
        cw.append(c)
    cw.save(Path(args.output))
