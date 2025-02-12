"""
このコードは以下のコードをLinear.appに対応させたものです。公式のコードではありません。
https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/_webhooks_server.py
https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/_webhooks_payload.py

まだ、Issue Objectのごく一部しか対応してません。
https://studio.apollographql.com/public/Linear-API/variant/current/schema/reference/objects/Issue

.envファイルに、api_key = linear-api-key および、webhook_secret = linear-webhook-secretの設定が必要です。

ローカルは起動ごとにURLが変わるので、起動時にLinear-APIでURLを更新しています。
target_webhook_label(デフォルト値はGradio)で指定したラベルのwebhookを実行時に上書きます。

gradio,fastapi,pydanticをあらかじめインストールしておく必要があります。
.envにlinear api_keyおよび、linear-webhook secretを記述する必要があります。
また、このExampleはUpdateのみなので、最初にラベルGradioでWebhookを作っておいてください。

** Linear.app 対応部分の著作権表示 **
# Copyright 2025-present, Akihito Miyazaki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

** Hugging Face Hub ライブラリのライセンス表示 **
# Copyright 2023-present, the HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

このコードには Hugging Face Hub ライブラリの一部が含まれており、Apache License, Version 2.0 の下でライセンスされています。
ライセンスの全文は以下から確認できます: http://www.apache.org/licenses/LICENSE-2.0
"""

import gradio as gr
from fastapi import Request
from gradio_webhook_server import WebhooksServer
from gradio_webhook_payload import WebhookPayload
import os
import sys
from pprint import pprint

# 現在のディレクトリから親ディレクトリへのパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "../api")
sys.path.append(parent_dir)

from linear_api_utils import load_api_key, execute_query

api_key = load_api_key("../api/")
"""
{'errors': [{'message': 'Unknown argument "filter" on field "Query.webhooks". Did you mean "after"?', 'locations': [{'line': 3, 'column': 12}], 'extensions': {'http': {'status': 400, 'headers': {}}, 'code': 'GRAPHQL_VALIDATION_FAILED', 'type': 'graphql error', 'userError': True}}]}

"""
webhook_query_text = """
query {
  webhooks{
    nodes {
      id
      label
      url
    }
  }
}
"""
target_webhook_label = "Gradio"  # filter not working
target_webhook_id = None
result = execute_query("webhook", webhook_query_text, api_key)
for webhook in result["data"]["webhooks"]["nodes"]:
    if target_webhook_label == webhook["label"]:
        target_webhook_id = webhook["id"]


os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"

# 1. Define  UI
with gr.Blocks() as ui:
    gr.Label("hello")

# 2. Create WebhooksServer with custom UI and secret
app = WebhooksServer(
    ui=ui,
    webhook_secret=os.environ["webhook_secret"],  # loaded by load_api_key
)

# 3. Register webhook with explicit name


@app.add_webhook("/linear_webhook")
async def hello(payload: WebhookPayload):
    pprint(payload.dict(), indent=4)

    return {"message": "ok"}


def webhook_update(url):
    webhook_update_text = """
mutation {
  webhookUpdate(
    id: "%s"
    input:{
    url:"%s"
    }
  ) {
    success
  }
}
""" % (target_webhook_id, url)
    result = execute_query("webhook_update", webhook_update_text, api_key)


# 5. Start server (optional)
app.launch(webhook_update=webhook_update)
