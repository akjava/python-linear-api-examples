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
    after = None
    active_issues_comment = {}

    page = 1
    while True:
        after_text = ""
        if after:
            after_text = f',after: "{after}"'
        """
            query-issues:デフォルトの値
            includeArchived :false - アーカイブ（削除）されたissueは含みません。
            orderBy :createdAt - 表示される順番は作成順です。(更新順ではない)

        """
        data = {
            "query": "{ issues(first: 10%s) { edges { node { id title comments { nodes {id}}} cursor} pageInfo {hasNextPage endCursor}}}"
            % (after_text)
        }
        print(f"process page {page}")
        page += 1
        result = request_linear(headers, data)
        # print(result)
        for node in result["data"]["issues"]["edges"]:
            issue_title = node["node"]["title"]
            issue_id = node["node"]["id"]
            # TODO if
            comment_data = {
                "query": '{issue(id:"%s"){comments { nodes { body}}}}'
                # "query": '{issues(filter:{id:{eq:"%s"}}){nodes{ comments { nodes { body}}}}}' 間違ってはないが、深い
                % (issue_id)
            }
            print(comment_data)

            comment_result = request_linear(headers, comment_data)
            print(comment_result)
            active_issues_comment[issue_title] = len(
                comment_result["data"]["issue"]["comments"]["nodes"]
                # comment_result["data"]["issues"]["nodes"][0]["comments"]["nodes"]
            )

        if not result["data"]["issues"]["pageInfo"]["hasNextPage"]:
            break
        else:
            after = result["data"]["issues"]["pageInfo"]["endCursor"]

    print(f"total issues {len(active_issues_comment.keys())}")
    for title in active_issues_comment.keys():
        print(f"{title} has {active_issues_comment[title]} comments")
