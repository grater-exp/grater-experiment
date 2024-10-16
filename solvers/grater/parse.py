from collections import OrderedDict

import csv
import numpy as np
import os
import sys
import re
import time
import z3
import pandas as pd
import argparse

# error code -1: not supported
# error code -2: error


sys.setrecursionlimit(3000) # to escape from RecursionError: maximum recursion depth exceeded while calling a Python object
EPSILON = np.finfo(float).tiny
EPSILON = ' ( 1e-50 ) '
MAXIMUM = np.finfo(float).max
MINIMUM = sys.float_info.min

need_further_process_type = ['to_fp', 'fp', 'fp.div', 'fp.mul', 'fp.add', 'fp.sub', 'fp.fma', 'fp.rem', 'fp.abs',
                             'fp.max', 'fp.min', 'fp.neg']
cannot_handle = ['fp.roundToIntegral', 'fp.sqrt', 'NaN', '+oo', '-oo', 'fp.isInfinite', 'distinct', 'fp.isNaN', '=>', 'fp.isZero', 'fpIsNormal', 'fpIsSubnormal', 'if', 'ite'] # => Implies
pattern_for_variable = '\w+'
pattern_for_num = '\d+'
pattern_for_fpFP = 'fpFP\\(\\d+, \\d+, \\d+\\)'
characters = ['(', ')', ',', '**', '+', '-', '*', '/', '>', '<', '>=', '<=', '=', 'and', '#or#'] # '#or#' is a special label


def process_fpref_node(node):
    s = ''
    if node is None or isinstance(node, z3.z3.FPRMRef):
        return False, ''
    elif node.decl().name() == 'to_fp':
        child_len = len(node.children())
        if child_len == 1:
            # print(f'\033[31m Error!. FPRef\'s only has one child: {node.children()}\033[0m')
            # exit(-2)
            if node.children()[0].decl().name() in need_further_process_type:
                flag, s = process_fpref_node(node.children()[0])
                return flag, s
            else:
                return True, str(node.children()[0])
        elif child_len == 2:
            if node.children()[1].decl().name() in need_further_process_type:
                flag, s = process_fpref_node(node.children()[1])
                return flag, s
            else:
                return True, str(node.children()[1])
        else:
            print(f'Not supported. FPRef\'s children:{node.children()}')
            return False, ''
            exit(-1)
    elif node.decl().name() == 'fp':
        num_node = z3.simplify(z3.fpToReal(node))
        # num_node = z3.simplify(node)
        s = str(num_node)
        return True, s
    elif node.decl().name() == 'fp.div':
        for one in node.children():
            flag, return_s = process_fpref_node(one)
            if flag:
                s += ' / ' + return_s
        return True, ' ( ' + s[3:] + ' ) '
    elif node.decl().name() == 'fp.mul':
        for one in node.children():
            flag, return_s = process_fpref_node(one)
            if flag:
                s += ' * ' + return_s
        return True, ' ( ' + s[3:] + ' ) '
    elif node.decl().name() == 'fp.add':
        for one in node.children():
            flag, return_s = process_fpref_node(one)
            if flag:
                s += ' + ' + return_s
        return True, ' ( ' + s[3:] + ' ) '
    elif node.decl().name() == 'fp.sub':
        for one in node.children():
            flag, return_s = process_fpref_node(one)
            if flag:
                s += ' - ' + return_s
        return True, ' ( ' + s[3:] + ' ) '
    elif node.decl().name() == 'fp.neg':
        flag, s = process_fpref_node(node.children()[0])
        return True, ' ( - ' + s + ' ) '
    elif node.decl().name() == 'fp.fma':
        for index, one in enumerate(node.children()):
            flag, return_s = process_fpref_node(one)
            if flag:
                if index == 1:
                    s = return_s
                elif index == 2:
                    s += ' * ' + return_s
                elif index == 3:
                    s += ' + ' + return_s
        return True, ' ( ' + s + ' ) '
    elif node.decl().name() == 'fp.rem':
        child_len = len(node.children())
        # print(node.children())
        if child_len == 2:
            left = ''
            right = ''
            for index, one in enumerate(node.children()):
                flag, return_s = process_fpref_node(one)
                if flag:
                    if index == 0:
                        left = return_s
                    elif index == 1:
                        right = return_s
            s = left + ' - ' + left + ' / ' + right + ' * ' + right
        else:
            print(f'fp.rem has more than 2 children:{node.children()}')
            return False, ''
            exit(-2)
        '''
        elif child_len == 3:
            for index, one in enumerate(node.children()):
                flag, return_s = process_fpref_node(one)
                if flag == True:
                    if index == 1:
                        left = return_s
                    elif index == 2:
                        right = return_s
            s = left + ' - ' + left + ' / ' + right + ' * ' + right
        '''
        return True, ' ( ' + s + ' ) '
    elif node.decl().name() == 'fp.abs':
        return True, str(node.children()[0])
    elif node.decl().name() == 'fp.max' or node.decl().name() == 'fp.min':
        return True, str(node.children()[0]) + ' ' + str(node.children()[1])
    else:
        s = str(node)
        return True, s


def find_one_num_in_fpref(node):
    if isinstance(node, z3.z3.FPRMRef):
        return False, ''
    elif node.decl().name() == 'fp':
        num_in_left = z3.simplify(z3.fpToReal(node)).as_string()
        return True, num_in_left
    elif len(node.children()) != 0:
        for child in node.children():
            return_flag, return_value = find_one_num_in_fpref(child)
            if return_flag:
                return True, return_value
        return False, ''
    else:
        return False, ''


def parse_one_node(item, functions, not_node=False):
    # print(f'\033[34m one constraint:{item} \033[0m') CQ
    function = ''
    if isinstance(item, z3.z3.BoolRef):
        decl_name = item.decl().name()
        if decl_name == 'and':
            for child_idx in range(len(item.children())):
                functions = parse_one_node(item.children()[child_idx], functions)
                if len(functions) == 0:
                    print(
                        f'\033[35m Skip! Don\'t generate objective functions due to unsupported operation.\033[0m')
                    return []
        elif decl_name == 'or':
            # circumstance like Or(fpIsNormal(a), fpIsZero(a), fpIsSubnormal(a)), skip
            or_start_idx = len(functions)
            for child_idx in range(len(item.children())):
                functions = parse_one_node(item.children()[child_idx], functions)
                if len(functions) == 0:
                    print(
                        f'\033[35m Skip! Don\'t generate objective functions due to unsupported operation.\033[0m')
                    return []
            for i in range(or_start_idx + 1, len(functions)):
                # add special words to label "or"
                if isinstance(functions[i], str):
                    functions[i] = "#or#" + functions[i]
                elif isinstance(functions[i], list):
                    functions[i][0] = "#or#" + functions[i][0]
        elif decl_name == 'not':

            if len(item.children()) == 1:
                sub_node = item.children()[0]
                if sub_node.decl().name() in cannot_handle:
                    return []
                if isinstance(sub_node.children()[0], z3.z3.FPRef) and isinstance(sub_node.children()[1], z3.z3.FPRef):
                    functions = parse_one_node(sub_node, functions, True)
                    # print(f'\033[33mnot supported\033[0m')
                elif isinstance(sub_node.children()[0], z3.z3.BoolRef) and isinstance(sub_node.children()[1],
                                                                                      z3.z3.BoolRef):
                    #print("sub_node: ", sub_node, "\n\n\n", sub_node.children())
                    functions = parse_one_node(sub_node, functions, True)
                    #print("functions: ", functions)
                    # print(f'\033[33mnot supported\033[0m')
                else:
                    print(f'not node children type are not supported')
                    return []
                    exit(-1)
            else:
                print(f'not node has more than 1 child: {item.children()}')
                return []
                exit(-2)
        elif decl_name == 'fp.eq' or decl_name == '=':
            if isinstance(item.children()[0], z3.z3.FPRef) and isinstance(item.children()[1], z3.z3.FPRef):
                left_side = ''
                right_side = ''
                left_decl = item.children()[0].decl().name()
                right_decl = item.children()[1].decl().name()
                left_node = item.children()[0]
                right_node = item.children()[1]
                # print(f'left_decl: {left_decl}') CQ
                # print(f'right_decl: {right_decl}') CQ
                if left_decl in cannot_handle or right_decl in cannot_handle:
                    return []
                if not left_node.children():
                    left_side = str(left_node)
                elif left_decl in need_further_process_type:
                    flag, return_s = process_fpref_node(left_node)
                    if flag:
                        left_side += return_s + ' '
                else:
                    for one_in_left in left_node.children():
                        # print(f'one_in_left.decl().name(): {one_in_left.decl().name()}') CQ
                        if one_in_left.decl().name() in cannot_handle:
                            return []
                        if one_in_left.decl().name() in need_further_process_type:
                            flag, return_s = process_fpref_node(one_in_left)
                            if flag:
                                left_side += return_s + ' '
                        else:
                            left_side += str(one_in_left) + ' '

                if not right_node.children():
                    right_side = str(right_node)
                elif right_decl in need_further_process_type:
                    flag, return_s = process_fpref_node(right_node)
                    if flag:
                        right_side += return_s + ' '
                else:
                    for one_in_right in right_node.children():
                        # print(f'one_in_right.decl().name(): {one_in_right.decl().name()}') CQ
                        if one_in_right.decl().name() in cannot_handle:
                            return []
                        if one_in_right.decl().name() in need_further_process_type:
                            flag, return_s = process_fpref_node(one_in_right)
                            if flag:
                                right_side += return_s + ' '
                        else:
                            right_side += str(one_in_right) + ' '

                if not not_node:
                    function = '( ( ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2'
                    if left_decl == 'fp.abs':
                        function = [left_side + '> 0.0', '( ( ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2',
                                    '( ( - ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2']
                    elif left_decl == 'fp.max':
                        function = [left_side.split()[0] + ' > ' + left_side.split()[1],
                                    '( ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' ) ) ** 2',
                                    '( ( ' + left_side.split()[1] + ' ) - ( ' + right_side + ' ) ) ** 2']
                    elif left_decl == 'fp.min':
                        function = [left_side.split()[0] + ' > ' + left_side.split()[1],
                                    '( ( ' + left_side.split()[1] + ' ) - ( ' + right_side + ' ) ) ** 2',
                                    '( ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' ) ) ** 2']
                else:
                    # not-equal rule
                    # print(f'use not equal rule to construct objective function')
                    if left_decl == 'fp.abs' or left_decl == 'fp.max' or left_decl == 'fp.min':
                        print(f'\033[31m Error! Need to further process. \033[0m')
                        return []
                        exit(-2) # TODO wintersteiger/max/max-has-no-other-solution-2320.smt2
                    function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= - ' + EPSILON, '0.0',
                                ' ( ' + left_side + ' ) - ( ' + right_side + ' ) > - ' + EPSILON + ' and ( ' + left_side + ' ) - ( ' + right_side + ' ) < ' + EPSILON,
                                '( ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON + ' ) * ( ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON + ' )',
                                '0.0']
                # print(f'\033[31m check the function of parenthesis and not equal: {function}\033[0m')
                # exit(-2)
                functions.append(function)
                # print(f'\033[32m function:{function}\033[0m') CQ
            elif isinstance(item.children()[0], z3.z3.BoolRef) and isinstance(item.children()[1], z3.z3.BoolRef):
                if item.children()[1].decl().name() == 'false':
                    if item.children()[0].decl().name() == 'fp.eq' or item.children()[0].decl().name() == '=':
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        if not_node:
                            if item.children()[0].children()[0].decl().name() == 'fp.abs':
                                function = [left_side + ' > 0.0',
                                            '( ( ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2',
                                            '( ( - ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2']
                            else:
                                function = '( ( ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2'
                        else:
                            # not-equal rule
                            # print(f'use not equal rule to construct objective function')
                            function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= - ' + EPSILON, '0.0',
                                        ' ( ' + left_side + ' ) - ( ' + right_side + ' ) > - ' + EPSILON + ' and ( ' + left_side + ' ) - ( ' + right_side + ' ) < ' + EPSILON,
                                        '( ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON + ' ) * ( ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON + ' )',
                                        '0.0']
                        # print(f'\033[31m check the function of parenthesis and not equal: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32mfunction:{function}\033[0m') CQ
                    elif item.children()[0].decl().name() == 'fp.lt' or item.children()[0].decl().name() == 'leq':
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        # (x<y) == false (consider <not> and ordinary, < and <=
                        if not_node:
                            if item.children()[0].decl().name() == 'fp.lt':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                            elif item.children()[0].decl().name() == 'fp.leq':
                                function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                        else:
                            if item.children()[0].decl().name() == 'fp.lt':
                                function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                            elif item.children()[0].decl().name() == 'fp.leq':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        # function = [
                        #     str(item.children()[0].children()[0]) + operator + str(item.children()[0].children()[1]),
                        #     '0.0',
                        #     str(item.children()[0].children()[0]) + ' - ' + str(item.children()[0].children()[1])]
                        # print(f'\033[31m check the function: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32mfunction:{function}\033[0m') CQ
                    elif item.children()[0].decl().name() == 'fp.gt' or item.children()[0].decl().name() == 'geq':
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        # (x>y) == false (consider <not> and ordinary, > and >=
                        if not_node:
                            if item.children()[0].decl().name() == 'fp.gt':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                            elif item.children()[0].decl().name() == 'fp.geq':
                                function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                        else:
                            if item.children()[0].decl().name() == 'fp.gt':
                                function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                            elif item.children()[0].decl().name() == 'fp.geq':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        # function = [
                        #     str(item.children()[0].children()[0]) + operator + str(item.children()[0].children()[1]),
                        #     '0.0',
                        #     '( ' + str(item.children()[0].children()[0]) + ' ) - ( ' + str(item.children()[0].children()[1]) + ' )']
                        # print(f'\033[31m check the function: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32mfunction:{function}\033[0m') CQ
                    else:
                        print(f'unrecognized operator: {item.children()[0]}')
                        return []
                        exit(-2)
                elif item.children()[1].decl().name() == 'true':
                    if item.children()[0].decl().name() == 'fp.eq' or item.children()[0].decl().name() == '=':
                        # (x==y) == true (consider <not> and ordinary
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        if not_node:
                            # not-equal rule
                            # print(f'use not equal rule to construct objective function')
                            function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= - ' + EPSILON, '0.0',
                                        ' ( ' + left_side + ' ) - ( ' + right_side + ' ) > - ' + EPSILON + ' and ( ' + left_side + ' ) - ( ' + right_side + ' ) < ' + EPSILON,
                                        '( ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON + ' ) * ( ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON + ' )',
                                        '0.0']
                        else:
                            function = '( ( ' + left_side + ' ) - ( ' + right_side + ' ) ) ** 2'
                        # print(f'\033[31m check the function whether need to add parenthesis: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32mfunction:{function}\033[0m') CQ
                    elif item.children()[0].decl().name() == 'fp.lt' or item.children()[0].decl().name() == 'fp.leq':
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        # (x<y) == true (consider <not> and ordinary, > and >=
                        if not_node:
                            if item.children()[0].decl().name() == 'fp.lt':
                                function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                            elif item.children()[0].decl().name() == 'fp.leq':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        else:
                            if item.children()[0].decl().name() == 'fp.lt':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                            elif item.children()[0].decl().name() == 'fp.leq':
                                function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                        # function = [
                        #     str(item.children()[0].children()[0]) + operator + str(item.children()[0].children()[1]),
                        #     '0.0',
                        #     '( ' + str(item.children()[0].children()[0]) + ' ) - ( ' + str(item.children()[0].children()[1]) + ' )']
                        # print(f'\033[31m check the function: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32mfunction:{function}\033[0m') CQ
                    elif item.children()[0].decl().name() == 'fp.gt' or item.children()[0].decl().name() == 'geq':
                        left_side = str(item.children()[0].children()[0])
                        right_side = str(item.children()[0].children()[1])
                        # (x>y) == true (consider <not> and ordinary, > and >=
                        if not_node:
                            if item.children()[0].decl().name() == 'fp.gt':
                                function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                            elif item.children()[0].decl().name() == 'fp.geq':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                            ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        else:
                            if item.children()[0].decl().name() == 'fp.gt':
                                function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                            elif item.children()[0].decl().name() == 'fp.geq':
                                function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                            ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                        # function = [
                        #     str(item.children()[0].children()[0]) + operator + str(item.children()[0].children()[1]),
                        #     '0.0',
                        #     '( ' + str(item.children()[0].children()[0]) + ' ) - ( ' + str(item.children()[0].children()[1]) + ' )']
                        # print(f'\033[31m check the function: {function}\033[0m')
                        # exit(-2)
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m') CQ
                    else:
                        print(f'unrecognized operator: {item.children()[0]}')
                        return []
                        exit(-2)
                else:
                    print(f'neither true or false in the right hand side of BoolRef not node: {item}')
                    return []
                    exit(-2)
            else:
                print(f'Not supported. BoolRef\'s children:{item.children()}')
                return []
                exit(-1)
        elif decl_name == 'fp.lt' or decl_name == 'fp.leq' or decl_name == 'fp.gt' or decl_name == 'fp.geq':
            if decl_name == 'fp.lt':
                operator = ' < '
                # opposite_operator = ' > '
            elif decl_name == 'fp.leq':
                operator = ' <= '
                # opposite_operator = ' >= '
            elif decl_name == 'fp.gt':
                operator = ' > '
                # opposite_operator = ' < '
            elif decl_name == 'fp.geq':
                operator = ' >= '
                # opposite_operator = ' <= '
            left_side = ''
            right_side = ''
            left_decl = item.children()[0].decl().name()
            right_decl = item.children()[1].decl().name()
            left_node = item.children()[0]
            right_node = item.children()[1]
            # print(f'left_decl: {left_decl}') CQ
            # print(f'right_decl: {right_decl}') CQ
            if left_decl in cannot_handle or right_decl in cannot_handle:
                return []
            if not left_node.children():
                left_side = str(left_node)
            elif left_decl in need_further_process_type:
                flag, return_s = process_fpref_node(left_node)
                if flag:
                    left_side += return_s + ' '
            else:
                for one_in_left in left_node.children():
                    # print(f'one_in_left.decl().name(): {one_in_left.decl().name()}') CQ
                    if one_in_left.decl().name() in cannot_handle:
                        return []
                    if one_in_left.decl().name() in need_further_process_type:
                        flag, return_s = process_fpref_node(one_in_left)
                        if flag:
                            left_side += return_s + ' '
                    else:
                        left_side += str(one_in_left) + ' '

            if not right_node.children():
                right_side = str(right_node)
            elif right_decl in need_further_process_type:
                flag, return_s = process_fpref_node(right_node)
                if flag:
                    right_side += return_s + ' '
            else:
                for one_in_right in right_node.children():
                    # print(f'one_in_right.decl().name(): {one_in_right.decl().name()}')
                    if one_in_right.decl().name() in cannot_handle:
                        return []
                    if one_in_right.decl().name() in need_further_process_type:
                        flag, return_s = process_fpref_node(one_in_right)
                        if flag:
                            right_side += return_s + ' '
                    else:
                        right_side += str(one_in_right) + ' '
            if not not_node:
                # ordinary node
                if operator == ' < ':
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' > ':
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' <= ':
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) >= ( ' + left_side.split()[0] + ' )', '0.0',
                                    ' ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) <= ( ' + right_side.split()[0] + ' )', '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' >= ':
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) <= ( ' + left_side.split()[0] + ' )', '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) >= ( ' + right_side.split()[0] + ' )', '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
            else:
                # not node
                if operator == ' < ':  # Actually is >=
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) <= ( ' + left_side.split()[0] + ' )',
                                    '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) >= ( ' + right_side.split()[0] + ' )', '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) >= ( ' + right_side + ' )', '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' > ':  # Actually is <=
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) >= ( ' + left_side.split()[0] + ' )',
                                    '0.0',
                                    ' ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) <= ( ' + right_side.split()[0] + ' )', '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) <= ( ' + right_side + ' )', '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side + ' )']
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' <= ':  # Actually is >
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + right_side.split()[0] + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + right_side + ' ) - ( ' + left_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                elif operator == ' >= ':  # Actually is <
                    if len(left_side.split()) == 1 and is_float(left_side.split()[0]):
                        function = [' ( ' + right_side + ' ) - ( ' + left_side.split()[0] + ' ) >= ' + EPSILON, '0.0',
                                    ' ( ' + left_side.split()[0] + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    elif len(right_side.split()) == 1 and is_float(right_side.split()[0]):
                        function = [' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side.split()[0] + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
                    else:
                        function = [' ( ' + left_side + ' ) - ( ' + right_side + ' ) <= -' + EPSILON, '0.0',
                                    ' ( ' + left_side + ' ) - ( ' + right_side + ' ) + ' + EPSILON]
                        functions.append(function)
                        # print(f'\033[32m function:{function}\033[0m')
        elif decl_name in cannot_handle:
            return []
        else:
            print(f'Not supported. BoolRef.name:{decl_name}')  # TODO
            return []
            exit(-1)
    else:
        print(f'Not supported. item.type:{type(item)}')
        return []
        exit(-1)
    return functions


def parse_one_smtfile(file_full_path):
    if os.path.exists(file_full_path):
        print(f'processing file {file_full_path}')
        relative_path = '/'.join(file_full_path.split('/')[6:])
        print(f'relative path: \n{relative_path}')
        ast_vector = z3.parse_smt2_file(file_full_path)
        # if '::main::' in ast_vector[0].children()[0].decl().name(): # TODO
        #     print(
        #         f'\033[35m Skip! Don\'t generate objective functions for file {relative_path} cause parse error.\033[0m')
        #     return []
        # print(f'constraints:{ast_vector}\n') CQ
        functions = []
        for item in ast_vector:
            functions = parse_one_node(item, functions)
            if len(functions) == 0:
                print(
                    f'\033[35mSkip! Don\'t generate objective functions for file {file_full_path} cause it contain unsupported operation.\033[0m')
                break
        # print(f'\noverall functions:{functions}\n') CQ
        return functions
    else:
        print(f'\033[31m Error! Don\'t exists the file {file_full_path}.\033[0m')
        exit(-2)
        # return []


def is_float(x):
    try:
        float(x)
        if str(x) in ['inf', 'infinity', 'INF', 'INFINITY', 'True', 'NAN', 'nan', 'False', '-inf', '-INF', '-INFINITY',
                      '-infinity', 'NaN', 'Nan']:
            return False
        else:
            return True
    except:
        try:
            return is_float(eval(x))
        except:
            return False

def get_rounding_mode(smt2_file_path):

    def check_mode(line):
        mode = ["RNE","RTP","RTN","RTZ","roundNearestTiesToEven","roundTowardPositive","roundTowardZero","roundTowardNegative"]

        for m in mode:
            if m in line:
                if m in ["RNE", "roundNearestTiesToEven"]:
                    return "RNE"
                elif m in ["RTP", "roundTowardPositive"]:
                    return "RTP"
                elif m in ["RTN", "roundTowardNegative"]:
                    return "RTN"
                elif m in ["RTZ", "roundTowardZero"]:
                    return "RTZ"
                else:
                    return "UNKNOWN"
                
        return None

    if smt2_file_path == "None":
        return "RNE"
    mode = ""
    with open(smt2_file_path, 'r') as sf:
        while True:
            line = sf.readline()
            if not line:
                break
            m = check_mode(line)
            if m != None:
                mode = m
                break # only one mode
    if mode == "":
        mode = "RNE" # default RNE
    return mode

def split_represent_final_objective_function(filename, functions, source_filename, variable_num=None, negation_idx = None, smt2_filepath = None):
    constraint_num = len(functions)
    variables = []
    append = ''
    split = []
    for one in functions:
        if isinstance(one, str):
            if one != '':
                if one.startswith("#or#"):
                    one = one[4:]
                    append += ' * ' + one
                else:
                    append += ' + ' + one
                for part in one.split():
                    # check the identifier according to the requirements of PL
                    '''
                    if re.fullmatch(pattern_for_variable, part):
                        if not is_float(part):  # part is variable
                            if part not in variables:
                                variables.append(part)
                    '''
                    # exclude the special characters, and the rest are all variables
                    if part not in characters and not is_float(part) and part not in variables:
                        variables.append(part)

        elif isinstance(one, list):
            split.append(one)
            for component in one:
                for part in component.split():
                    if part not in characters and not is_float(part) and part not in variables:
                        variables.append(part)
                    '''
                    if re.match(pattern_for_variable, part) and not is_float(part):  # part is variable
                        if part not in variables:
                            variables.append(part)
                    '''
    append = append[3:]
    # print(f'variables:{variables}') CQ
    if len(variables) == 0:
        # parse error
        print(f'\033[31m Error! Don\'t contain any variable in {source_filename}.\033[0m')
        exit(-2)
        return False
    if variable_num is not None:
        if len(variables) != variable_num:
            return False
        # assert len(variables) == variable_num

    if negation_idx is None:
        code_snippet = '''def ''' + source_filename + '''(params):\n    '''
    else:
        code_snippet = '''def ''' + source_filename + '''_''' + str(negation_idx) + '''(params):\n    '''
    for index, v in enumerate(variables):
        if index == 0:
            code_snippet += v
        else:
            code_snippet += ', ' + v
    code_snippet += ''' = params'''
    rounding_mode = get_rounding_mode(smt2_filepath)
    if rounding_mode == "RTZ":
        code_snippet += '''\n    libm.fesetround(FE_TOWARDZERO)'''
    elif rounding_mode == "RTP":
        code_snippet += '''\n    libm.fesetround(FE_UPWARD)'''
    elif rounding_mode == "RTN":
        code_snippet += '''\n    libm.fesetround(FE_DOWNWARD)'''
    else:
        code_snippet += '''\n    libm.fesetround(FE_TONEAREST)'''
    return_append = ''
    for index in range(len(split)):
        if split[index][0].startswith("#or#"):
            split[index][0] = split[index][0][4:]
            return_append += ''' #or#segment''' + str(index)
        else:
            return_append += ''' segment''' + str(index)
        code_snippet += '''\n    segment''' + str(index) + ''' = None'''
        length = len(split[index])
        assert length % 2 != 0
        if length == 3:
            code_snippet += '''\n    if ''' + split[index][0] + ''':\n''' + '''        segment''' + str(index) + ''' = ''' + \
                        split[index][1] + '''\n    else:\n''' + '''        segment''' + str(index) + ''' = ''' + \
                        split[index][2]
        else:
            # CQ !=
            code_snippet += '''\n    if ''' + split[index][0] + ''':\n''' + '''        segment''' + str(index) + ''' = ''' + \
                        split[index][1]
            for index_p in range(2, length - 1, 2):
                code_snippet += '''\n    elif ''' + split[index][index_p] + ''':\n''' + '''        segment''' + str(index) + ''' = ''' + \
                        split[index][index_p+1]
            code_snippet += '''\n    else:\n''' + '''        segment''' + str(index) + ''' = ''' + split[index][length-1]

    code_snippet += '''\n    return '''
    if len(append) == 0:
        return_append_split = return_append.split()
        code_snippet_t = ""
        for i in range(len(return_append_split)):
            if return_append_split[i].startswith("#or#"):
                code_snippet_t += ' * ' + return_append_split[i][4:]
            else:
                code_snippet_t += ' + ' + return_append_split[i]
        code_snippet += code_snippet_t[3:] #' + '.join(return_append.split())
    else:
        code_snippet += append
        if len(return_append.split()) > 0:
            return_append_split = return_append.split()
            code_snippet_t = ""
            for i in range(len(return_append_split)):
                if return_append_split[i].startswith("#or#"):
                    code_snippet_t += ' * ' + return_append_split[i][4:]
                else:
                    code_snippet_t += ' + ' + return_append_split[i]
            code_snippet += code_snippet_t
            #code_snippet += ''' + ''' + '+'.join(return_append.split())

    # print(f'generated code snippet:\n{code_snippet}') CQ
    # check variable name
    replace_idx = 0
    for v in variables:
        if not v.isidentifier():
            code_snippet = code_snippet.replace(v, "rplc_x" + str(replace_idx))
            replace_idx += 1
    # write into file
    with open(filename, 'a') as fw:
        fw.write(code_snippet + '\n\n')
    return True

def construct_objective_function(functions):
    # organize all piecewise function
    less_fun = {}
    grt_fun = {}
    append = ''
    interval_variables = []
    points = {}
    for fun in functions:
        if isinstance(fun, list):
            if '<' in fun[0] or '<=' in fun[0]:
                if is_float(fun[0].split()[2]):
                    num = float(fun[0].split()[2])
                    var = fun[0].split()[0]
                    if var not in interval_variables:
                        interval_variables.append(var)
                        less_fun[var] = {}
                        grt_fun[var] = {}
                        points[var] = []
                    points[var].append(num)
                    less_fun[var][str(num)] = fun[1]
                    grt_fun[var][str(num)] = fun[2]
                    # less_fun[num] = fun[1]
                    # grt_fun[num] = fun[2]
                else:
                    print(f'< between variables')

            elif '>' in fun[0] or '>=' in fun[0]:
                if is_float(fun[0].split()[2]):
                    num = fun[0].split()[2]
                    var = fun[0].split()[0]
                    if var not in interval_variables:
                        interval_variables.append(var)
                        less_fun[var] = {}
                        grt_fun[var] = {}
                        points[var] = {}
                    points[var].append(num)
                    less_fun[var][str(num)] = fun[2]
                    grt_fun[var][str(num)] = fun[1]
                    # less_fun = fun[2]
                    # grt_fun = fun[1]
                else:
                    print(f'> between variables')

            else:
                print(f'Not supported. fun:{fun}')
                # CQ 240321 exit(-1)
        elif isinstance(fun, str):
            append += ' + ' + fun
    print(f'less_fun:{less_fun}')
    print(f'grt_fun:{grt_fun}')
    print(f'append:{append}')
    print(f'interval_variables:{interval_variables}')
    print(f'points:{points}')

    # get all variables
    variables = interval_variables.copy()

    for one in append.split():
        if re.match(pattern_for_variable, one) and not re.match(pattern_for_num, one) and one not in variables:
            variables.append(one)
    print(f'variables:{variables}')

    # combine all piecewise function
    interval_function = OrderedDict()
    for var in interval_variables:
        # points[var] = sorted(map(float, points[var]))
        interval_function[var] = {}
        if len(points[var]) == 1:
            num = points[var][0]
            interval_function[var]['-,' + str(num)] = less_fun[var][str(num)]
            interval_function[var]['-,' + str(num)] += append
            interval_function[var][str(num) + ',+'] = grt_fun[var][str(num)]
            interval_function[var][str(num) + ',+'] += append
        else:
            for i, num in enumerate(points[var]):
                if i == 0:
                    interval_function['-,' + str(num)] = ''
                    for item in less_fun.keys():
                        interval_function['-,' + str(num)] += ' + ' + less_fun[item]
                    interval_function['-,' + str(num)] += append
                    interval_function['-,' + str(num)] = interval_function['-,' + str(num)][3:]
                elif i == len(points[var]) - 1:
                    interval_function[str(num) + ',+'] = ''
                    for item in grt_fun.keys():
                        interval_function[str(num) + ',+'] += ' + ' + grt_fun[item]
                    interval_function[str(num) + ',+'] += append
                    interval_function[str(num) + ',+'] = interval_function[str(num) + ',+'][3:]
                else:
                    interval_function[str(points[var][i - 1]) + ',' + str(num)] = ''
                    for item in less_fun.keys():
                        if float(item) < num:
                            interval_function[str(points[var][i - 1]) + ',' + str(num)] += ' + ' + grt_fun[item]
                        else:
                            interval_function[str(points[var][i - 1]) + ',' + str(num)] += ' + ' + less_fun[item]
                    interval_function[str(points[var][i - 1]) + ',' + str(num)] += append
                    interval_function[str(points[var][i - 1]) + ',' + str(num)] = interval_function[
                                                                                      str(points[var][
                                                                                              i - 1]) + ',' + str(num)][
                                                                                  3:]

    print(f'interval_function:{interval_function}\n')
    assert len(interval_function) == len(interval_variables)
    return interval_function, interval_variables, variables


def write_into_py_file(filename, functions, interval_variables, variables, source_filename):
    # write objective function into python file
    code_snippet = '''def f''' + source_filename + '''(params):\n    '''
    for index, v in enumerate(variables):
        if index == 0:
            code_snippet += v
        else:
            code_snippet += ',' + v
    code_snippet += ''' = params'''

    # combine different variable's interval and function
    pieces_sum = 1
    for index in range(len(functions)):
        pieces_sum *= len(functions[interval_variables[index]])
    combined_interval_functions = combine(functions)

    print(f'should generated {pieces_sum} pieces')
    assert pieces_sum == len(combined_interval_functions)

    # continue writing
    for one in combined_interval_functions:
        # type(one) = list
        assert len(one) == len(interval_variables)
        condition = ''
        stmt = ''
        for index in range(len(interval_variables)):
            condition += ' and ' + return_code_format_interval(one[index][0], interval_variables[index])
            stmt += ' + ' + one[index][1]
        code_snippet += '''\n    if (''' + condition[5:] + '''):
        return ''' + stmt[3:]
        # return eval(\'''' + stmt[3:] + '''\')'''

    print(f'generated code snippet:\n{code_snippet}')
    # write into file
    with open(filename, 'w') as fw:
        fw.write(code_snippet + '\n\n')


def combine(functions={}, idx=0, final=[], one=[]):
    max_idx = len(functions) - 1
    keys = list(functions.keys())
    # print(type(keys))
    sub_items = list(functions[keys[idx]].items())
    # print(len(functions[keys[idx]]))
    for sub_idx in range(len(functions[keys[idx]])):
        one.append(sub_items[sub_idx])
        if idx == max_idx:
            final.append([*one])
        else:
            final = combine(functions, idx + 1, final, one)
        one.pop()
    return final


def return_code_format_interval(interval, variable):
    if interval.startswith('-,'):
        return variable + ' < ' + interval.split(',')[1]
    elif interval.endswith(',+'):
        return variable + ' > ' + interval.split(',')[0]
    else:
        return variable + ' > ' + interval.split(',')[0] + ' and ' + variable + ' < ' + interval.split(',')[1]


def run_dataset():
    object_dir = '/home/chenqian/Documents/poly/QF_FP-master/'
    # filename = '/home/chenqian/Documents/poly/benchmarks+output/output/gosat/result.csv'
    filename = '/home/chenqian/Desktop/gt5-benchmark-result.csv'
    # filename = '/home/chenqian/Desktop/testcq.csv'
    write_filename = 'generated_objective_functions/objective_functions.py'
    skip = ['/root/benchmarks/benchmarks-5000/easy/newton.6.1.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/newton.8.3.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/square.4.0.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/newton.6.3.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/sine.3.0.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/newton.2.3.i.smt2',
            '/root/benchmarks/benchmarks-5000/easy/square.5.0.i.smt2',
            '/root/benchmarks/benchmarks-5000/hard/double_req_bl_0310_true-unreach-call.c_1.smt2',
            '/root/QF_FP/griggio/fmcad12/sin.c.125.smt2', '/root/QF_FP/griggio/fmcad12/sin.c.175.smt2',
            '/root/QF_FP/griggio/fmcad12/sin.c.25.smt2', '/root/QF_FP/griggio/fmcad12/sin.c.75.smt2',
            '/root/QF_FP/griggio/fmcad12/sin2.c.10.smt2',
            '/root/QF_FP/griggio/fmcad12/sin2.c.125.smt2']
    time_record = []
    os.popen('rm ' + write_filename)
    with open(filename, 'r') as f:
        content = csv.reader(f)
        for line in content:
            if line[0] in skip:
                continue
            print(line)
            # time.sleep(5)
            one_line_record = []
            variable_num = line[1]
            '''
            if line[0].split('/')[4].startswith('easy'):
                print(f'belong to easy')
            elif line[0].split('/')[4].startswith('medium'):
                print(f'belong to medium')
            elif line[0].split('/')[4].startswith('hard'):
                print(f'belong to hard')
            '''
            filepath = ''.join(line[0].split('.')[:-1]).split('/')[3:]
            if '/'.join(filepath).startswith('wintersteiger/toIntegral/') or '/'.join(filepath).startswith(
                    'wintersteiger/sqrt/'):
                continue
            if filepath[0][0].isdigit():
                source_filename = '_'.join(filepath[1:]).replace('-', '_')
            else:
                source_filename = '_'.join(filepath).replace('-', '_')
            full_filepath = object_dir + '/'.join(line[0].split('/')[3:])

            # if re.match('^\d.*', source_filename):
            #    print(f'\033[35mFunction name error. Skip.\033[0m')
            #    continue
            # print(full_filepath)
            # print(source_filename)
            # exit()
            start = time.time()
            functions = parse_one_smtfile(full_filepath)
            if len(functions) != 0:
                flag = split_represent_final_objective_function(write_filename, functions, source_filename
                                                                , int(variable_num))
                if flag == False:
                    print(
                        f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause parse error.\033[0m')
            else:
                print(
                    f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause it contain unsupported operation.\033[0m')
            end = time.time()
            time_used = end - start
            one_line_record.extend(line[:])
            one_line_record.append(str(time_used))
            time_record.append(one_line_record)
            print(f'time used:{time_used}')
    # print(f'time_record[0]:{time_record[0]}')
    with open('mpcs_result_for_constructing_objective_functions.csv', 'w') as fw:
        for one in time_record:
            fw.write(','.join(one) + '\n')


def run_single_file(filename):
    # if filename.startswith('wintersteiger/toIntegral/') or filename.startswith('wintersteiger/sqrt/'):
    #    exit()
    object_dir = '/home/chenqian/Documents/gradient_solve/QF_FP-master/'
    object_file = object_dir + filename
    write_filename = 'generated_objective_functions/objective_functions_1018.py'
    os.popen('rm ' + write_filename)
    filepath = '.'.join(filename.split('.')[:-1]).split('/')
    if filepath[0][0].isdigit():
        source_filename = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
    else:
        source_filename = '_'.join(filepath).replace('-', '_').replace('.', '_')
    # source_filename = '_'.join().replace('-','_')
    # if re.match('^\d.*', source_filename):
    #    print(f'\033[35mFunction name error. Skip.\033[0m')
    #    return
    # CQ the '-' in the original filename is replaced with '_', the redundant '.' is replaced with ''
    start = time.time()
    functions = parse_one_smtfile(object_file)
    if len(functions) != 0:
        flag = split_represent_final_objective_function(write_filename, functions, source_filename)
        if not flag:
            print(
                f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause parse error.\033[0m')
    else:
        print(
            f'\033[35mSkip! Don\'t generate objective functions for file {filename} cause it contain unsupported operation.\033[0m')

    # CQ combine in if-else
    # objective_functions, interval_variables, variables = construct_objective_function(functions)
    # write_into_py_file(write_filename, objective_functions, interval_variables, variables, source_filename)
    # CQ combine in return-smt
    # split_represent_final_objective_function(write_filename, functions, source_filename)
    end = time.time()
    time_used = end - start
    print(f'time used:{time_used}')


def compare_with_other_tools(filename, benchark_name):
    parse_error_num = 0
    unsupported_operation_num = 0
    benchmark = benchark_name#filename.split('/')[-1].split('.')[0].split('-')[0]
    #object_dir = '/home/chenqian/Documents/gradient_solve/QF_FP-master/'
    #write_dir = '/home/chenqian/Documents/gradient_solve/parse-constraint/' + benchmark + '/'
    write_dir = './' + benchmark + '/'
    # filename = '/home/chenqian/Documents/poly/benchmarks+output/output/gosat/result.csv'
    if not os.path.exists(write_dir):
        os.popen('mkdir ' + write_dir)
    else:
        os.popen('rm ' + write_dir + '/*')
    time.sleep(1)
    #write_filename = write_dir + 'objective_functions_' + benchmark + '.py'
    write_filename = 'objective_functions.py'

    with open(write_filename, "w") as wf:
        wf.write('''import ctypes
import numpy as np
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')\n\n''')
    
    skip = ['griggio/fmcad12/square_and_power_inverse.smt2', 'griggio/fmcad12/test_v5_r15_vr10_c1_s11127.smt2',
            '20170501-Heizmann-UltimateAutomizer/Newlib-BadKrozingenChallenge-Oversimplified.smt2',
            'ramalho/esbmc/nan_double-main.smt2', 'ramalho/esbmc/nan_float-main.smt2']
    skip = []
    time_record = []
    with open(filename, 'r') as f:
        content = csv.reader(f)
        for index, line in enumerate(content):
            if index == 0:
                pass#continue
            one_line_record = []
            one_line_record.extend(line[:])
            variable_num = line[2]
            # print(line[1])
            # print(line[1].split('.')[:-1])
            # print('.'.join(line[1].split('.')[:-1]))
            line_1_split = '.'.join(line[1].split('.')[:-1]).split('/')
            if 'QF_FP' in line[1]:
                idx = line_1_split.index('QF_FP')
            elif 'FP' in line[1]:
                idx = line_1_split.index('FP')
            else:
                idx = len(line_1_split) - 2
            filepath = line_1_split[idx + 1:]
            # print(filepath)
            # if '/'.join(filepath).startswith('wintersteiger/toIntegral/') or '/'.join(filepath).startswith('wintersteiger/sqrt/'):
            #    continue
            if filepath[0][0].isdigit():
                if len(filepath) <= 1 or filepath[1][0].isdigit():
                    source_filename = 'test_' + '_'.join(filepath[0:]).replace('-', '_').replace('.', '_')
                else:
                    source_filename = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
            else:
                source_filename = '_'.join(filepath).replace('-', '_').replace('.', '_')
            #full_filepath = object_dir + '/'.join(filepath) + '.smt2'
            full_filepath = line[0]
            if full_filepath == "":
                full_filepath = line[1]
            if '/'.join(filepath) + '.smt2' in skip:
                continue

            # if re.match('^\d.*', source_filename):
            #    print(f'\033[35mFunction name error. Skip.\033[0m')
            #    continue
            print(full_filepath)
            print(source_filename)
            # exit()
            start = time.time()
            functions = parse_one_smtfile(full_filepath)
            if len(functions) != 0:
                flag = split_represent_final_objective_function(write_filename, functions, source_filename
                                                                , int(variable_num), smt2_filepath = full_filepath)
                if not flag:
                    print(
                        f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause parse error.\033[0m')
                    parse_error_num += 1
                    one_line_record.append('parse error')
                    time_record.append(one_line_record)
                    continue
            else:
                print(
                    f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause it contain unsupported operation.\033[0m')
                unsupported_operation_num += 1
                one_line_record.append('unsupported operation')
                time_record.append(one_line_record)
                continue
            end = time.time()
            time_used = end - start
            one_line_record.append(str(time_used))
            time_record.append(one_line_record)
            print(f'time used:{time_used}')
    # print(f'time_record[0]:{time_record[0]}')
    #os.popen('cp ' + write_filename + ' ./objective_functions.py')
    write_data = np.array(time_record).tolist()
    df = pd.DataFrame(write_data)
    df.to_csv(write_dir + 'construct.csv', index=False, header=False)
    # with open(write_dir + 'mpcs_result_for_constructing_objective_functions.csv', 'w') as fw:
    #     for one in time_record:
    #         fw.write(','.join(one) + '\n')
    print(f'num of benchmarks due to parse error: {parse_error_num}')
    print(f'num of benchmarks due to unsupported operation: {unsupported_operation_num}')


def reconstruct_objective_function(read_file, write_file, benchmark):
    write_dir = '/home/chenqian/Documents/gradient_solve/parse-constraint/' + benchmark + '/'
    write_filename = write_dir + 'objective_functions_' + benchmark + '_final_after_negation.py'
    object_dir = '/home/chenqian/Documents/gradient_solve/QF_FP-master/'

    with open(read_file, 'r') as fr, open(write_file, 'w') as fw:
        read_data = csv.reader(fr)
        for index, line in enumerate(read_data):
            one_line_record = []
            one_line_record.extend(line[:])
            if line[18].strip() == 'unsat' and line[15].strip() != 'unsupported operation':
                idx = '.'.join(line[1].split('.')[:-1]).split('/').index('QF_FP')
                filepath = '.'.join(line[1].split('.')[:-1]).split('/')[idx + 1:]
                if filepath[0][0].isdigit():
                    source_filename = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
                else:
                    source_filename = '_'.join(filepath).replace('-', '_').replace('.', '_')
                print(f'\nfun name:[{source_filename}]')
                file_full_path = object_dir + '/'.join(filepath) + '.smt2'
                ast_vector = z3.parse_smt2_file(file_full_path)
                functions = []
                start = time.time()
                print(f'constraints: {ast_vector}')
                # CQ not ( A and B) == (not A) or (not B)
                for ii, item in enumerate(ast_vector):
                    # print(f'ast_vector component: {ast_vector[ii]}')
                    functions = parse_one_node(item, functions, True)
                    if len(functions) == 0:
                        print(
                            f'\033[35mSkip! Don\'t generate objective functions for file {file_full_path} cause it contain unsupported operation.\033[0m')
                        continue
                    else:
                        flag = split_represent_final_objective_function(write_file, functions, source_filename, negation_idx=ii)
                        if not flag:
                            print(
                                f'\033[35mSkip! Don\'t generate objective functions for file {source_filename} cause parse error.\033[0m')
                            # one_line_record.append('parse error')
                            # write_data.append(one_line_record)
                            # continue
                end = time.time()
                time_used = end - start
                one_line_record.append(str(time_used))
                one_line_record.append(str(len(ast_vector)))
            else:
                one_line_record.extend(['', ''])
            fw.write(','.join(one_line_record) + '\n')
    # os.popen('cp ' + write_filename + ' ./objective_functions.py')

def constrcut_csv(benchmark_folder_path, constrcut_csv_path):
    construct_list = []
    for root, _, files in os.walk(benchmark_folder_path):
        for file in files:
            if file.endswith('.smt2'):
                smt2_file_path = os.path.join(root, file)
                var_num = 0
                with open(smt2_file_path, 'r') as sf:
                    line = sf.readline()
                    while line:
                        if "declare-fun" in line:
                            var_num += 1
                        line = sf.readline()
                construct_list.append((smt2_file_path, smt2_file_path, var_num))
    with open(constrcut_csv_path, 'w', newline='') as cf:
        writer = csv.writer(cf)
        for construct in construct_list:
            writer.writerow(construct)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark","-b", help = "specify the output directory of benchmark to run", default="output")
    parser.add_argument("--path","-p", help = "need to specify the folder path of benchmark")
    args = parser.parse_args()
    benchmark = args.benchmark
    benchmark_folder_path = args.path
    # CQ supported constraint file:
    # griggio/fmcad12/square.smt2, e1_1.c.smt2, pow5.smt2, div.c.3.smt2, f23.smt2, test_v5_r5_vr10_c1_s5996, wintersteiger/add/add-has-no-other-solution-15685.smt2, wintersteiger/sub/sub-has-solution-11649.smt2

    # filename = 'griggio/fmcad12/newton.4.1.i.smt2'
    # run_single_file(filename)
    # exit()


    # run_dataset()
    # benchmark = '500'
    #compare_with_other_tools('/home/chenqian/Documents/gradient_solve/experiment_results/' + benchmark + '-benchmark-result.csv')
    constrcut_csv_path = 'to_construct.csv'
    constrcut_csv(benchmark_folder_path, constrcut_csv_path)
    compare_with_other_tools(constrcut_csv_path, benchmark)
    os.popen('rm ' + constrcut_csv_path)
    #parse_one_smtfile("a.smt2")

    '''
    # deal with unsat
    # cq the benchmarks that Grater returns 'unsat' should be processed further:
    # FIRST negation
    # SECOND solve the negated-benchmark,
    # IF it return 'sat', then the original benchmark is unsat
    # IF it return 'unsat', then the result fot original benchmark should be unknown
    benchmark = 'jfs'
    read_file = benchmark + '/mpcs_result_for_solving.csv'
    write_file = benchmark + '/mpcs_result_for_constructing_final_after_negation.csv'
    reconstruct_objective_function(read_file, write_file, benchmark)
    '''

    # wintersteiger/fma/fma-has-no-other-solution-2948.smt2 # CQ: circumstance of Not(xx == yy), i.e., not equal
    # griggio/fmcad12/test_v3_r3_vr10_c1_s14052.smt2 # CQ: circumstance of 'xx == yy + zz', where parenthesis is needed
    # ramalho/esbmc/newton_3_6_false-unreach-call-main.smt2 # CQ: contains sth like |c::main::fp::x@2!0&0#1|, not supported yet
    # 2017-xxxx # CQ: var name errors, not support yet