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
https://developers.linear.app/docs/graphql/working-with-the-graphql-api#creating-and-editing-issues

お使いのLinearの状態によって返ってくる値は異なり、issueが存在しない場合動作がおかしいことがあります。（未検証)

注意事項：このスクリプトは新しくissueを作成します。

このスクリプトではNew exceptionというIssueを作成後に、'New Issue Title'に名前が変わります。
statusは、Backlogあるいは、triage機能がoffの場合、別なの(おそらくCancel)に変わります。
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

    state_text = """
query WorkflowStates{
workflowStates{
   nodes {
      id
      name
      team{
        name
        id
      }
    }
}
}
"""

    def result_to_state_dic_by_team(result):
        team_dic = {}
        for node in result["data"]["workflowStates"]["nodes"]:
            team_id = node["team"]["id"]
            if team_id in team_dic:
                team_dic[team_id][node["id"]] = node["name"]
            else:
                team_dic[team_id] = {node["id"]: node["name"]}
        return team_dic

    result = execute_query("WorkflowStates", state_text)
    state_dic_by_team = result_to_state_dic_by_team(result)
    print("# State Dic by Team")
    print(state_dic_by_team)

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

    issue_create_text = """
    mutation IssueCreate {
  issueCreate(
    input: {
      title: "New exception"
      description: "More detailed error report in markdown"
      teamId: "%s"
    }
  ) {
    success
    issue {
      id
      title
    }
  }
}""" % (first_team_id)
    result = execute_query("IssueCreate", issue_create_text)
    issue_id = result["data"]["issueCreate"]["issue"]["id"]

    # 0 is maybe backlog,if not enabled triage
    state_id = list(state_dic_by_team[first_team_id].keys())[
        1
    ]  # if states length smaller than 1,it woule error happen(default never happen)
    issue_update_text = """
mutation IssueUpdate {
  issueUpdate(
    id: "%s",
    input: {
      title: "New Issue Title"
      stateId: "%s",
    }
  ) {
    success
    issue {
      id
      title
      state {
        id
        name
      }
    }
  }
}
""" % (issue_id, state_id)
    result = execute_query("IssueUpdate", issue_update_text)
