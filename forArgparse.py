import argparse
from pathlib import Path
import pyzipper


def add_tree_to_zip(zf, src_dir: Path) -> None:
    src_dir = src_dir.resolve()

    for p in src_dir.rglob("*"):
        if p.is_file():
            # zip -r で絶対パスを渡したときに近い保存名: 先頭 / を除いた絶対パス
            arcname = str(p.resolve()).lstrip("/")
            zf.write(str(p), arcname)


def create_zip(zip_path: str, src_dir: str, password: str) -> None:
    with pyzipper.AESZipFile(
        zip_path,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.ZIP_CRYPTO,  # zip -P 相当の互換性重視方式
    ) as zf:
        zf.setpassword(password.encode("utf-8"))
        add_tree_to_zip(zf, Path(src_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="zip -r -P 相当でフォルダをパスワード付き圧縮する"
    )
    parser.add_argument(
        "--zip",
        default="/Users/aizawaharuka/Documents/GitHub/zip_pasSet.zip",
        help="作成する zip ファイルのパス",
    )
    parser.add_argument(
        "--src",
        default="/Users/aizawaharuka/Documents/test_csv",
        help="圧縮元フォルダのパス",
    )
    parser.add_argument(
        "--password",
        default="pass",
        help="zip パスワード",
    )
    args = parser.parse_args()

    create_zip(args.zip, args.src, args.password)
    print(f"作成完了: {args.zip}")