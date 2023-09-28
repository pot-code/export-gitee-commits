import argparse
from pathlib import Path

from .commits import fetcher, writer

parser = argparse.ArgumentParser(prog="export-gitee-commits", description='导出 gitee 提交历史')
parser.add_argument('owner', metavar='OWNER', type=str, help='仓库所属用户')
parser.add_argument('repo', metavar="REPO", type=str, help='仓库名称')
parser.add_argument('-o', '--output', type=str, required=True, help='导出 Excel 文件路径')
parser.add_argument('-t', '--token', type=str, help='gitee 第三方授权 token')
parser.add_argument('-a', '--author', type=str, help='限定提交用户')

if __name__ == '__main__':
    args = parser.parse_args()
    cw = writer.CommitsExcelWriter()
    for c in fetcher.CommitFetcher(args.owner, args.repo, params={
        "access_token": args.token,
        "author": args.author
    }):
        cw.append(c)
    cw.save(Path(args.output))
