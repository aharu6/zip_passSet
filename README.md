# zip_passSet

## 概要

zip_passSet は、ZIP ファイルのパスワード管理と設定を行うツールです。複数の ZIP ファイルに対して、パスワードを設定・変更・検証することができます。
linux/windows両方で動作します。
ファイルの解凍時にはmacは標準のエクスプローラーで可能ですが、
windowsは7-z等の別途ツールがインストールされていない場合は本ツールでの解凍が必要になります。

## 主な機能

- ZIP ファイルへのパスワード設定
- パスワードの変更と管理
- パスワード検証機能
- バッチ処理対応

## 使用方法

### インストール

```bash
git clone https://github.com/aharu6/zip_passSet.git
cd zip_passSet
```

### 基本的な使い方

```bash
# ZIP ファイルにパスワードを設定
python zip_passSet.py -f <zip_file_path> -p <password>

# パスワードを検証
python zip_passSet.py -f <zip_file_path> -v <password>
```

### オプション

- `-f, --file`: 対象の ZIP ファイルパス（必須）
- `-p, --password`: 設定するパスワード
- `-v, --verify`: パスワード検証モード
- `-h, --help`: ヘルプ表示

## 例

```bash
# example.zip にパスワード "abc123" を設定
python zip_passSet.py -f example.zip -p abc123

# パスワードが正しいか検証
python zip_passSet.py -f example.zip -v abc123
```

## 要件

- Python 3.7 以上

## ライセンス

MIT License
