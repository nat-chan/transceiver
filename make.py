import glob
import unittest
from pathlib import Path

import twine.commands.upload
from build.__main__ import main as build_main

assert (Path.Home() / ".pypirc").exists(), "認証情報を~/.pypircに書いてください"


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner()
    runner.run(suite)


def upload_package():
    dist_files = glob.glob("dist/*")
    twine.commands.upload.main(dist_files)


run_tests()
build_main([])
upload_package()
