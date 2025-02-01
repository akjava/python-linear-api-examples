# Linear Issue Comment by Huggingface Example

このスクリプトは、Linear の Issue に AI モデルがコメントを生成し、開発者の Issue 内容の理解や解決策の検討をサポートさせる第一歩となるサンプルコードです。このスクリプトは Linear を利用している開発者向けです。

## 概要

このスクリプトは、以下の処理を自動化します。

1.  Linear API  を使用して最新の Issue を取得します。
2.  Huggingface Inference API を使用して、Issue の説明に基づいた解決策を生成します。
3.  生成された解決策を、Linear Issue のコメントとして追加します。

## 依存関係

*   `requests 2.32.3`: HTTP リクエストを行うためのライブラリ
*   `python-dotenv 1.0.1`: 環境変数から設定を読み込むためのライブラリ
*   `huggingface_hub 0.26.1`: Huggingface Inference API とやり取りするためのライブラリ
*   `linear_api_utils.py`: Linear API とのやり取りをサポートする自作モジュール (後述)
*   Python 3.10 で 上記ライブラリーのバージョンで動作を確認しました。

## セットアップ

### 環境変数の設定

1.  `.env` ファイルを作成し、以下の形式で Linear API キーと Hugging Face トークンを設定してください。

    ```
    LINEAR_API_KEY=your_linear_api_key
    hf_token=your_huggingface_token
    ```
    *   `LINEAR_API_KEY`: Linear API にアクセスするためのキー
    *   `hf_token`: Hugging Face Inference API にアクセスするためのトークン
2.  `.env` ファイルは `.gitignore` に追加して、決して公開しないようにしてください。


### linear_api_utils.py

このファイルは、Linear API とのやり取りを抽象化する自作モジュールです。

* 同階層においてあります。

## 使用方法

1.  `python linear_comment_generator.py` を実行します。
2.  スクリプトは、自動的に最新の Linear Issue を取得し、AI によって生成されたコメントを追加します。

### モデルの選択

以下のモデルが使用可能です。

*   `google/gemma-2-27b-it`
*   `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` 
*   `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-Japanese` は容量制限により使用できません。

## 入出力

*   **入力:**
    *   最新の Linear Issue のタイトルと説明文が入力として使用されます。
*   **出力:**
    *   出力されるコメントは、AI モデルの名前を含むヘッダーと、モデルによって生成された解決策のテキストで構成されます。
        ```markdown
        [ ](start-ai-comment:google/gemma-2-27b-it)
        # gemma-2-27b-itのコメント
        解決策は...
        ```
        以下出力例
        ```markdown
        [ ](start-ai-comment:google/gemma-2-27b-it)
        # gemma-2-27b-itのコメント
        このIssueは、○○に関する問題のようです。解決策としては、△△を検討すると良いでしょう。具体的な手順は以下の通りです。
        1. xxx
        2. yyy
        ```

## エラー処理

*   Hugging Face API のサーバーがダウンしている場合や、レート制限に達した場合にエラーが発生することがあります。
*   Hugging Face API への接続が失敗した場合は、時間をおいて再度実行するか、別のモデルを試してみてください。
*   エラーログは標準出力に表示されます。

## 注意事項/制限

*   使用する AI モデルが日本語に対応している必要があります。
*   Linear API と Hugging Face Inference API には、レート制限などの制限がある可能性があります。
*   現時点では、一度に処理できる Issue の数は 1 つに限定されています。
*    AIの出力は、必ずしも正しいとは限りません。出力されたコメントは必ず確認するようにしてください。
* 将来のバージョンでは、複数の Issue をまとめて処理できるようにする予定です。

## ライセンス

このプログラムは MIT ライセンスの下で公開されています。

## 貢献方法

*   バグを発見した場合は、GitHub の Issue トラッカーで報告してください。
*   機能要望や改善提案がある場合は、プルリクエストを送ってください。

## 著者/連絡先
Akihito Miyazaki
https://github.com/akjava