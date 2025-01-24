"""
License MIT
https://github.com/akjava/
"""

import os

import argparse
import csv


def parse_arguments():
    """引数を解析します。

    Returns:
    """
    parser = argparse.ArgumentParser(description="create rotated data")
    parser.add_argument("--input", "-i", default="example.csv", help="Input Linear CSV")
    return parser.parse_args()


def read_csv_with_newlines(filepath):
    """
    改行を含むCSVファイルを読み込む関数

    Parameters:
        filepath (str): CSVファイルのパス

    Returns:
        list: 読み込んだCSVデータをリストのリストで返す
    """
    data = []
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def issue_text_to_dict(head, csv_lines):
    """
    issue-csv-textを辞書に変換

    Parameters:
        head (str):header 通常csvの最初の行
        csv_lines:csvテキストのリスト

    Returns:
        list: 読み込んだissue-CSVデータを辞書のリストで返す
    """
    result = []
    for line in csv_lines:
        dict = {}
        for i, key in enumerate(head):
            if i < len(line):
                dict[key] = line[i]
        result.append(dict)
    return result


if __name__ == "__main__":
    args = parse_arguments()
    csv_path = args.input
    if not os.path.exists(csv_path):
        print(f"csv not exist {csv_path}")
        exit(0)

    csv_issue_texts = read_csv_with_newlines(csv_path)
    dicts = issue_text_to_dict(csv_issue_texts[0], csv_issue_texts[1:])
    archived = 0
    for dic in dicts:
        if dic["Archived"]:
            archived += 1
    print(f"total {len(dicts)} archived {archived} active {len(dicts)-archived}")
