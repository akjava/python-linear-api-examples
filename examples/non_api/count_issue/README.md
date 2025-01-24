# count_issue.py

## コードの内容
このPythonコードでは、csvモジュールを使ってCSVファイルを読み込んでいます。CSVの1行目は、"ID","Team","Title","Description","Status"...といったヘッダーになっており、それをキーとして各行を辞書形式に変換します。念のため、データの長さをチェックしています。Archivedとは、LinearでIssueが削除された時に一時的に設定される状態を表し、残りがActive Issueです。

## 実行結果
このコードは、コマンドプロンプトで実行できます。実行すると、以下のように、アーカイブされたIssueとアクティブなIssueの数が表示されます。

PS C:\pythons\test> python .\count_issue.py -i "Export Wed Jan 22 2025.csv"
total 101 archived 90 active 14
この結果から、現在のプロジェクトにおけるIssueの数を把握できます。