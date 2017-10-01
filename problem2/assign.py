#!/usr/bin/env python3
# assign.py : Assign students to groups to make the total time minimum
# Yingnan Ju, 2017 created

import math
import sys


class Student:
    # student name
    name = ""
    # the group size that the student prefers
    preferred_group_size = 0
    # the student list that the student prefers
    preferred_student_list = []
    # the student list that the student prefers not to be with
    hate_student_list = []

    def __init__(self, name, size, p_list, h_list):
        self.name = name
        self.preferred_group_size = int(size)
        self.preferred_student_list = list(p_list)
        self.hate_student_list = list(h_list)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Status:
    # time to grade each group, also known as k
    # "They need k minutes to grade each assignment, so total grading time is k times number of teams."
    time_grade_group = 0
    # time to read and reply a email when student not in a preferred group size
    # "Each student who requested a specific group size and was assigned to a different group size will
    # complain to the instructor after class, taking 1 minute of the instructor's time."
    # this value is fixed, for now
    time_size_email = 1
    # time to read and reply a email when student not grouped with another preferred student, also known as n
    # "Each student who is not assigned to someone they requested will send a complaint email, which
    # will take n minutes for the instructor to read and respond. If a student requested to work with
    # multiple people, then they will send a separate email for each person they were not assigned to."
    time_no_preferred_email = 0
    # time for a meeting when student is grouped with a dislike student, also known as m
    # "Each student who is assigned to someone they requested not to work with (in question 4 above)
    # will request a meeting with the instructor to complain, and each meeting will last m minutes. If
    # a student requested not to work with two specific students and is assigned to a group with both
    # of them, then they will request 2 meetings."
    time_hate_meeting = 0

    # total time
    # "The total time spent by the course staff is equal to the sum of these components."
    total_time = 0

    least_possible_time = 0

    # assigned group
    assigned_list = []
    assigned_count = 0
    # unassigned people list
    unassigned_list = []

    def __init__(self, assigned_list, unassigned_list):
        self.assigned_list = []
        for group in assigned_list:
            self.assigned_list.append(list(group))
        self.unassigned_list = list(unassigned_list)
        # self.calculate_total_time()

    # set the parameter only one time
    # do not forget
    @staticmethod
    def set_parameter(k, n, m):
        Status.time_grade_group = k
        Status.time_no_preferred_email = n
        Status.time_hate_meeting = m

    def calculate_total_time(self):
        self.total_time = len(self.assigned_list) * Status.time_grade_group
        for group in self.assigned_list:
            for student in group:
                if student.preferred_group_size != 0 and student.preferred_group_size != len(group):
                    self.total_time += Status.time_size_email
                    # self.least_possible_time += Status.time_size_email \
                    # if len(group) > student.preferred_group_size else 0
                for preferred_student in student.preferred_student_list:
                    if preferred_student not in list(student.name for student in group):
                        self.total_time += self.time_no_preferred_email
                        # self.least_possible_time += self.time_no_preferred_email \
                        # if preferred_student not in list(student.name for student in self.unassigned_list) else 0
                for hate_student in student.hate_student_list:
                    if hate_student in list(student.name for student in group):
                        self.total_time += self.time_hate_meeting
                        # self.least_possible_time += self.time_hate_meeting
        self.least_possible_time = self.total_time
        self.least_possible_time += math.ceil(len(self.unassigned_list) / 3)

    def calculate_total_time_old(self):
        self.total_time = len(self.assigned_list) * Status.time_grade_group
        least_possible_group_count = math.ceil((self.assigned_count + len(self.unassigned_list)) / 3)
        self.least_possible_time = least_possible_group_count * Status.time_grade_group
        for group in self.assigned_list:
            for student in group:
                if student.preferred_group_size != 0 and student.preferred_group_size != len(group):
                    self.total_time += Status.time_size_email
                    self.least_possible_time += Status.time_size_email \
                        if len(group) > student.preferred_group_size else 0
                for preferred_student in student.preferred_student_list:
                    if preferred_student not in list(student.name for student in group):
                        self.total_time += self.time_no_preferred_email
                        self.least_possible_time += self.time_no_preferred_email \
                            if preferred_student not in list(student.name for student in self.unassigned_list) else 0
                for hate_student in student.hate_student_list:
                    if hate_student in list(student.name for student in group):
                        self.total_time += self.time_hate_meeting
                        self.least_possible_time += self.time_hate_meeting

    def assign_student(self, group_index):
        if len(self.unassigned_list) > 0:
            if group_index < len(self.assigned_list):
                if len(self.assigned_list[group_index]) < 3:
                    self.assigned_list[group_index].append(self.unassigned_list.pop(0))
                else:
                    return False
            else:
                self.assigned_list.append([self.unassigned_list.pop(0)])
            self.calculate_total_time()
            return True
        else:
            return False

    def print_status(self):
        print(self.assigned_list, self.total_time)


# read the input file for initial status
def read_file(path):
    file = open(path, 'r')
    line = "initial"
    student_list = []
    while line:
        line = file.readline()
        if len(line) > 0:
            line_split = line.split()
            name = line_split[0]
            preferred_size = int(line_split[1])
            preferred_list = line_split[2].split(',') if line_split[2] != '_' else []
            hate_list = line_split[3].split(',') if line_split[2] != '_' else []
            student_list.append(Student(name, preferred_size, preferred_list, hate_list))
    return student_list


def is_goal(status):
    return len(status.unassigned_list) == 0


def find_successors(status):
    successors = []
    for i in range(0, len(status.assigned_list) + 1):
        new_status = Status(status.assigned_list, status.unassigned_list)
        is_assigned = new_status.assign_student(i)
        successors.append(new_status) if is_assigned else None
    return successors


def find_next(collection):
    temp_min = 999999
    index = 0
    for item in collection:
        if item.least_possible_time < temp_min:
            temp_min = item.least_possible_time
            index = collection.index(item)
    return index


def solve(status):
    # initial fringe and closed
    fringe = [status]
    while len(fringe) > 0:
        for s in find_successors(fringe.pop()):
            if is_goal(s):
                return s
            fringe.append(s)
            fringe.sort(key=lambda student: student.least_possible_time, reverse=True)
    return False


def solve_old(status):
    # initial fringe and closed
    fringe = [status]
    possible_goal = None
    while len(fringe) > 0:
        # print([state.least_possible_time for state in fringe])
        index = find_next(fringe)
        next_status = fringe.pop(index)
        if is_goal(next_status):
            if possible_goal is None or possible_goal.total_time > next_status.total_time:
                possible_goal = next_status
            if len(fringe) == 0 or possible_goal.total_time <= fringe[-1].least_possible_time:
                return possible_goal
        for s in find_successors(next_status):
            fringe.append(s)
            # fringe.sort(key=lambda student: student.least_possible_time, reverse=True)
    return possible_goal


def full_solve(status):
    # initial fringe and closed
    fringe = [status]
    possible_goal = None
    while len(fringe) > 0:
        print([state.least_possible_time for state in fringe])
        for s in find_successors(fringe.pop()):
            # s.print_status()
            if is_goal(s):
                if possible_goal is None or possible_goal.total_time > s.total_time:
                    possible_goal = s
            fringe.append(s)
    return possible_goal


# Main
#  get file path from argv
file_path = sys.argv[1] if sys.argv.__len__() > 1 else None
# read time parameter from argv
time_grade = int(sys.argv[2]) if sys.argv.__len__() > 2 else 1
time_preferred_email = int(sys.argv[4]) if sys.argv.__len__() > 4 else 1
time_hate_meeting = int(sys.argv[3]) if sys.argv.__len__() > 3 else 1
# read the file
full_student_list = read_file(file_path)
# set status time, static
Status.set_parameter(time_grade, time_preferred_email, time_hate_meeting)
# get the initial status
initial_status = Status([], full_student_list)
solution = solve(initial_status)
solution.print_status()
