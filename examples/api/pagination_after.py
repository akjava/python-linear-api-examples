# This code is licensed under the MIT License.
# Copyright (c) [2025-01-28] [Akihito Miyazaki]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Note that the GraphQL query texts included in this file are for illustrative purposes
# and are quoted from the Linear API documentation. They are not covered by the MIT License.
# See: https://developers.linear.app/docs/graphql/working-with-the-graphql-api


import codecs
import json
import os


from linear_api_utils import load_api_key, execute_query

"""
このスクリプトでは、以下のページに含まれるQueryを実行します。
https://developers.linear.app/docs/graphql/working-with-the-graphql-api/pagination

　お使いのLinearの状態によって返ってくる値は異なります。値が空なことも有りえます。
Issueの数が多かったり、頻繁に呼び出すと、Rate-Limitの関係でエラーになることがあります。

　このスクリプトで実行していること
すべてのIssueをページで取り出しています。最後にIssue数と、Issueタイトルを表示します。


"""

if __name__ == "__main__":
    api_key = load_api_key()

    after = None
    active_issues = []

    page = 1
    while True:
        after_text = ""
        if after:
            # after must be double-quote
            after_text = f',after: "{after}"'
        """
            query-issues:デフォルトの値
            includeArchived :false - アーカイブ（削除）されたissueは含みません。
            orderBy :createdAt - 表示される順番は作成順です。(更新順ではない)

        """
        paging_query_text = (
            "{ issues(first: 10%s) { edges { node { id title } cursor} pageInfo {hasNextPage endCursor}}}"
            % (after_text)
        )

        # print(data)

        result = execute_query(f"ページ {page}", paging_query_text, api_key)
        page += 1
        # print(result)
        for node in result["data"]["issues"]["edges"]:
            active_issues.append(node["node"]["title"])

        if not result["data"]["issues"]["pageInfo"]["hasNextPage"]:
            break
        else:
            after = result["data"]["issues"]["pageInfo"]["endCursor"]

    print(f"total issues {len(active_issues)}")
    for title in active_issues:
        print(title)
