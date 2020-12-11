def constraint_satisfactions(n, blocks):
    to_color = sum(blocks)
    options = []

    line = [0 for i in range(n)]

    constraint_helper(blocks, 0, to_color, line, options, 0)

    return options


def constraint_helper(blocks, block_index, to_color, row, options, line_index):
    if to_color == 0:
        options.append(row[:])
        return

    if line_index >= len(row) or block_index > len(blocks):
        return

    block_length = blocks[block_index]

    for i in range(line_index, len(row)):
        if i + block_length > len(row):
            return
        row[i: i + block_length] = [1 for i in range(block_length)]
        to_color -= block_length
        block_index += 1

        constraint_helper(blocks, block_index, to_color, row, options, i + block_length + 1)

        row[i: i + block_length] = [0 for i in range(block_length)]
        to_color += block_length
        block_index -= 1


def row_variations(row, blocks):
    pass
