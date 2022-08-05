from pathlib import Path

import docs_helper
import toml

test_path = Path(__file__).absolute().parent
project_path = test_path.parent

pyproject = toml.load(project_path / "pyproject.toml")


def test_version():
    assert docs_helper.__version__ == pyproject["tool"]["poetry"]["version"]


def test_missing_conf_py():
    assert docs_helper.main() == 1
