#!/usr/bin/env python3
# assign.py : Assign students to groups to make the total time minimum
# Yingnan Ju, 2017 created


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
        self.preferred_group_size = size
        self.preferred_student_list = list(p_list)
        self.hate_student_list = list(h_list)


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

    # assigned group
    assigned_list = []
    # unassigned people list
    unassigned_list = []

    def __init__(self, assigned_list, unassigned_list):
        self.assigned_list.extend([list(group) for group in assigned_list])
        self.unassigned_list = list(unassigned_list)

    # set the parameter only one time
    # do not forget
    @staticmethod
    def set_parameter(k, n, m):
        Status.time_grade_group = k
        Status.time_no_preferred_email = n
        Status.time_hate_meeting = m

    def calculate_total_time(self):
        self.total_time = 0
