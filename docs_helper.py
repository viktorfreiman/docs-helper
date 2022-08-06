__doc__ = """

docs_helper.py
--------------

| Small script that makes it easier to work with intersphinx it takes config data from docs/conf.py
| :doc:`sphinx:usage/extensions/intersphinx`

:ref:`sphinx:xref-syntax`

| insted of: ``python -m sphinx.ext.intersphinx https://www.sphinx-doc.org/en/master/objects.inv``
| run ``python scripts/docs_helper.py.py`` and then pick the project you want.

Wraps also over `sphobjinv <https://github.com/bskinn/sphobjinv>`_ to make easy to search

We don't need to use edit sys.path and and then to import

We only use importlib.util

.. todo::
    set chmod on env file like ssh does to keys

    autofix shorthand
    https://github.com/bskinn/sphobjinv/issues/234

.. note::

    idea make it a sphinx plugin to autofix the setup and extract build_dir

"""

import importlib.util
import re
import signal
import subprocess
import sys
from pathlib import Path
from typing import Union
from urllib.parse import urljoin, urlparse


def _signal_SIGINT_handler(signal, frame):
    """This is to have a nicer printout on KeyboardInterrupt"""
    print("\nGOT SIGINT(Probably KeyboardInterrupt), Quitting")
    sys.exit(0)


__version__ = "0.0.9"


def main():
    # Just expect we are in the docs folder
    # This fixes all things and just give the user error if we can't find conf.py
    # If we can't find intersphinx_mapping -> quit

    # # for testing
    # import os
    # os.chdir("/workspaces/docs-helper/docs")

    conf_path = Path("conf.py")

    if not conf_path.exists():
        print("Can't find conf.py")
        return 1

    print("Intersphinx objects.inv printout")
    conf_path = conf_path.resolve()
    print(f"conf_path={conf_path}")
    conf = get_py_config(conf_path)

    try:
        intersphinx_mapping = conf.intersphinx_mapping
    except AttributeError:
        print("Can't find intersphinx_mapping, quitting")
        return 1

    build_dir = find_bild_dir()

    # add local-project to make easy to see self
    intersphinx_mapping[conf.project] = (
        build_dir / "html/objects.inv",
        None,
    )

    for i, doc in enumerate(intersphinx_mapping.keys()):
        print(f"{i}) {doc}")
    int_picker = int(input("Pick a number for docs: "))

    picked_name = list(intersphinx_mapping.keys())[int_picker]
    print(f"picked: {picked_name}\n")

    type_picker = int(
        input(
            f"0) Print all from objects.inv from {picked_name}\n"
            f"1) Search and suggest object\n"
            f"Select mode: "
        )
    )

    if picked_name == conf.project:
        obj_inv_path = intersphinx_mapping[conf.project][0]
    else:
        # the extra slash if it is missing in the config data
        # and urljoin will fix the url for us
        obj_inv_path = urljoin(intersphinx_mapping[picked_name][0] + "/", "objects.inv")

    if type_picker:
        print("--- sphobjinv ---")
        search = input("Search: ")

        cli = ["sphobjinv", "suggest", obj_inv_path, search, "-s"]
        if urlparse(str(obj_inv_path)).scheme:
            cli.append("--url")

    else:
        print("--- intersphinx ---")
        cli = [sys.executable, "-m", "sphinx.ext.intersphinx", obj_inv_path]

    cli_out = subprocess.check_output(cli).decode()
    print(cli_out)

    print(
        """
--- Note ---
Please note the output from this tools
need to be changed to work as a cross-references
Exemple:
:std:label:`thing_to_link` -> :ref:`thing_to_link`
or
:std:label:`thing_to_link` -> :ref:`project_name:thing_to_link`

:py:function:`that_func`   -> :py:func:`that_func`
or
:py:function:`that_func`   -> :py:func:`project_name:that_func`
--- Note ---
--- Links ---
Link for intersphinx cross-referencing tags
https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#xref-syntax
--- Links ---
    """
    )

    print(f'CLI:\n{" ".join(list(map(str, cli)))}')


def get_py_config(path: Union[Path, str]):
    """Imports the sphinx to extract the intersphinx mapping

    Uses importlib.util tricks to import without the problems of edit sys.path
    and python lint missing imports

    .. note::
        This function will execute the input file

    from:
    https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    module_name = Path(path).name

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    # sys.mod is good to set
    sys.modules[module_name] = module

    # Execte the imported file
    spec.loader.exec_module(module)

    return module


def find_bild_dir():
    """
    Support only Makefile for now

    Per sphinx ref there are
    https://www.sphinx-doc.org/en/master/man/sphinx-build.html#environment-variables

    .. todo::
        support for make.bat and ENV
    """
    with open("Makefile") as mfile:
        data = mfile.read()
        match = re.search("BUILDDIR += (.+)", data)
        if match:
            return Path(match.group(1)).resolve()


if __name__ == "__main__":
    # activate signal
    signal.signal(signal.SIGINT, _signal_SIGINT_handler)

    # https://docs.python.org/3/library/__main__.html#packaging-considerations
    sys.exit(main())
