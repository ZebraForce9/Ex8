def constraint_satisfactions(n, blocks):
    to_color = sum(blocks)
    options = []

    line = [0 for i in range(n)]

    helper(to_color, line, options, 0)

    return options


def helper(to_color, line, options, index):
    if to_color == 0:
        options.append(line[:])
        return

    for i in range(len(line)):
        line[i] = 1
        to_color -= 1
        helper(to_color, line, options, index + 2)
        line[i] = 0
        to_color += 1


print(constraint_satisfactions(3, [1]))
