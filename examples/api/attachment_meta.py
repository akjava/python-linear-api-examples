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
Attachmentは添付ファイルではありません。Issueの下部に表示されるリンク(Links)のことです。
https://developers.linear.app/docs/graphql/attachments

AttachementのMetaは基本 API内部だけで処理するものです。
ですが、Metadataに関するQueryやMutationおよびFilterは現在調べてますがないようです。Resultから主導で処理することになる。

ただ画面の表示に影響のある２つの特別なメタ機能があります。

１つめはRich metadataです。
https://developers.linear.app/docs/graphql/attachments#rich-metadata
これを指定すると、通常のクリックして他のサイトが開くだけのリンクが、クリックするとメッセージをダイアログで展開するリンクに変わります。（外部リンクのアイコンを押して展開せずにリンク先を開くことも可能です。）

２つめはFormattingで、日付をmetaに埋め込んで、それを基準にした現時刻との比較をattachment(リンク)のsubtitleに表示できます。
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

    url = "https://github.com/akjava"
    """
    メッセージ付きのAttachmentを作成
    注意事項 messages[{}] - 配列です。
    """
    attachment_create_text_with_messages = """
mutation{
  attachmentCreate(input:{
    issueId: "%s"
    title: "My Github"
    subtitle: "click to expand"
    url: "%s"
    metadata: {
    title:"Popular repositories"
    messages:[
    {
    subject:"no idead,how to work"
    body:"godot-simple-gemini-api - 10 stars"
    timestamp:"2024-11-04"
    }
    {
    subject:"no idead,how to work"
    body:"Matcha-TTS-Japanese - 3 stars"
    timestamp:"2024-10-01"
    }
    ]
    }
  }){
    success
    attachment{
      id
    }
  }
}

""" % (issue_id, url)
    result = execute_query(
        "attachment_create_text_with_messages",
        attachment_create_text_with_messages,
        api_key,
    )

    url2 = "https://qiita.com/akjava"
    attachment_create_text_with_format = """
mutation{
  attachmentCreate(input:{
    issueId: "%s"
    title: "My Qita"
    subtitle: "lastmodified {cdate__since} mdate:{mdate__relativeTimestamp} cdate:{cdate__relativeTimestamp}"
    url: "%s"
    metadata: {
    cdate:"2025-01-29T12:22:32.090+09:00"
    mdate:"2025-01-10T12:22:32.090+09:00"
    }
  }){
    success
    attachment{
      id
    }
  }
}

""" % (issue_id, url2)
    result = execute_query(
        "attachment_create_text_with_format",
        attachment_create_text_with_format,
        api_key,
    )
