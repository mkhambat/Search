#!/usr/bin/env python3
# solver16.py : Solve the 16 numbers problem when multiple tiles can move
# Yingnan Ju, 2017 created
#

import sys
import math
import copy


def enum(**enums):
    return type('Enum', (), enums)


Directions = enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, NONE=4)

board_end = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]


# board_end = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
# board_end = [['1', '2'], ['3', '0']]

class Status:
    board = []
    previous = Directions.NONE
    count = 0
    manhattan = 0
    misplace = 0
    linear_conflict = 0
    priority_manhattan = 0
    priority_misplace = 0
    priority_linear_conflict = 0
    priority = 0
    solution = []

    def __init__(self, board, count, solution):
        self.board = copy.deepcopy(board)
        self.count = count
        self.solution = list(solution)
        self.update_linear_priority(board_end)
        # self.update_manhattan(board_end)
        # self.update_misplace(board_end)

    def exchange(self, coordinate1, coordinate2):
        self.board[coordinate1[0]][coordinate1[1]], self.board[coordinate2[0]][coordinate2[1]] = \
            self.board[coordinate2[0]][coordinate2[1]], self.board[coordinate1[0]][coordinate1[1]]
        self.count += 1
        self.update_linear_priority(board_end)
        # self.update_manhattan(board_end)
        # self.update_misplace(board_end)

    def set_previous(self, direction):
        self.previous = direction
        self.solution.append(self.previous)

    def update_misplace(self, board_to_compare):
        self.misplace = compare_board_misplace(self.board, board_to_compare)
        self.update_priority()

    def update_manhattan(self, board_to_compare):
        self.manhattan = compare_board_manhattan(self.board, board_to_compare)
        self.update_priority()

    def update_linear_priority(self, board_to_compare):
        self.linear_conflict = compare_board_linear_conflict_horizontal(self.board, board_to_compare) + \
                               compare_board_linear_conflict_vertical(self.board, board_to_compare)
        self.update_manhattan(board_to_compare)

    def update_priority(self):
        self.priority_manhattan = self.count + self.manhattan
        self.priority_misplace = self.count + self.misplace
        self.priority_linear_conflict = self.priority_manhattan + self.linear_conflict * 2
        self.priority = self.priority_linear_conflict

    def print_info(self):
        print("Count=", self.count, \
              " Manhattan=", self.manhattan, " priority1=", self.priority_manhattan, \
              " Misplace=", self.misplace, " priority2=", self.priority_misplace, \
              " linear Conflict=", self.linear_conflict, " priority3=", self.priority_linear_conflict)

    def print_solution(self):
        print(self.solution)

    def print_all(self):
        print(printable_board(self.board))
        self.print_info()
        self.print_solution()


# read the input file for initial status
def read_file(file_path):
    file = open(file_path, 'r')
    line = "initial"
    board = []
    while line:
        line = file.readline()
        if len(line) > 0:
            line_split = line.split()
            board.append(line_split)
    return board


def find_coordinate(tile, board):
    for row in board:
        for col in row:
            if tile == col:
                return (board.index(row), row.index(col))
    return None


def solvable(board):
    flat_board = []
    for row in board:
        flat_board.extend(row)
    sum = 0
    for i in flat_board:
        for j in flat_board[0:flat_board.index(i)]:
            if j > i and i != '0':
                sum += 1
    return sum % 2


def calculate_manhattan_distance(coordinate1, coordinate2):
    return math.fabs(coordinate1[0] - coordinate2[0]) + math.fabs(coordinate1[1] - coordinate2[1])


# compare two boards
# by manhattan distance?
def compare_board_manhattan(board1, board2):
    sum = 0
    for row in board1:
        for col in row:
            coordinate1 = find_coordinate(col, board1)
            coordinate2 = find_coordinate(col, board2)
            sum += calculate_manhattan_distance(coordinate1, coordinate2)
    return sum


# compare two boards
# by misplace tiles
def compare_board_misplace(board1, board2):
    sum = 0
    for row in board1:
        for col in row:
            if col != board2[board1.index(row)][row.index(col)]:
                sum += 1
    return sum


# compare two boards
# by misplace tiles
def compare_board_linear_conflict_horizontal(board1, board2):
    sum = 0
    for i in range(0, len(board1)):
        for j in range(0, len(board1[i])):
            for k in range(j + 1, len(board1[i])):
                if board1[i][j] in board2[i] \
                        and board1[i][k] in board2[i] \
                        and board2[i].index(board1[i][j]) > board2[i].index(board1[i][k]):
                    sum += 1
    return sum


# compare two boards
# by misplace tiles
def compare_board_linear_conflict_vertical(board1, board2):
    board3 = [[row[i] for row in board1] for i in range(len(board1[0]))]
    board4 = [[row[i] for row in board2] for i in range(len(board2[0]))]
    return compare_board_linear_conflict_horizontal(board3, board4)


def is_goal(board1):
    return is_same(board1, board_end)


def is_same(board1, board2):
    if len(board1) != len(board2):
        return False
    return False \
        if any(board1[r][c] != board2[r][c] for r in range(len(board1)) for c in range(len(board[r]))) \
        else True


def find_next(fringe):
    min = 9999999
    index = 0
    for status in fringe:
        # '<=' time less than '<', maybe 40% less
        if status.priority <= min:
            min = status.priority
            index = fringe.index(status)
    return index


def find_successors(status):
    successors = []
    coordinate_empty = find_coordinate('0', status.board)
    upper_limit = len(status.board)
    successor_coordinates = [(coordinate_empty[0] - 1, coordinate_empty[1]), \
                             (coordinate_empty[0] + 1, coordinate_empty[1]), \
                             (coordinate_empty[0], coordinate_empty[1] - 1), \
                             (coordinate_empty[0], coordinate_empty[1] + 1)]

    for coordinate in successor_coordinates:
        direction = successor_coordinates.index(coordinate)
        if coordinate[0] >= 0 \
                and coordinate[1] >= 0 \
                and coordinate[0] < upper_limit \
                and coordinate[1] < upper_limit:
            new_status = Status(status.board, status.count, status.solution)
            new_status.exchange(coordinate, coordinate_empty)
            new_status.set_previous(direction)
            successors.append(new_status)
    return successors


# make board in printable in a matrix
def printable_board(board):
    return "\n".join([" ".join([col for col in row]) for row in board])


def solve(initial_status):
    fringe = [initial_status]
    closed = []
    while len(fringe) > 0:
        index = find_next(fringe)
        next = fringe.pop(index)
        # next.print_all()
        if is_goal(next.board):
            next.print_all()
            return next
        closed.append(next.board)
        for s in find_successors(next):
            is_in_closed = False
            for c in closed:
                if is_same(s.board, c):
                    is_in_closed = True
                    break
            is_in_fringe = False
            if not is_in_closed:
                for open in fringe:
                    if is_same(s.board, open.board):
                        is_in_fringe = True
                        if s.priority < open.priority:
                            fringe.remove(open)
                            is_in_fringe = False
                        break
                if not is_in_fringe:
                    fringe.append(s)
                    # closed.append(s.board)
    return False


# Main
file_path = sys.argv[1] if sys.argv.__len__() > 1 else None
board = read_file(file_path)
initial_status = Status(board, 0, [])

import time

start = time.time()
if solvable(board) == solvable(board_end):
    solve(initial_status)
else:
    print("No solution.")
end = time.time()
print(end - start)
