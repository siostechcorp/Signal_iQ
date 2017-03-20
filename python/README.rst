SignaliQ
=============================

This SDK provides the set of methods and models in python that allow integration with SIOS iQ Machine Learning product capabilities.

Importing SDK
-------------

- TODO

Quick Start
-----------
- Clone the repository.

.. code:: bash

    git clone https://github.com/siostechcorp/Signal_iQ.git

- Install required packages (requires sudo).

.. code:: bash

    sudo pip install -r requirements.txt

- Copy `SignaliQ/config.sample.ini` to `SignaliQ/config.ini`.

- Update `config.ini` with **SIOS iQ** username and password, typically one used to log into the UI.

- Run the **example** script to test that you can send a message to **SIOS iQ** instance

.. code:: bash

    python test/scripts/example.py


(Optional) Setting up Virtual Environment
-----------------------------------------
- The following directions are for setting up `virtualenv`, instead of using your system's python version.

- Using a virtual environment will limit your packages to just the user's home directory; therefore, no need for `sudo`.

- Create the virtualenvs. The name of the directory is arbitrary, any name will do.

.. code:: bash

  mkdir ~/.virtualenv
  virtualenv --python=python3.4 ~/.virtualenv/sdk3
  virtualenv --python=python2.7 ~/.virtualenv/sdk2

- Activate virtual environment (for Python3)

.. code:: bash

    source ~/.virtualenv/sdk3/bin/activate

- Install dev packages. These are optional tools for development.

.. code:: bash

    pip install -r requirements.dev.txt


- Test that everything is installed correctly.

.. code:: bash

    make lint
    make test

- To create project template the first time use `cookiecutter`_.

.. code:: bash

    cookiecutter https://github.com/Nekroze/cookiecutter-pypackage.git

- Install any extra packages, and if needed edit the `requirements.dev.txt`.


.. _cookiecutter: https://github.com/Nekroze/cookiecutter-pypackage
