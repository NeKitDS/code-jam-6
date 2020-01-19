import io
import os
import pathlib as pl
import shutil
import sys
import unittest

from project.core import api
from project.core.terminal import IOTerminal


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = api.SimpleBoot().start()
        self.test_msg = "Hello Friends\n"
        self.term = IOTerminal(self.api)
        os.mkdir("./.test_fs")
        shutil.copytree("../project/file_system/bin", "./.test_fs/bin")

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

    def test_cd(self) -> None:
        i = io.StringIO("cd bin")
        o = io.StringIO()
        sys.stdin = i
        sys.stdout = o
        self.term = IOTerminal(self.api, ps_format='{path}')
        try:
            self.term.start()
        except EOFError:
            self.assertIn('bin', o.getvalue())

    def test_cat(self) -> None:
        with pl.Path("./.test_fs/a_file").open("w") as f:
            f.write(self.test_msg)
        i = io.StringIO("cat a_file")
        o = io.StringIO()
        sys.stdin = i
        sys.stdout = o
        self.term = IOTerminal(self.api, ps_format='')
        try:
            self.term.start()
        except EOFError:
            self.assertEqual(o.getvalue(), f"{self.test_msg}\n")

    def test_echo(self) -> None:
        i = io.StringIO(f"echo {self.test_msg}")
        o = io.StringIO()
        sys.stdin = i
        sys.stdout = o
        self.term = IOTerminal(self.api, ps_format='')
        try:
            self.term.start()
        except EOFError:
            self.assertEqual(o.getvalue(), self.test_msg)

    def test_touch(self) -> None:
        i = io.StringIO(f"touch touched")
        o = io.StringIO()
        sys.stdin = i
        sys.stdout = o
        self.term = IOTerminal(self.api, ps_format='')
        try:
            self.term.start()
        except EOFError:
            self.assertTrue(self.api.exists_file('touched'))

    def tearDown(self) -> None:
        shutil.rmtree("./.test_fs")
        pass


if __name__ == "__main__":
    unittest.main()
