# Installation

This chapter contains the installation instructions for the distributed quantum Fourier
transformation (DQFT)
software developed by "team Q-Harmonics" as part of the
[Quantum Internet Hackathon (QIH) 2022](https://labs.ripe.net/author/karla-white/take-part-in-the-quantum-internet-hackathon-2022/).
For a general overview of the QIH 2022 hackathon and the team Q-Harmonics DQFT project
see the [README](../README.md) file.

These installation instructions have been tested on a MacBook Air running macOS Catalina, but
they should work with little or no changes on any other platform including Windows or Linux.

We assume that you already have the following software installed on your computer:
 * Python 3.8.x: Needed to run the Python code in the repo.
 * Pip: Needed to install [PyPI](https://pypi.org/) dependencies.
 * Git: Need to clone git repository from GitHub and work on it.
 * Some code editor: I use Visual Studio Code (VSC).
 * Some way to run Jupyter notebooks: I use the Microsoft Jupyter extension in Visual Studio Code.

On macOS we recommend using `brew` to install this software if you don't already have it.

# Minimal installation instructions

The minimal installation instructions allow you read all of the team Q-Harmonics code and
to run the Qiskit-related code.
To also run the QNE-ADK related code you will need to follow the additional instructions
[below](#additional-installation-instructions-for-qne-adk-related-code).

## Clone the repository

Clone the 
[`brunorijsman/quantum-internet-hackathon-20022`](https://github.com/brunorijsman/quantum-internet-hackathon-2022/)
GitHub repository:

<pre>
$ <b>git clone https://github.com/brunorijsman/quantum-internet-hackathon-2022.git</b>
Cloning into 'quantum-internet-hackathon-2022'...
remote: Enumerating objects: 474, done.
remote: Counting objects: 100% (114/114), done.
remote: Compressing objects: 100% (78/78), done.
remote: Total 474 (delta 62), reused 75 (delta 31), pack-reused 360
Receiving objects: 100% (474/474), 2.04 MiB | 5.24 MiB/s, done.
Resolving deltas: 100% (238/238), done.
</pre>

In the remainder of these installation instructions, I will use the `QIH_2022_ROOT` environment
variable to refer to the directory in which you cloned the repository:

<pre>
$ <b>export QIH_2022_ROOT=$(pwd)</b>
</pre>

## Create and activate a Python virtual environment

Change directory to the newly created local clone:

<pre>
$ <b>cd ${QIH_2022_ROOT}/quantum-internet-hackathon-2022</b>
</pre>

Create a Python virtual environment:

<pre>
$ <b>python3.8 -m venv venv</b>
</pre>

<b>Note:</b>You must use Python3.8.x. QNE-ADK does not yet work with Python3.9.x or later.
I have not tested with Python 3.7.x or earlier. I recommend using `brew` to install Python 3.8 on
your Mac and using `pyenv` for making Python3.8 the default Python version for this project.

Activate the virtual environment:

<pre>
$ <b>source venv/bin/activate</b>
(venv) $
</pre>

<b>Note:</b> Every time you open a new shell or new terminal window, you must activate the
virtual environment. Your command-line prompt includes `(venv)` when the virtual environment is
active.

## Install the dependencies

Upgrade `pip` to the latest version:

<pre>
(venv) $ <b>pip install --upgrade pip</b>
Requirement already satisfied: pip in ./venv/lib/python3.8/site-packages (22.0.4)
Collecting pip
  Using cached pip-22.3.1-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 22.0.4
    Uninstalling pip-22.0.4:
      Successfully uninstalled pip-22.0.4
Successfully installed pip-22.3.1
</pre>

Use `pip` to install the `wheel` package:

<pre>
(venv) $ <b>pip install wheel</b>
Collecting wheel
  Using cached wheel-0.38.4-py3-none-any.whl (36 kB)
Installing collected packages: wheel
Successfully installed wheel-0.38.4
</pre>

Use `pip` to install the Qiskit textbook package:

<pre>
$ <b>pip install git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src</b>
Collecting git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src
  Cloning https://github.com/qiskit-community/qiskit-textbook.git to /private/var/folders/fm/m9yystmd0673fvqd2811t_c00000gn/T/pip-req-build-n3w1vg5t
  Running command git clone --filter=blob:none --quiet https://github.com/qiskit-community/qiskit-textbook.git /private/var/folders/fm/m9yystmd0673fvqd2811t_c00000gn/T/pip-req-build-n3w1vg5t
  Resolved https://github.com/qiskit-community/qiskit-textbook.git to commit 7787075d0a02f7b6bacc2e624842902e1318621a
  Preparing metadata (setup.py) ... done
Collecting qiskit
  Using cached qiskit-0.39.3-py3-none-any.whl
...
Building wheels for collected packages: qiskit-textbook
  Building wheel for qiskit-textbook (setup.py) ... done
  Created wheel for qiskit-textbook: filename=qiskit_textbook-0.1.0-py3-none-any.whl size=17557 sha256=f5ecc0782bf7f08c5ea26fb40d0ce48017fab34fb0ecd7c58814f46fa12ca6e4
  Stored in directory: /private/var/folders/fm/m9yystmd0673fvqd2811t_c00000gn/T/pip-ephem-wheel-cache-w0b6e2y4/wheels/80/c4/dd/b7ea1ee2a7247e8997db78bc777bbe22e61ab1e5ed1c4b46e1
Successfully built qiskit-textbook
Installing collected packages: wcwidth, pure-eval, ptyprocess, ply, pickleshare, mpmath, executing, backcall, appnope, widgetsnbextension, 
...
jupyter-client, cryptography, requests-ntlm, qiskit-terra, ipython, qiskit-ibmq-provider, qiskit-aer, ipykernel, qiskit, ipywidgets, qiskit-textbook
Successfully installed appnope-0.1.3 asttokens-2.2.0 backcall-0.2.0 certifi-2022.9.24 cffi-1.15.1 charset-normalizer-2.1.1 contourpy-1.0.6 cryptography-38.0.4 cycler-0.11.0 debugpy-1.6.4 decorator-5.1.1 dill-0.3.6 entrypoints-0.4 executing-1.2.0 fonttools-4.38.0 idna-3.4 
...
tweedledum-1.1.1 urllib3-1.26.13 wcwidth-0.2.5 websocket-client-1.4.2 websockets-10.4 widgetsnbextension-4.0.3
</pre>

Use `pip` to install the remaining required [PyPI](https://pypi.org/) packages, which are specified
in the file `minimal-requirements.txt`:

<pre>
(venv) $ <b>pip install -r minimal-requirements.txt</b>
Collecting qiskit-textbook@ git+https://github.com/qiskit-community/qiskit-textbook.git@7787075d0a02f7b6bacc2e624842902e1318621a#subdirectory=qiskit-textbook-src
  Using cached qiskit_textbook-0.1.0-py3-none-any.whl
Requirement already satisfied: appnope==0.1.3 in ./venv/lib/python3.8/site-packages (from -r minimal-requirements.txt (line 1)) (0.1.3)
Collecting asgiref==3.5.2
  Using cached asgiref-3.5.2-py3-none-any.whl (22 kB)
...
Successfully installed Django-4.0.6 Jinja2-3.1.2 MarkupSafe-2.1.1 PyYAML-6.0 asgiref-3.5.2 asttokens-2.1.0 attrs-22.1.0 backports.zoneinfo-0.2.1 certifi-2022.6.15 charset-normalizer-2.1.0 click-8.1.3 colorama-0.4.6 commonmark-0.9.1 coreapi-2.3.3 coreschema-0.0.4 cryptography-38.0.3 debugpy-1.6.3 djangorestframework-3.13.1 flake8-5.0.4 idna-3.3 importlib-resources-5.10.0 inflection-0.5.1 ipython-8.6.0 itypes-1.2.0 jedi-0.18.1 jsonpickle-2.2.0 jsonschema-4.17.0 jupyter_client-7.4.5 jupyter_core-5.0.0 lxml-4.9.1 mccabe-0.7.0 netqasm-0.12.2 numpy-1.22.4 pkgutil_resolve_name-1.3.10 prompt-toolkit-3.0.32 pyang-2.5.3 pycodestyle-2.9.1 pydantic-1.10.2 pyflakes-2.5.0 pylatexenc-2.10 pyrsistent-0.19.2 pytz-2022.1 qiskit-0.39.2 qiskit-terra-0.22.2 qlink-interface-1.0.0 qne-adk-0.1.0 retworkx-0.12.0 rich-12.6.0 ruamel.yaml-0.17.21 ruamel.yaml.clib-0.2.6 rustworkx-0.12.0 scipy-1.8.1 shellingham-1.5.0 sqlparse-0.4.2 stack-data-0.6.1 tabulate-0.9.0 traitlets-5.5.0 typer-0.7.0 typing_extensions-4.4.0 uritemplate-4.1.1 urllib3-1.26.11 zipp-3.11.0
</pre>

# Additional installation instructions for QNE-ADK related code

The minimal installation instructions described above are sufficient for downloading and viewing
all of the team Q-Harmonics code and for running all Qiskit related code.
If you also want to run the QNE-ADK related code you must follow the additional installation
instruction described in this chapter. You must follow the minimal installation instructions
before following the additional installation instructions.

**TODO** Finish the additional installation instructions
