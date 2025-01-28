# This code is licensed under the MIT License.
# Copyright (c) [2025] [Akihito Miyazaki]
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


"""
このスクリプトでは、以下の章にで説明されているArchivedされたIssueを表示します。
https://developers.linear.app/docs/graphql/working-with-the-graphql-api#archived-resources

お使いのLinearの状態によって返ってくる値は異なります。ArchivedされたIssue(削除されたIssueは３０日間、復元可能なArchived状態になります。)がなければ空になります。

includeArchived: true を指定し、あとはfilterを使います。
"""

"""
load_api_key - .env中のapi_keyを読み込みます。エラーになる場合、.envファイルを作成して、Linearの設定で作成したAPI_KEYを書き込んでください
request_linear - 実際にlinear APIのエンドポイントに送信します。
"""
from linear_api_utils import load_api_key, request_linear


if __name__ == "__main__":
    headers = {
        "Content-Type": "application/json",
        "Authorization": load_api_key(),
    }

    def execute_query(label, query_text):
        print(f"label:{label}")

        query_dic = {"query": query_text}
        print(f"send query:{query_dic['query']}")
        result = request_linear(headers, query_dic)
        print(result)
        print("")  # spacer

        return result

    issues_text = """
query {
  issues(includeArchived: true,filter:{
    archivedAt:{
      null:false
      }
  }) {
    nodes {
      title
      archivedAt
    }
  }
}
"""

    result = execute_query("users_text", issues_text)
