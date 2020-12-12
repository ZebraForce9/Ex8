def constraint_satisfactions(n, blocks):
    to_color = sum(blocks)
    options = []

    row = [0 for i in range(n)]

    constraint_helper(row, 0, blocks, 0, to_color, options)

    return options


def constraint_helper(row, row_index, blocks, block_index, to_color, options):
    if to_color == 0:
        options.append(row[:])
        return

    if row_index >= len(row) or block_index >= len(blocks):
        return

    block_length = blocks[block_index]

    for i in range(row_index, len(row)):

        if i + block_length > len(row):
            return

        row[i: i + block_length] = [1 for i in range(block_length)]
        to_color -= block_length
        block_index += 1

        constraint_helper(row, i + block_length + 1, blocks, block_index, to_color, options)

        row[i: i + block_length] = [0 for i in range(block_length)]
        to_color += block_length
        block_index -= 1


def row_variations(row, blocks):
    to_color = sum(blocks) - row.count(1)
    options = []
    row_copy = row[:]

    variations_helper(row, row_copy, 0, blocks, 0, to_color, options)

    return options


def variations_helper(row_original, row_copy, row_index, blocks, block_index, to_color, options):
    if to_color == 0:
        row_copy_copy = [0 if square == -1 or square == 0 else 1 for square in row_copy]

        options.append(row_copy_copy)
        return

    if row_index >= len(row_copy) or block_index >= len(blocks):
        return

    block_length = blocks[block_index]

    for i in range(row_index, len(row_copy)):

        if i + block_length > len(row_copy):
            return

        if not is_legal_coloring(i, row_copy, block_length):
            continue

        row_copy[i: i + block_length] = [1 for i in range(block_length)]
        to_color -= row_original[i: i + block_length].count(-1)
        block_index += 1

        variations_helper(row_original, row_copy, i + block_length + 1, blocks, block_index, to_color, options)

        row_copy[i: i + block_length] = row_original[i: i + block_length]
        to_color += row_original[i: i + block_length].count(-1)
        block_index -= 1


def is_legal_coloring(i, row_copy, block_length):
    if i + block_length < len(row_copy):
        if row_copy[i + block_length] == 1:
            return False

    if 0 in row_copy[i: i + block_length] or -1 not in row_copy[i: i + block_length]:
        return False

    return True
