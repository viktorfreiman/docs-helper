__doc__ = """

docs_helper.py
--------------

| Small script that makes it easier to work with intersphinx it takes config data from docs/conf.py
| :doc:`sphinx:usage/extensions/intersphinx`

:ref:`sphinx:xref-syntax`

| insted of: ``python -m sphinx.ext.intersphinx https://www.sphinx-doc.org/en/master/objects.inv``
| run ``python scripts/docs_helper.py.py`` and then pick the project you want.

Wraps also over `sphobjinv <https://github.com/bskinn/sphobjinv>`_ to make easy to search

"localhost" need to have a webserver with built html from sphinx,
have ``autobuild-html-docs`` running

We don't need to use edit sys.path and and then to import

We only use importlib.util
"""

import importlib.util
import os
import signal
import sys
from pathlib import Path
from urllib.parse import urljoin


def _signal_SIGINT_handler(signal, frame):
    """This is to have a nicer printout on KeyboardInterrupt"""
    print("\nGOT SIGINT(Probably KeyboardInterrupt), Quitting")
    sys.exit(0)


def main():
    # Just expect we are in the docs folder
    # This fixes all things and just give the user error if we can't find conf.py
    # If we can't find intersphinx_mapping -> quit

    print("Intersphinx objects.inv printout")

    print(f'{Path("conf.py").resolve()}')
    conf = get_py_config(Path("conf.py"))

    try:
        intersphinx_mapping = conf.intersphinx_mapping
    except AttributeError:
        print("Can't find intersphinx_mapping, quitting")
        sys.exit(1)
    # # add localhost to make easy to see self
    # intersphinx_mapping[project] = (
    #     next(search_docs_parent.glob("_?build/html/objects.inv")),
    #     None,
    # )

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

    if picked_name == project:
        obj_inv_path = intersphinx_mapping[project][0]
    else:
        # the extra slash if it is missing in the config data
        # and urljoin will fix the url for us
        obj_inv_path = urljoin(intersphinx_mapping[picked_name][0] + "/", "objects.inv")

    if type_picker:
        print("--- sphobjinv ---")
        search = input("Search: ")
        cli = f"sphobjinv suggest {obj_inv_path} {search} -su"

    else:
        print("--- intersphinx ---")
        cli = f"{sys.executable} -m sphinx.ext.intersphinx {obj_inv_path}"

    os.system(cli)

    # todo: Change this printout to use triple quotes insted
    print(
        "--- Note ---\n"
        "Please note the output from this tools\n"
        "need to be changed to work as a cross-references\n"
        "Exemple:\n"
        ":std:label:`thing_to_link` -> :ref:`thing_to_link`\n"
        "or\n"
        ":std:label:`thing_to_link` -> :ref:`project_name:thing_to_link`\n\n"
        ":py:function:`that_func`   -> :py:func:`that_func`\n"
        "or\n"
        ":py:function:`that_func`   -> :py:func:`project_name:that_func`\n"
        "--- Note ---\n"
    )

    print(
        "--- Links ---\n"
        "Link for intersphinx cross-referencing tags\n"
        "https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#xref-syntax\n"  # noqa b950
        "--- Links ---\n"
    )

    print(f"CLI:\n{cli}")


def get_py_config(path: Path):
    """Imports the sphinx to extract the intersphinx mapping

    Uses importlib.util tricks to import without the problems of edit sys.path
    and python lint missing imports

    .. note::
        This function will execute the input file

    from:
    https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    module_name = path.name

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    # sys.mod is good to set
    sys.modules[module_name] = module

    # Execte the imported file
    spec.loader.exec_module(module)

    return module


if __name__ == "__main__":
    # activate signal
    signal.signal(signal.SIGINT, _signal_SIGINT_handler)

    main()
