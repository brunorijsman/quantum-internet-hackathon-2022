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

```
git clone https://github.com/brunorijsman/quantum-internet-hackathon-2022.git
```

In the remainder of these installation instructions, I will use the `QIH_2022_ROOT` environment
variable to refer to the directory in which you cloned the repository:

```
export QIH_2022_ROOT=$(pwd)
```


## Create and activate a Python virtual environment

Change directory to the newly created local clone:

```
cd ${QIH_2022_ROOT}/quantum-internet-hackathon-2022
```


Create a Python virtual environment:

```
python3.8 -m venv venv
```

<b>Note:</b>You must use Python3.8.x. QNE-ADK does not yet work with Python3.9.x or later.
I have not tested with Python 3.7.x or earlier. I recommend using `brew` to install Python 3.8 on
your Mac and using `pyenv` for making Python3.8 the default Python version for this project.

Activate the virtual environment:

```
source venv/bin/activate
```

<b>Note:</b> Every time you open a new shell or new terminal window, you must activate the
virtual environment. Your command-line prompt includes `(venv)` when the virtual environment is
active.

## Install the dependencies

Upgrade `pip` to the latest version:

```
pip install --upgrade pip
```

Install the `wheel` package:

```
pip install wheel
```

Install the Qiskit textbook package:

```
pip install git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src
```

Install the remaining required [PyPI](https://pypi.org/) packages, which are specified
in the file `minimal-requirements.txt`:

```
pip install -r minimal-requirements.txt
```

# Additional installation instructions for QNE-ADK related code

The minimal installation instructions described above are sufficient for downloading and viewing
all of the team Q-Harmonics code and for running all Qiskit related code.

If you also want to run the QNE-ADK related code you must follow the additional installation steps
listed below (make sure you execute the basic installation steps listed above first).

Install the Quantum Network Explorer Application Development Kit (QNE-ADK):

```
pip install qne-adk
```


**TODO** Finish the additional installation instructions
