import io
import os
import pathlib as pl
import shutil
import unittest
from typing import IO

from project.core import api


class TestTerm(api.Terminal):
    def __init__(self, back: IO) -> None:
        self.io = back

    def stdin(self) -> IO:
        return self.io

    def stdout(self) -> IO:
        return self.io


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = api.SimpleBoot().start()
        self.test_msg = "Hello Friends\n"

    def test_stdio(self) -> None:
        self.back_io = io.StringIO()
        term = TestTerm(self.back_io)
        self.api.add_terminal("Test", term)

        self.api.send_to_all(self.test_msg)
        self.assertEqual(
            self.back_io.getvalue(), self.test_msg, "Testing stdout of terminals"
        )

    def test_fs(self) -> None:
        self.assertFalse(self.api.exists_file("not_a_file"))
        with pl.Path("./.test_fs/a_file").open("w") as f:
            f.write(self.test_msg)
        self.assertTrue(self.api.exists_file("a_file"))
        with self.api.open_file("a_file", "r") as f:
            self.assertEqual(self.test_msg, f.read())

    def test_command(self) -> None:
        cmd = tuple(self.api.resolve_commands())
        print(cmd)
        self.assertEqual(len(cmd), 6)

    def tearDown(self) -> None:
        shutil.rmtree("./.test_fs")
        os.mkdir("./.test_fs")
        shutil.copytree("../project/file_system/bin", "./.test_fs/bin")
        pass


if __name__ == "__main__":
    unittest.main()
