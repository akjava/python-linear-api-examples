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


import codecs
import json
import os
import re

"""
このスクリプトでは、以下の章に含まれるQueryを実行します。
https://developers.linear.app/docs/graphql/working-with-the-graphql-api#queries-and-mutations

お使いのLinearの状態によって返ってくる値は異なり、issueが存在しない場合動作がおかしいことがあります。（未検証)
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
        print(f"send query {query_text}")
        query_dic = {"query": query_text}
        result = request_linear(headers, query_dic)
        print(result)
        print("")  # spacer

        return result

    me_text = """
    query Me {
  viewer {
    id
    name
    email
  }
}
    """
    execute_query("Me", me_text)

    teams_text = """
query Teams {
  teams {
    nodes {
      id
      name
    }
  }
}
"""
    result = execute_query("Teams", teams_text)
    first_team_id = result["data"]["teams"]["nodes"][0]["id"]
    # 時間がかかるので、デフォルトの50件から5件に issuesのクエリを修正しています。
    team_text = """
query Team {
  team(id: "%s") {
    id
    name

    issues(first:5) {
      nodes {
        id
        title
        description
        assignee {
          id
          name
        }
        createdAt
        archivedAt
      }
    }
  }
}
""" % (first_team_id)
    result = execute_query("Team", team_text)
    first_issue_id = result["data"]["team"]["issues"]["nodes"][0]["id"]

    issue_text = """
query Issue {
  issue(id: "%s") {
    id
    title
    description
  }
}
""" % (first_issue_id)
    execute_query("Issue", issue_text)
