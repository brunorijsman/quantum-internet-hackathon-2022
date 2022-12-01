# Running the distributed quantum Fourier transformation implemented in QNE-ADK

This is just a minimal place holder so that everyone can try running a basic QNE-ADK program.

I am assuming that the environment variable `QIH_2022_ROOT` is set to the 
directory where we cloned our repositories (see the
[installation instructions](docs/installation.md)
for details).

Change the directory to the `quantum-internet-hackathon-2022/qne_adk` repository directory:

```
cd $QIH_2022_ROOT/quantum-internet-hackathon-2022
```

If you have not already activated your virtual environment do so now:

```
source venv/bin/activate
```

Change into the `qne_adk` directory:

```
cd qne_adk
```

Run the `qft` application (in this case I am including the output so that you know what to expect):

<pre>
$ <b>./run.sh qft</b>
Cleaning qft...
Running qft...
qne experiment create qft_experiment qft randstad
Experiment run successfully. Check the results using command 'experiment results'
Results:
[
  {
    "app_qft": {
      "n": 3,
      "value": 1
    }
  }
]
Logs:
qft_app_log.yaml:
  LOG: qft starts
  LOG: n=3
  LOG: value=1
  LOG: qft creates register of 3 qubits
  LOG: apply qft
  LOG: apply qft value n=3 value=1
  LOG: bit 0 = 1
  LOG: X gate qubit 0
  LOG: bit 1 = 0
  LOG: bit 2 = 0
  LOG: apply qft rotations n=3
  LOG: hadamard qubit 2
  LOG: controlled phase control qubit 0 and target qubit 2 by angle pi/4
  LOG: controlled phase control qubit 1 and target qubit 2 by angle pi/2
  LOG: apply qft rotations n=2
  LOG: hadamard qubit 1
  LOG: controlled phase control qubit 0 and target qubit 1 by angle pi/2
  LOG: apply qft rotations n=1
  LOG: hadamard qubit 0
  LOG: apply qft swaps
  LOG: swap qubit 0 with qubit 2 (XXX not implemented)
  LOG: "density matrix for qubit 2 = [[ 1.25000000e-01+0.j          8.83883476e-02-0.08838835j\n
    \ -1.25000000e-01+0.j         -8.83883476e-02+0.08838835j\n   2.08166817e-17-0.125j
    \     -8.83883476e-02-0.08838835j\n  -2.08166817e-17+0.125j       8.83883476e-02+0.08838835j]\n
    [ 8.83883476e-02+0.08838835j  1.25000000e-01+0.j\n  -8.83883476e-02-0.08838835j
    -1.25000000e-01+0.j\n   8.83883476e-02-0.08838835j  2.08166817e-17-0.125j\n  -8.83883476e-02+0.08838835j
    -2.08166817e-17+0.125j     ]\n [-1.25000000e-01+0.j         -8.83883476e-02+0.08838835j\n
    \  1.25000000e-01+0.j          8.83883476e-02-0.08838835j\n  -2.08166817e-17+0.125j
    \      8.83883476e-02+0.08838835j\n   2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j]\n
    [-8.83883476e-02-0.08838835j -1.25000000e-01+0.j\n   8.83883476e-02+0.08838835j
    \ 1.25000000e-01+0.j\n  -8.83883476e-02+0.08838835j -2.08166817e-17+0.125j\n   8.83883476e-02-0.08838835j
    \ 2.08166817e-17-0.125j     ]\n [ 2.08166817e-17+0.125j       8.83883476e-02+0.08838835j\n
    \ -2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j\n   1.25000000e-01+0.j
    \         8.83883476e-02-0.08838835j\n  -1.25000000e-01+0.j         -8.83883476e-02+0.08838835j]\n
    [-8.83883476e-02+0.08838835j  2.08166817e-17+0.125j\n   8.83883476e-02-0.08838835j
    -2.08166817e-17-0.125j\n   8.83883476e-02+0.08838835j  1.25000000e-01+0.j\n  -8.83883476e-02-0.08838835j
    -1.25000000e-01+0.j        ]\n [-2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j\n
    \  2.08166817e-17+0.125j       8.83883476e-02+0.08838835j\n  -1.25000000e-01+0.j
    \        -8.83883476e-02+0.08838835j\n   1.25000000e-01+0.j          8.83883476e-02-0.08838835j]\n
    [ 8.83883476e-02-0.08838835j -2.08166817e-17-0.125j\n  -8.83883476e-02+0.08838835j
    \ 2.08166817e-17+0.125j\n  -8.83883476e-02-0.08838835j -1.25000000e-01+0.j\n   8.83883476e-02+0.08838835j
    \ 1.25000000e-01+0.j        ]]"
  LOG: writing density matrix to qne_dm.txt
  LOG: qft ends
</pre>