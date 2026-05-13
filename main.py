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
#解凍ツール
def extract_zip(zip_foldername, password, extract_to):
    zip_path = Path(zip_foldername)
    if not zip_path.exists() or not zip_path.is_file():
        print(f"エラー: zipファイルが見つかりません: {zip_foldername}")
        return False

    Path(extract_to).mkdir(parents=True, exist_ok=True)

    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.setpassword(password.encode("utf-8"))
            zf.extractall(extract_to)
        return True
    except RuntimeError:
        print("エラー: パスワードが正しくない可能性があります。")
        return False
    except pyzipper.BadZipFile:
        print("エラー: zipファイルが壊れているか、形式が不正です。")
        return False
    except OSError as e:
        print(f"エラー: 解凍中にファイル操作で失敗しました: {e}")
        return False
        
if __name__ == "__main__":
    #説明文表示
    print("このスクリプトは、パスワード付きzipフォルダを作成したり、解凍したりするためのツールです。\nコマンドラインツールとtkinter GUIの両方に対応しています。",
        "\n暗号化形式はAES-256を使用していますが、互換性のためにセキュリティは弱めになっています。",
        "\nlinuxやmacOSではデフォルトの環境で解凍ができますが、windowsでは7-Zipなどのサードパーティ製の解凍ツール・本ツールでの解凍が必要です。"
        )
    choice = input("コマンドラインツールかtkinter GUIのどちらを使用しますか？使用する方を入力してください (cli/gui): ").strip().lower()
    if choice == "cli":
        actions = input("zipファイルを作成しますか？解凍しますか？ (create/extract): ").strip().lower()
        zip_foldername = input("作成するzipフォルダの名前を入力してください（例: secret.zip）(注:拡張子.zipまで入力してください): ")
        password = getpass.getpass("パスワードを入力してください: ")
        if actions == "create":
            files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
            create_password_protected_zip(zip_foldername, password, files)
            print(f"{zip_foldername} が作成されました。")
        elif actions == "extract":
            extract_to = input("解凍先のフォルダを入力してください: ")
            if extract_zip(zip_foldername, password, extract_to):
                print(f"{zip_foldername} が {extract_to} に解凍されました。")
    elif choice == "gui":
        import tkinter as tk
        from tkinter import filedialog,simpledialog
        
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示にする
        actions = simpledialog.askstring("アクション選択", "zipファイルを作成しますか？解凍しますか？ (create/extract):")
        if actions is None:
            print("キャンセルされました。")
            root.destroy()
            raise SystemExit(0)

        actions = actions.strip().lower()

        if actions == "create":
            zip_foldername = simpledialog.askstring("Zipファイル名", "作成するzipフォルダの名前を入力してください（例: secret.zip）(注:拡張子.zipまで入力してください):")
            if not zip_foldername:
                print("zipファイル名が未入力のため処理を中止しました。")
                root.destroy()
                raise SystemExit(0)

            password = simpledialog.askstring("パスワード", "パスワードを入力してください:", show='*')
            if password is None:
                print("キャンセルされました。")
                root.destroy()
                raise SystemExit(0)

            files = filedialog.askdirectory(title="圧縮するフォルダを選択してください")
            if not files:
                print("圧縮するフォルダが未選択のため処理を中止しました。")
                root.destroy()
                raise SystemExit(0)

            create_password_protected_zip(zip_foldername, password, [files])
            print(f"{zip_foldername} が作成されました。")
        elif actions == "extract":
            zip_foldername = filedialog.askopenfilename(title="解凍するzipファイルを選択してください", filetypes=[("Zip files", "*.zip")])
            if not zip_foldername:
                print("解凍するzipファイルが未選択のため処理を中止しました。")
                root.destroy()
                raise SystemExit(0)

            password = simpledialog.askstring("パスワード", "パスワードを入力してください:", show='*')
            password = password.strip() if password else None
            if password is None:
                print("キャンセルされました。")
                root.destroy()
                raise SystemExit(0)

            extract_to = filedialog.askdirectory(title="解凍先のフォルダを選択してください")
            if not extract_to:
                print("解凍先フォルダが未選択のため処理を中止しました。")
                root.destroy()
                raise SystemExit(0)

            if extract_zip(zip_foldername, password, extract_to):
                print(f"{zip_foldername} が {extract_to} に解凍されました。")
        else:
            print("無効なアクションです。create または extract を入力してください。")

        root.destroy()
    else:
        print("無効な選択です。cli または gui を入力してください。")
        
