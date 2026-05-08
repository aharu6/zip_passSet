"""
パスワード付きzipフォルダを作成するスクリプト
コマンドラインで動作する
"""

import pyzipper
import os
import getpass
from pathlib import Path

def create_password_protected_zip(zip_foldername, password, paths):
    # 互換性重視（セキュリティは弱め）
    with pyzipper.AESZipFile(
        zip_foldername,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zf:
        zf.setpassword(password.encode("utf-8"))

        for raw_path in paths:
            path = Path(raw_path.strip())

            if path.is_file():
                zf.write(path, arcname=path.name)
            elif path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file():
                        arcname = str(child.relative_to(path.parent))
                        zf.write(child, arcname=arcname)

if __name__ == "__main__":
    zip_foldername = input("作成するzipフォルダの名前を入力してください（例: secret.zip）: ")
    password = getpass.getpass("パスワードを入力してください: ")
    files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
    create_password_protected_zip(zip_foldername, password, files)
    print(f"{zip_foldername} が作成されました。")
