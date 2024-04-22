import glob
import os
import unittest
from pathlib import Path

import toml
import twine.commands.upload
from build.__main__ import main as build_main

assert (Path.home() / ".pypirc").exists(), "認証情報を~/.pypircに書いてください"


def update_toml():
    with open("pyproject.toml") as f:
        dict_toml = toml.load(f)
    version = [int(x) for x in dict_toml["project"]["version"].split(".")]
    version[2] += 1
    dict_toml["project"]["version"] = ".".join(str(x) for x in version)
    print("current version is", dict_toml["project"]["version"])
    with open("pyproject.toml", "w") as f:
        toml.dump(dict_toml, f)


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner()
    runner.run(suite)


def upload_package():
    dist_files = glob.glob("dist/*")
    twine.commands.upload.main(dist_files)


def clean_dist_files():
    dist_path = "dist/*"
    files = glob.glob(dist_path)
    for f in files:
        os.remove(f)
    print("distディレクトリ内のファイルを全削除しました。")


run_tests()
update_toml()
build_main([])
upload_package()
clean_dist_files()
