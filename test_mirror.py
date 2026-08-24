import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import mirror


class FakeResponse:
    status = 200

    def __init__(self, body=b""):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


class PyPIProjectTests(unittest.TestCase):
    @patch.object(mirror.urllib.request, "urlopen")
    def test_queries_canonical_project_for_latest_version(self, urlopen):
        urlopen.return_value = FakeResponse(
            b'{"releases":{"0.6.3":[],"0.6.4":[],"0.7.0rc1":[]}}'
        )

        self.assertEqual(mirror.get_latest_upd_version(), "0.6.4")
        urlopen.assert_called_once_with("https://pypi.org/pypi/upd/json")

    @patch.object(mirror.urllib.request, "urlopen")
    def test_waits_for_version_on_canonical_project(self, urlopen):
        urlopen.return_value = FakeResponse()

        self.assertTrue(mirror.wait_for_pypi("0.6.4"))
        urlopen.assert_called_once_with("https://pypi.org/pypi/upd/0.6.4/json")


class UpdatePyprojectTomlTests(unittest.TestCase):
    def test_migrates_legacy_dependency_to_canonical_project(self):
        with tempfile.TemporaryDirectory() as directory:
            pyproject = Path(directory, "pyproject.toml")
            pyproject.write_text(
                '[project]\nname = "upd-pre-commit"\nversion = "0.6.3"\n'
                'dependencies = ["upd-cli==0.6.3"]\n'
            )

            previous_directory = Path.cwd()
            try:
                os.chdir(directory)
                changed = mirror.update_pyproject_toml("0.6.4")
            finally:
                os.chdir(previous_directory)

            self.assertTrue(changed)
            self.assertIn('version = "0.6.4"', pyproject.read_text())
            self.assertIn('"upd==0.6.4"', pyproject.read_text())

    def test_updates_existing_canonical_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            pyproject = Path(directory, "pyproject.toml")
            pyproject.write_text(
                '[project]\nname = "upd-pre-commit"\nversion = "0.6.4"\n'
                'dependencies = ["upd==0.6.4"]\n'
            )

            previous_directory = Path.cwd()
            try:
                os.chdir(directory)
                changed = mirror.update_pyproject_toml("0.6.5")
            finally:
                os.chdir(previous_directory)

            self.assertTrue(changed)
            self.assertIn('version = "0.6.5"', pyproject.read_text())
            self.assertIn('"upd==0.6.5"', pyproject.read_text())


if __name__ == "__main__":
    unittest.main()
