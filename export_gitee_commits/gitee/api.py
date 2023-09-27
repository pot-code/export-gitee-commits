import requests

BASE_URL = "https://gitee.com/api/v5"


def get_commits(owner, repo, params=None):
    """
    获取 gitee 的提交历史
    :param owner: 仓库所有人/组织的用户名
    :param repo: 仓库名
    :param params: 其他参数，详见 https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepoCommits
    :return: 提交数据数组
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
    return requests.get(url, params=params)
