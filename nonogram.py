from copy import deepcopy

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


def legal_row(row, blocks):
    if blocks:
        largest_block = max(blocks)
        count = 0

        for square in row:
            if square == 1:
                count += 1
                if count > largest_block:
                    return False
            else:
                count = 0
    return True


def row_variations(row, blocks):
    to_color = sum(blocks)
    options = []
    row_copy = row[:]

    if legal_row(row, blocks):
        variations_helper(row, row_copy, 0, blocks, 0, to_color, options)

    return options


def variations_helper(row_original, row_copy, row_index, blocks, block_index, to_color, options):

    if check_to_color(to_color, row_copy, row_index, blocks, block_index, options):
        return

    block_length = blocks[block_index]

    for i in range(row_index, len(row_copy)):

        if i + block_length > len(row_copy):
            return

        if not is_legal_coloring(i, row_copy, block_length):
            continue

        row_copy[i: i + block_length] = [1 for i in range(block_length)]
        to_color -= block_length
        block_index += 1

        variations_helper(row_original, row_copy, i + block_length + 1, blocks, block_index, to_color, options)

        row_copy[i: i + block_length] = row_original[i: i + block_length]
        to_color += block_length
        block_index -= 1


def is_legal_coloring(i, row_copy, block_length):
    if i + block_length < len(row_copy):
        if row_copy[i + block_length] == 1:
            return False

    if i > 0:
        if row_copy[i - 1] == 1:
            return False

    if 0 in row_copy[i: i + block_length]:
        return False

    return True


def check_to_color(to_color, row_copy, row_index, blocks, block_index, options):
    if to_color == 0:
        if block_index == len(blocks) and row_copy.count(1) == sum(blocks):
            row_copy_copy = [0 if square == -1 or square == 0 else 1 for square in row_copy]

            options.append(row_copy_copy)
        return True

    if to_color < 0:
        return True

    elif row_index >= len(row_copy) or block_index >= len(blocks):
        return True


def intersection_row(rows):
    square_intersection = zip(*rows)
    row_intersection = []

    for square in square_intersection:
        first = square[0]
        for i in range(1, len(square)):
            if square[i] != first:
                row_intersection.append(-1)
                break
        else:
            row_intersection.append(first)

    return row_intersection


def solve_easy_nonogram(constraints):
    board, col_constraints, row_constraints, unknown_count = initialize_game(constraints)

    while unknown_count > 0:
        changed = False

        for col_ind, constraint in enumerate(col_constraints):
            col = make_col(col_ind, board)
            col_options = row_variations(col, constraint)
            col_intersection = intersection_row(col_options)
            if not col_intersection:
                return

            for row_ind, (square1, square2) in enumerate(zip(col, col_intersection)):
                if square1 == -1 and square1 != square2:
                    board[row_ind][col_ind] = square2
                    unknown_count -= 1
                    changed = True

        if unknown_count == 0 or changed is False:
            break

        for row_ind, (row, constraint) in enumerate(zip(board, row_constraints)):
            row_options = row_variations(row, constraint)
            row_intersection = intersection_row(row_options)
            if not row_intersection:
                return

            for col_ind, (square1, square2) in enumerate(zip(row, row_intersection)):
                if square1 == -1 and square1 != square2:
                    board[row_ind][col_ind] = square2
                    unknown_count -= 1
                    changed = True

            if changed is False:
                break

    return board


def initialize_game(constraints):
    row_constraints = constraints[0]
    col_constraints = constraints[1]
    board = []
    row_length = len(constraints[1])
    unknown_count = 0
    for constraint in row_constraints:
        row_options = constraint_satisfactions(row_length, constraint)
        row_intersection = intersection_row(row_options)
        board.append(row_intersection)
        unknown_count += row_intersection.count(-1)
    return board, col_constraints, row_constraints, unknown_count


def solve_nonogram(constraints):
    row_constraints = constraints[0]
    col_constraints = constraints[1]
    solutions = []
    board = solve_easy_nonogram(constraints)
    row_length = len(board[0])
    solve_nonogram_helper(board, row_constraints, col_constraints, solutions, row_length)

    return solutions


def solve_nonogram_helper(board, row_constraints, col_constraints, solutions, row_length):
    col_index = find_col_index(board)

    if col_index == row_length:
        board_copy = deepcopy(board)
        solutions.append(board_copy)
        return

    col = make_col(col_index, board)
    col_variations = row_variations(col, col_constraints[col_index])
    for variation in col_variations:
        insert_col(board, col_index, variation)
        if check_rows(board, row_constraints):
            solve_nonogram_helper(board, row_constraints, col_constraints, solutions, row_length)
        insert_col(board, col_index, col)


def check_rows(board, row_constraints):
    for i, row in enumerate(board):
        if not row_variations(row, row_constraints[i]):
            return False
    return True


def insert_col(board, col_index, variation):
    for row_index, square in enumerate(variation):
        board[row_index][col_index] = square


def make_col(col_index, board):
    col = [row[col_index] for row in board]
    return col


def find_col_index(board):
    lowest_index = len(board[0])

    for row in board:
        for i, square in enumerate(row):
            if square == -1 and i < lowest_index:
                lowest_index = i
    return lowest_index





