from sys import exit


def read_dm(filename):
    print(f"Reading density matrix from {filename}")
    dir = "/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022"
    with open(f"{dir}/{filename}", "r") as f:
        producer = f.readline().strip()
        print(f"  Source: {producer}")
        production_time = f.readline().strip()
        print(f"  Production time: {production_time}")
        n = int(f.readline().strip())
        print(f"  N: {n}")
        value = int(f.readline().strip())
        print(f"  Value: {value}")
        swap = bool(f.readline().strip())
        print(f"  Swap: {swap}")
        dm = []
        for r in range(n):
            row = []
            for c in range(n):
                v = complex(f.readline().strip())
                row.append(v)
            dm.append(row)
        print(f"  Read {n}x{n} density matrix")
        return {
            "n": n,
            "value": value,
            "swap": swap,
            "dm": dm
        }


def diff_dm(n, dm1, dm2):
    diff = []
    for r in range(n):
        row = []
        for c in range(n):
            d = dm1[r][c] - dm2[r][c]
            row.append(d)
        diff.append(row)
    return diff


def transpose(n, m):
    transposed = []
    for r in range(n):
        row = []
        for c in range(n):
            row.append(m[c][r])
        transposed.append(row)
    return transposed


def print_matrix(name, m):
    print(f"\n{name}\n")
    for row in m:
        for value in row:
            r = value.real
            i = value.imag
            print(f"{r:>6.3f} {i:>6.3f}j   ", end="")
        print("")


qiskit = read_dm("qiskit_dm.txt")
qne = read_dm("qne_dm.txt")

if qiskit["n"] != qne["n"]:
    print("ERROR: Inconsistent n")
    exit(1)

if qiskit["value"] != qne["value"]:
    print("WARNING: Inconsistent value")

if qiskit["swap"] != qne["swap"]:
    print("WARNING: Inconsistent swap")

n = qiskit["n"]

qiskit_dm = qiskit["dm"]
transposed_qiskit_dm = transpose(n, qiskit_dm)

qne_dm = qne["dm"]

print_matrix("Qiskit Density Matrix", qiskit_dm)

print_matrix("QNE Density Matrix", qne_dm)

diff = diff_dm(n, qiskit_dm, qne_dm)
print_matrix("Difference Density Matrix: Qiskit vs QNE", diff)

diff = diff_dm(n, transposed_qiskit_dm, qne_dm)
print_matrix("Difference Density Matrix: transposed Qiskit vs QNE", diff)
