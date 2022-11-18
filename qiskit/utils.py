def reverse_bit_order(nr_bits, value):
    reversed_value = 0
    for _ in range(nr_bits):
        bit = value & 1
        value >>= 1
        reversed_value <<= 1
        reversed_value |= bit
    return reversed_value


def dm_reverse_bit_order(nr_qubits, dm):
    dm_size = nr_qubits ** 2
    reversed_dm = []
    for row_index in range(dm_size):
        row = []
        for column_index in range(dm_size):
            reversed_row_index = reverse_bit_order(nr_qubits, row_index)
            reversed_column_index = reverse_bit_order(nr_qubits, column_index)
            value = dm[reversed_row_index][reversed_column_index]
            row.append(value)
        reversed_dm.append(row)
    return reversed_dm


def pretty_print_dm(nr_qubits, dm):
    dm_size = nr_qubits ** 2
    for r in range(dm_size):
        for c in range(dm_size):
            value = dm[r][c]
            rv = value.real
            iv = value.imag
            print(f"{rv:>6.3f} {iv:>6.3f}j    ", end="")
        print()
