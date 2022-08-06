Welcome to docs-helper's documentation!
=======================================

Simple interactive wrapper over sphobjinv and your sphinx conf.py to make it easier to cross-reference with intersphinx.

insted of: ``python -m sphinx.ext.intersphinx https://www.sphinx-doc.org/en/master/objects.inv``

install and run ``docs-helper`` and then pick the project you want.

Wraps also over `sphobjinv <https://github.com/bskinn/sphobjinv>`_ to make easy to search.

.. todo::
    - set chmod on env file like ssh does to keys
    - autofix shorthand
      https://github.com/bskinn/sphobjinv/issues/234
    - idea make it a sphinx plugin to autofix the setup and extract build_dir

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    usage
    development
    apireference
    changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`