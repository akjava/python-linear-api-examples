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
Attachmentは添付ではありません。Issueの下部に表示されるリンク(Links)です。
https://developers.linear.app/docs/graphql/attachments
"""

import time
import json

"""
load_api_key - .env中のapi_keyを読み込みます。エラーになる場合、.envファイルを作成して、Linearの設定で作成したAPI_KEYを書き込んでください
execute_query - 実際にlinear APIのエンドポイントに送信し、結果を表示します。
"""
from linear_api_utils import load_api_key, execute_query


if __name__ == "__main__":
    api_key = load_api_key()

    # 最新のIssue IDを取得する
    issues_text = """
query {
  issues(first: 1) {
    nodes {
      title
      id
    }
  }
}
"""

    result = execute_query("最新のIssueを取り出す", issues_text, api_key)
    issue_id = result["data"]["issues"]["nodes"][0]["id"]
    url = "https://huggingface.co/Akjava"
    # attachment/リンクを作成する
    # exception.com?はよくわからないので、自分の管理しているサイトに変更(githubだとiconUrlの挙動がおかしいので他を使用)
    """
    iconUrlは指定ではなく、domainから取られる
    """
    attachment_create_text = """
mutation{
  attachmentCreate(input:{
    issueId: "%s"
    title: "Huggingface"
    subtitle: "link"
    iconUrl: "https://akjava.github.io/AIDiagramChatWithVoice-FaceCharacter/jpg/128x128/00003245.jpg"
    url: "%s"
    metadata: {exceptionId: "exc-123"}
  }){
    success
    attachment{
      id
    }
  }
}

""" % (issue_id, url)
    result = execute_query("attachment_create_text", attachment_create_text, api_key)

    attachment_id = result["data"]["attachmentCreate"]["attachment"]["id"]
    attachment_update_text = """
mutation{
  attachmentUpdate(id: "%s", input: {
    title: "My Huggingface Page"
    subtitle: "link page"
    metadata: {exceptionId: "exc-123"}
    }){
    success
    attachment{
      id
      metadata
    }
  }
}
""" % (attachment_id)
    attachment_with_id = """
query {
  attachment(id: "%s") {
    id
    issue {
      id
      identifier
      title
    }
  }
}
""" % (attachment_id)
    result = execute_query("Query for attachments with id", attachment_with_id, api_key)

    attachment_with_url = """
query {
  attachmentsForURL(url: "%s") {
    nodes {
      id
      issue {
        id
        identifier
        title
      }
    }
  }
}
""" % (url)

    result = execute_query(
        "Query for attachments with url", attachment_with_url, api_key
    )
