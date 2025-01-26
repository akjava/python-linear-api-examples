import codecs
import json
import os

from dotenv import load_dotenv
import requests

url = "https://api.linear.app/graphql"


def request_linear(headers, data):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # ステータスコードが200番台以外の場合に例外を発生させる
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラー: {e}")
        print(f"レスポンス内容:\n{response.text}")


def load_api_key():
    load_dotenv(dotenv_path=".env")
    if "api_key" in os.environ:
        api_key = os.environ["api_key"]
        return api_key
    else:
        print("'api_key' が環境変数にありません。")
        print(".envファイルを作成し 以下の行を追加してください。")
        print("api_key=your_api_key")
        print("このファイルは.gitignoreに追加して、決して公開しないでください。")
        print(
            "Linear Settings Security&access - Personal API keysからAPI Keyは作成できます。"
        )
        exit(0)


if __name__ == "__main__":
    headers = {
        "Content-Type": "application/json",
        "Authorization": load_api_key(),
    }

    data = {"query": "{ issues { nodes { id title } } }"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # ステータスコードが200番台以外の場合に例外を発生させる

        response_data = response.json()
        print(response_data)

        print(
            json.dumps(response_data, indent=2, ensure_ascii=False)
        )  # JSONを整形して表示

    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラー: {e}")
        print(f"レスポンス内容:\n{response.text}")
