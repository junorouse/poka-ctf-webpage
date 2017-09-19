def calculate_hori_ver(arr, index):
    arr_len = len(arr)
    hori_ver_count = [0, 0]
    bingo_count = 0

    for i in range(arr_len):
        hori_ver_count[0] = hori_ver_count[0] + 1 if arr[index][i] else hori_ver_count[0]
        hori_ver_count[1] = hori_ver_count[1] + 1 if arr[i][index] else hori_ver_count[1]

    bingo_count = bingo_count + 1 if hori_ver_count[0] ==  arr_len else bingo_count
    bingo_count = bingo_count + 1 if hori_ver_count[1] == arr_len else bingo_count
    return bingo_count


def calculate_bingo(arr):
    # arr will be 5*5 25index
    arr_len = len(arr)

    diagonal_count = [0, 0]
    bingo_count = 0

    for i in range(arr_len):
        diagonal_count[0] = diagonal_count[0] + 1 if arr[i][i] else diagonal_count[0]
        diagonal_count[1] = diagonal_count[1] + 1 if arr[i][arr_len-i-1] else diagonal_count[1]
        bingo_count += calculate_hori_ver(arr, i)

    bingo_count = bingo_count + 1 if diagonal_count[0] ==  arr_len else bingo_count
    bingo_count = bingo_count + 1 if diagonal_count[1] == arr_len else bingo_count


    return bingo_count

test = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

print(calculate_bingo(test))