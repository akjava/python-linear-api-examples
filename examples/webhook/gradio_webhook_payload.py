"""
このコードは以下のコードをLinear.appに対応させたものです。公式のコードではありません。
https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/_webhooks_payload.py

まだ、Issue Objectのごく一部しか対応してません。実際には、設定次第でissue以外のデーターも飛んでくるようになりますが、対応してません。(Unionとか使うぽい)
https://studio.apollographql.com/public/Linear-API/variant/current/schema/reference/objects/Issue

Issueの新規・更新・削除は確認しました。

そして、変更が激しい部分なので、将来 属性が、deprecatedからremovedになりエラーが出るかもしれません。


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

"""Contains data structures to parse the webhooks payload."""

from typing import List, Literal, Optional
from datetime import datetime


def is_pydantic_available():
    return True


if is_pydantic_available():
    from pydantic import BaseModel
else:
    # Define a dummy BaseModel to avoid import errors when pydantic is not installed
    # Import error will be raised when trying to use the class

    class BaseModel:  # type: ignore [no-redef]
        def __init__(self, *args, **kwargs) -> None:
            raise ImportError(
                "You must have `pydantic` installed to use `WebhookPayload`. This is an optional dependency that"
                " should be installed separately. Please run `pip install --upgrade pydantic` and retry."
            )


# This is an adaptation of the ReportV3 interface implemented in moon-landing. V0, V1 and V2 have been ignored as they
# are not in used anymore. To keep in sync when format is updated in
# https://github.com/huggingface/moon-landing/blob/main/server/lib/HFWebhooks.ts (internal link).


class WebhookPayloadUploadFrom(BaseModel):
    stateId: Optional[str] = None
    updatedAt: datetime
    description: Optional[str] = None


class WebhookPayloadTeam(BaseModel):
    id: str
    name: str
    key: str


class WebhookPayloadProject(BaseModel):
    id: str
    name: str
    url: str


class WebhookPayloadState(BaseModel):
    id: str
    color: str
    name: str
    type: str


class WebhookPayloadLabel(BaseModel):
    id: str
    color: str
    name: str


class WebhookPayloadData(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    archivedAt: Optional[datetime] = None
    title: str
    description: Optional[str] = None
    labels: List[WebhookPayloadLabel]
    priority: int
    estimate: Optional[int] = None
    startedAt: Optional[datetime] = None
    state: WebhookPayloadState
    team: WebhookPayloadTeam
    project: WebhookPayloadProject


class WebhookPayload(BaseModel):
    action: str
    type: str
    createdAt: str
    data: WebhookPayloadData
    url: Optional[str] = None
    webhookTimestamp: int
    webhookId: str
    updatedFrom: Optional[WebhookPayloadUploadFrom] = None
