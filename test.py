matrix = [[1, 2, 3, 4, 99], [5, 6, 7, 8], [9, 10, 11, 12, 100, 101]]
transposed = []
for i in range(max(len(l) for l in matrix)):
    # the following 3 lines implement the nested listcomp
    transposed_row = []
    for row in matrix:
        try:
            transposed_row.append(row[i])
        except IndexError:
            pass
    transposed.append(transposed_row)

print(transposed)
