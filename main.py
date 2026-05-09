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

        for raw_path in paths:
            path = Path(raw_path.strip())

            if path.is_file():
                zf.setpassword(password.encode("utf-8"))
                zf.write(path, arcname=path.name)
            elif path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file():
                        arcname = str(child.relative_to(path.parent))
                        zf.setpassword(password.encode("utf-8"))
                        zf.write(child, arcname=arcname)

if __name__ == "__main__":
    choice = input("コマンドラインツールかtkinter GUIのどちらを使用しますか？ (cli/gui): ").strip().lower()
    if choice == "cli":
        zip_foldername = input("作成するzipフォルダの名前を入力してください（例: secret.zip）(注:拡張子.zipまで入力してください): ")
        password = getpass.getpass("パスワードを入力してください: ")
        files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
        create_password_protected_zip(zip_foldername, password, files)
        print(f"{zip_foldername} が作成されました。")
    elif choice == "gui":
        import tkinter as tk
        from tkinter import filedialog,simpledialog
        
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示にする
        zip_foldername = simpledialog.askstring("Zipファイル名", "作成するzipフォルダの名前を入力してください（例: secret.zip）(注:拡張子.zipまで入力してください):")
        password = simpledialog.askstring("パスワード", "パスワードを入力してください:", show='*')
        files = filedialog.askdirectory(title="圧縮するフォルダを選択してください")
        create_password_protected_zip(zip_foldername, password, [files])
        print(f"{zip_foldername} が作成されました。")
    else:
        print("無効な選択です。cli または gui を入力してください。")
        
