"""ZipCryptoを使用してパスワード付きzipフォルダを作成するスクリプト"""

import pyzipper
import os
import getpass

def create_password_protected_zip(zip_foldername, password, files):
    # 互換性重視（セキュリティは弱め）
    with pyzipper.AESZipFile(zip_foldername, 'w',
                        compression=pyzipper.ZIP_DEFLATED,
                        encryption=pyzipper.ZIP_CRYPTO) as zf:
        zf.setpassword(password.encode('shift-jis'))
        for file in files:
            zf.write(file, os.path.basename(file))#ファイル名だけで保存
        
if __name__ == "__main__":
    zip_foldername = input("作成するzipフォルダの名前を入力してください（例: secret.zip）: ")
    password = getpass.getpass("パスワードを入力してください: ")
    files = input("圧縮するファイルのパスをカンマ区切りで入力してください: ").split(",")
    create_password_protected_zip(zip_foldername, password, files)
    print(f"{zip_foldername} が作成されました。")