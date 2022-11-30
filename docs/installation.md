# Installation

This document contains the installation instructions for distribution quantum Fourier transform
project software developed by "team Q-Harmonics" as part of the
[Quantum Internet Hackathon (QIH) 2022](https://labs.ripe.net/author/karla-white/take-part-in-the-quantum-internet-hackathon-2022/)
.

These installation instructions have been tested on a MacBook Air running macOS Catalina, but
they should work with little or no changes on any other platform including Windows or Linux.

I assume you already have the following software installed on your computer.
On macOS I recommend `brew` to install this software if you don't already have it:
 * Python 3.8.x: Needed to run the Python code in the repo.
 * Pip: Needed to install [PyPI](https://pypi.org/) dependencies.
 * Git: Need to clone git repository from GitHub and work on it.
 * Some code editor: I use Visual Studio Code (VSC).
 * Some way to run Jupyter notebooks: I use the Microsoft Jupyter extension in Visual Studio Code.


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


Use `pip` to install the required [PyPI](https://pypi.org/) packages:

<pre>
(venv) $ <b>pip install -r minimal-requirements.txt</b>
Collecting certifi==2022.9.24
  Using cached certifi-2022.9.24-py3-none-any.whl (161 kB)
Collecting cffi==1.15.1
  Using cached cffi-1.15.1-cp38-cp38-macosx_10_9_x86_64.whl (178 kB)
...
Collecting websockets==10.4
  Using cached websockets-10.4-cp38-cp38-macosx_10_9_x86_64.whl (97 kB)
Building wheels for collected packages: qiskit
  Building wheel for qiskit (setup.py) ... done
  Created wheel for qiskit: filename=qiskit-0.39.3-py3-none-any.whl size=12245 sha256=24ce18ea4fa11a2f415bc17bfc1f02535c45e4e73bab1da13d356cd4732d9445
  Stored in directory: /Users/brunorijsman/Library/Caches/pip/wheels/ed/b2/74/9e8a20d11a6fc8b1b59cb16e73733e1cf14209a8f2b9b98abc
Successfully built qiskit
Installing collected packages: ply, mpmath, websockets, websocket-client, urllib3, tweedledum, sympy, symengine, six, pycparser, psutil, pbr, numpy, ntlm-auth, idna, dill, charset-normalizer, certifi, stevedore, scipy, rustworkx, requests, python-dateutil, cffi, retworkx, cryptography, requests-ntlm, qiskit-terra, qiskit-ibmq-provider, qiskit-aer, qiskit
Successfully installed certifi-2022.9.24 cffi-1.15.1 charset-normalizer-2.1.1 cryptography-38.0.4 dill-0.3.6 idna-3.4 mpmath-1.2.1 ntlm-auth-1.5.0 numpy-1.23.5 pbr-5.11.0 ply-3.11 psutil-5.9.4 pycparser-2.21 python-dateutil-2.8.2 qiskit-0.39.3 qiskit-aer-0.11.1 qiskit-ibmq-provider-0.19.2 qiskit-terra-0.22.3 requests-2.28.1 requests-ntlm-1.1.0 retworkx-0.12.1 rustworkx-0.12.1 scipy-1.9.3 six-1.16.0 stevedore-4.1.1 symengine-0.9.2 sympy-1.11.1 tweedledum-1.1.1 urllib3-1.26.13 websocket-client-1.4.2 websockets-10.4
</pre>

# Additional installation instructions for QNE-ADK related code

The minimal installation instructions described above are sufficient for downloading and viewing
all of the team Q-Harmonics code and for running all Qiskit related code.
If you also want to run the QNE-ADK related code you must follow the additional installation
instruction described in this chapter. You must follow the minimal installation instructions
before following the additional installation instructions.

TODO Finish the additional installation instructions
