def constraint_satisfactions(n, blocks):
    to_color = sum(blocks)
    options = []

    line = [0 for i in range(n)]

    helper(blocks, 0, to_color, line, options, 0)

    return options


def helper(blocks, block_index, to_color, line, options, line_index):
    if to_color == 0:
        options.append(line[:])
        return

    if line_index >= len(line) or block_index > len(blocks):
        return

    block_length = blocks[block_index]

    for i in range(line_index, len(line)):
        if i + block_length > len(line):
            return
        line[i: i + block_length] = [1 for i in range(block_length)]
        to_color -= block_length
        block_index += 1
        helper(blocks, block_index, to_color, line, options, i + 2)
        block_index -= 1
        line[i: i + block_length] = [0 for i in range(block_length)]
        to_color += block_length

print(constraint_satisfactions(2, [1]))