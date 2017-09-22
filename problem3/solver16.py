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


class Status:
    board = []
    previous = Directions.NONE
    count = 0
    manhattan = 0
    priority = 0

    def __init__(self, board, count):
        self.board = copy.deepcopy(board)
        self.count = count
        self.update_manhattan(board_end)

    def exchange(self, coordinate1, coordinate2):
        self.board[coordinate1[0]][coordinate1[1]], self.board[coordinate2[0]][coordinate2[1]] = \
            self.board[coordinate2[0]][coordinate2[1]], self.board[coordinate1[0]][coordinate1[1]]
        self.count += 1
        self.update_manhattan(board_end)

    def set_previous(self, direction):
        self.previous = direction

    def update_manhattan(self, board_to_compare):
        self.manhattan = compare_board(self.board, board_to_compare)
        self.update_priority()

    def update_priority(self):
        self.priority = self.count + self.manhattan

    def print_info(self):
        print("Count=", self.count, " Manhattan=", self.manhattan, " priority=", self.priority)

    def print_all(self):
        print(printable_board(self.board))
        self.print_info()


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


def calculate_manhattan_distance(coordinate1, coordinate2):
    return math.fabs(coordinate1[0] - coordinate2[0]) + math.fabs(coordinate1[1] - coordinate2[1])


# compare two boards
# by manhattan distance?
def compare_board(board1, board2):
    sum = 0
    for row in board1:
        for col in row:
            coordinate1 = find_coordinate(col, board1)
            coordinate2 = find_coordinate(col, board2)
            sum += calculate_manhattan_distance(coordinate1, coordinate2)
    return sum


def is_goal(board1, board2):
    return True if compare_board(board1, board2) == 0 else False


def is_same(board1, board2):
    if len(board1) != len(board2):
        return False
    for r in range(0, len(board1)):
        for c in range(0, len(board[r])):
            if board1[r][c] != board2[r][c]:
                return False
    return True


def find_next(fringe):
    min = 9999999
    index = 0
    for status in fringe:
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
        if status.previous != direction:
            if coordinate[0] >= 0 \
                    and coordinate[1] >= 0 \
                    and coordinate[0] < upper_limit \
                    and coordinate[1] < upper_limit:
                new_status = Status(status.board, status.count)
                new_status.exchange(coordinate, coordinate_empty)
                new_status.set_previous(direction)
                successors.append(new_status)
    return successors


# make board in printable in a matrix
def printable_board(board):
    return "\n".join([" ".join([col for col in row]) for row in board])


def solve(initial_status):
    fringe = [initial_status]
    closed = [initial_status.board]
    while len(fringe) > 0:
        index = find_next(fringe)
        # print(printable_board(fringe[index].board))
        # print(index,"/",len(fringe))
        next = fringe.pop(index)
        next.print_all()
        closed.append(next.board)
        for s in find_successors(next):
            if is_goal(s.board, board_end):
                print(printable_board(s.board))
                return s
            is_in_closed = False
            for c in closed:
                if is_same(s.board, c):
                    is_in_closed = True
                    break
            if not is_in_closed:
                fringe.append(s)
                closed.append(s.board)
    return False


# Main
file_path = sys.argv[1] if sys.argv.__len__() > 1 else None
board = read_file(file_path)
initial_status = Status(board, 0)
# board_end_state = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]

# board_end_state = [['1', '2'], ['3', '0']]
solve(initial_status)
