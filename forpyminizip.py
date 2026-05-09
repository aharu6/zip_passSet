"""pyminizipでパスワード付きzipファイルを作成するスクリプト
pyminizipがインストールできない

"""
import pyminizip
import os
from pathlib import Path

def create_zip(zip_filename, password, files):
    for raw_path in files:
        path = Path(raw_path.strip())
        if path.is_file():
            pyminizip.compress(str(path), None, zip_filename, password, 5)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    arcname = str(child.relative_to(path.parent))
                    pyminizip.compress(str(child), None, zip_filename, password, 5)

if __name__ == "__main__":
    zip_filename = input("作成するzipファイルの名前を入力してください（例: secret.zip）: ")
    password = input("パスワードを入力してください: ")
    files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
    create_zip(zip_filename, password, files)
    print(f"{zip_filename} が作成されました。")