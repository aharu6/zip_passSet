"""zipcrypto形式でパスワード付きzipファイルを作成するスクリプト"""
import zipfile
import os
from pathlib import Path
import getpass

def create_zipcrypto_zip(zip_filename, password, files):
    with zipfile.ZipFile(
        zip_filename,
        'w',
        zipfile.ZIP_DEFLATED
        ) as zipf:
        for raw_path in files:
            path = Path(raw_path.strip())
            if path.is_file():
                zipf.setpassword(password.encode("utf-8"))
                zipf.write(path, arcname=path.name)
            elif path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file():
                        arcname = str(child.relative_to(path.parent))
                        zipf.setpassword(password.encode("utf-8"))
                        zipf.write(child, arcname=arcname)
                        

if __name__ == "__main__":
    zip_filename = input("作成するzipファイルの名前を入力してください（例: secret.zip）: ")
    password = getpass.getpass("パスワードを入力してください: ")
    files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
    create_zipcrypto_zip(zip_filename, password, files)
    print(f"{zip_filename} が作成されました。")