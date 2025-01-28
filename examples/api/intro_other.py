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
import re

"""
このスクリプトでは、以下の章に含まれるQueryを実行します。
https://developers.linear.app/docs/graphql/working-with-the-graphql-api#creating-and-editing-issues

お使いのLinearの状態によって返ってくる値は異なります。値が空なことも有りえます。

このスクリプトで実行していること

すべてのユーザーのIDと名前を取得/表示する
最初のユーザーに割り当てられているIssuのIDとタイトルを取得/表示する

すべてのステート(Backlog,Todo,..)のIDと名前を取得/表示する
最初のステートに割り当てられているIssuのIDとタイトルを取得/表示する
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

    users_text = """
query {
  users {
    nodes {
      name
      id
    }
  }
}
"""

    result = execute_query("users_text", users_text)
    first_user_id = result["data"]["users"]["nodes"][0]["id"]

    assigned_text = """
query {
  user(id: "%s") {
    id
    name
    assignedIssues {
      nodes {
        id
        title
      }
    }
  }
}
""" % (first_user_id)

    result = execute_query("assigned", assigned_text)

    states_text = """
query {
  workflowStates {
    nodes {
      id
      name
    }
  }
}
"""
    result = execute_query("states", states_text)
    first_state_id = result["data"]["workflowStates"]["nodes"][0]["id"]

    state_issues_text = """
query {
  workflowState(id: "%s") {
    issues {
      nodes {
        title
      }
    }
  }
}
""" % (first_state_id)
    result = execute_query("state_issues", state_issues_text)
