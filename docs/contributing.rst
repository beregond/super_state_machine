============
Contributing
============

Contributions are welcome. Report bugs and propose changes on
`GitHub <https://github.com/beregond/super_state_machine>`_.

Development setup
-----------------

Clone the repository and install the package with its development extras::

    $ git clone https://github.com/beregond/super_state_machine.git
    $ cd super_state_machine
    $ uv sync --extra dev --extra docs

Or with plain ``pip``::

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -e ".[dev,docs]"

Tests
-----

::

    $ python -m pytest src

The examples in the documentation are doctests::

    $ python -m pytest --doctest-glob="*.rst" docs

CI runs the tests on Python 3.10 to 3.14.

Lint
----

The ruff version is pinned in ``pyproject.toml`` (``dev`` extra), and CI uses
that pin. Run the same version locally::

    $ ruff check .
    $ ruff format --check .

Documentation
-------------

Build the HTML docs into ``docs/_build/html``::

    $ sphinx-build -W docs docs/_build/html

``docs/readme.rst`` includes ``README.md``, so README changes show up in the
docs too.

Changelog
---------

Do not edit ``HISTORY.rst``. Add a one-line entry for every user-visible
change with `pyhistory <https://pypi.org/project/pyhistory/>`_::

    $ pyhistory add "Added X."

This writes a file into ``history/``, commit it with your change. The
maintainer merges these entries into ``HISTORY.rst`` at release time.

Pull requests
-------------

Before you open a pull request, check that:

1. Tests pass and new behaviour has tests.
2. Ruff check and format are clean.
3. Docs are updated if the public API changed.
4. A ``history/`` entry is added for user-visible changes.
