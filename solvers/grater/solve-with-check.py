# from mpcs_231030_gt5_result.objective_functions import *
import os

from objective_functions import *

import csv
import numpy as np
import sys, scipy, time, re, z3
from autograd import grad
import pandas as pd
import func_timeout
from func_timeout import func_set_timeout
import argparse
import bitstring
import random
import inspect
# import objective_functions_negation
# error code -1: not supported
# error code -2: error

ITERATION = 100000000
fun_whose_function_value_less_than_0 = []
succeed_function_value = []
pattern_for_variable = '[_a-zA-Z][_a-zA-Z0-9]*'
pattern_for_my_var = 'x[0-9]+'

def generate_x0(func, low, high):
    func_str = inspect.getsource(func)
    
    matches = re.findall(r'(?:\(\s*)+[a-z]+\d*(?:\s*\))+\s+[-]\s+(?:\(\s*)+[-]?\d+[/]?\d*(?:\s*\))+\s+\*\*\s+2', func_str)

    var_dict = {}

    for match in matches:
        var = re.search(r'[a-z]+\d*', match).group()
        num = re.search(r'(\(\s*)+[-]?\d+[/]?\d*(\s*\))', match).group()
        var_dict[var] = float(eval(num))
    
    line = re.search(r'([a-z]+\d*,*\s)+=\sparams', func_str).group()
    var_list = line.split(' = ')[0].split(', ') #
    results = []
    for var in var_list:
        if var_dict.get(var) != None:
            results.append(var_dict[var])
        else:
            a = high - low
            out = (np.random.rand(1) * a + low).tolist()
            results += out
    
    return np.array(results)

timeout = 48*60*60
@func_set_timeout(timeout)
def solve_one_in_benchmark(variable_num, filepath, var_list, gradf=None, negation_idx=None):
    if filepath[0][0].isdigit():
        if len(filepath) <= 1 or filepath[1][0].isdigit():
            fun = 'test_' + '_'.join(filepath[0:]).replace('-', '_').replace('.', '_')
        else:
            fun = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
        #fun = 'test_' + '_'.join(filepath[0:]).replace('-', '_').replace('.', '_')
        #fun = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
    else:
        fun = '_'.join(filepath).replace('-', '_').replace('.', '_')
    print(f'fun name: {fun}')
    if var_list is not None:
        var_list = var_list.split()
    # print(variable_num)
    global fun_whose_function_value_less_than_0, succeed_function_value
    func_name = fun
    #try:
    #    eval(fun)
    #except:
    #    print(f'\033 [35m does not contain the function in py file\033[0m')
    #    exit(-2) # TODO
    try:
        gradf = grad(eval(func_name))
    except NameError:
        print(f'\033[31m get autograd function error {func_name}\033[0m')
        return False, 0.0, None
        # one_to_write.append('not-supported')
        # one_to_write.append('not-supported')
        # one_to_write.append('get autograd function error')
        # write_data.append(one_to_write)
        # fw.write(','.join(one_to_write) + '\n')
        # continue
    if func_name == '':
        print(f'\033[31m function name error\033[0m')
        exit(-2) # TODO
    func_str = inspect.getsource(eval(func_name))
    matches = re.findall(r'(?:\(\s*)+[a-z]+\d*(?:\s*\))+\s+[-]\s+(?:\(\s*)+[-]?\d+[/]?\d*(?:\s*\))+\s+\*\*\s+2', func_str)
    has_solution = False
    if len(matches) == variable_num:
        has_solution = True
    start = time.time()
    solved = False
    x_ret = np.array([0] * variable_num)
    i = 0
    while True:
        i += 1
        if has_solution:
            ix0 = generate_x0(eval(func_name), -100, 100)
        elif i > 1 and np.all(abs(gradf(x_ret)) < 1.0): # add perturbation
            ix0 = x_ret + randfloat(variable_num, -10, 10)
        else:
            ix0 = randfloat(variable_num, -100, 100)
        print(f'i: {i}, Initial inputs:{ix0}')
        try:
            if gradf is not None:
                min = scipy.optimize.fmin_cg(eval(func_name), ix0, fprime=gradf, full_output=True)  # CQ how to convert a string to a callble function in python module]
                #print(eval(func_name)(min[0]))
            else:
                min = scipy.optimize.fmin_cg(eval(func_name), ix0, full_output=True)
        except Exception as e:
            print(e)
            exit(-1)
            my_ix0 = randfloat(variable_num, -100, 100)  # TODO
            min = [my_ix0, 1]
        x_ret = min[0]
        print("min_val: ", min[1])
        print("x_ret: ", x_ret)
        # CQ precise checking
        '''
        if min[1] == 0.0:
            solved = True
            break
        elif min[1] < 0.0:
            print(f'error objective function! the minimum value is < 0!')
        '''
        # CQ non-precise checking
        #if min[1] == 0.0:
        if float(format(min[1], '.9f')) == 0.0 or float(format(min[1], '.9f')) == -0.0:
            solved = True
            break
        # elif float(format(min[1], '.10f')) < 0.0:
        #     print(f'\033[31m error objective function! the minimum value is < 0!\033[0m')  # TODO
        #     fun_whose_function_value_less_than_0.append(func_name)
        if var_list is None:
            continue
        if re.fullmatch(pattern_for_my_var, var_list[0]):
            # the variable name has been re-shaped, jump the bring in check
            continue
        
        if not solved and min[1] < 1.0:
            print(f'function value now: {min[1]}, check the original constraint\'s satisfiability')
            # directly bring in original constraint and check
            # print(f'x_ret:{min[0]}')
            x_ret = min[0]
            x_list = {}
            for iii,val in enumerate(x_ret):
                x_list[var_list[iii]] = val
            fr_data = []
            read_smt_dir = 'checksat/QF_FP-JFS/'
            write_smt_dir = 'checksat/write_QF_FP-JFS/'
            read_smt_file = read_smt_dir + '/'.join(filepath) + '.smt2'
            if not os.path.exists(read_smt_file):
                continue
            with open(read_smt_file, 'r') as fr_smt:
                print(f'read smt file: {read_smt_file}')
                fr_data = fr_smt.readlines()
                for ii, one in enumerate(fr_data):
                    if one.startswith('(declare-fun'):
                        if len(one.split()) == 7: # in the form of '(declare-fun b2090 () (_ FloatingPoint 8 24))'
                            varname = one.split()[1]
                            print(one.split())
                            man = int(one.strip().split()[-1][:-2])
                            exp = int(one.split()[-2])
                            # bitsize = int(one.strip().split()[-1][:-2]) + int(one.split()[-2])
                            bitstr = bitstring.BitArray(float=x_list[varname], length=exp + man).bin
                            fr_data[ii] = one.replace('declare', 'define').replace('))\n', ')') + ' (fp #b' + bitstr[
                                0] + ' #b' + bitstr[1:exp + 1] + ' #b' + bitstr[exp + 1:] + '))\n'
                        elif len(one.split()) == 4: # in the form of '(declare-fun a () Float32)'
                            varname = one.split()[1]
                            bitsize = one.strip().split()[-1][:-1]
                            if bitsize.endswith('32'):
                                man = 24
                                exp = 8
                            elif bitsize.endswith('64'):
                                man = 53
                                exp = 11
                            else:
                                print(f'\033[31m Error. float bit-width is neither 32 nor 64: {one.strip().split()[-1]}\033[0m')
                                exit(0)
                            bitstr = bitstring.BitArray(float=x_list[varname], length=exp + man).bin
                            rep = '(_ FloatingPoint ' + str(exp) + ' ' + str(man) + ') (fp #b' + bitstr[0] + ' #b' + bitstr[
                                                                                        1:exp + 1] + ' #b' + bitstr[
                                                                                                             exp + 1:] + '))\n'
                            fr_data[ii] = one.replace('declare', 'define').replace('Float' + str(man+exp) + ')\n', rep)
                        else:
                            print(f'\033[31m Error. not support format: {one}\033[0m')
                            exit(0)

                # print(fr_data)
            with open(write_smt_dir + fun + '.smt2', 'w') as fw:
                fw.writelines(fr_data)
            solver = z3.z3.Solver()
            solver.from_file(write_smt_dir + fun + '.smt2')
            if solver.check() == z3.z3.sat:
                solved = True
                succeed_function_value.append(min[1])
                print(f'\033[31m function value now: {min[1]}, bring in the original constraint and return sat\033[0m')
                break
            # bitstr = bitstring.BitArray(float=min[0][0], length=32).bin

            '''
            # read cvc's solution and check
            cvc_model_dir = 'baselines/models/cvc5/'
            cvc_filename = filepath[-1] + '.txt'
            var_pair = {}
            fr_data = []
            with open(cvc_model_dir + cvc_filename, 'r') as fmodel, open(read_smt_dir + '/'.join(filepath) + '.smt2',
                                                                         'r') as fr_smt:
                fmodel_data = fmodel.readlines()
                fr_data = fr_smt.readlines()
                for ii, one in enumerate(fr_data):
                    if one.startswith('(declare-fun'):
                        var_pair[one.split()[1]] = ii
                # print(var_pair)
                for two in fmodel_data:
                    if two.startswith('(define-fun'):
                        # to replace line in original smt file
                        split_data = two.split()
                        fr_data[var_pair[split_data[1]]] = two
            with open(write_smt_dir + fun + '.smt2', 'w') as fw:
                fw.writelines(fr_data)
            solver = z3.z3.Solver()
            solver.from_file(write_smt_dir + fun + '.smt2')
            # print(solver.check())
            if solver.check() == z3.z3.sat:
                solved = True
                break
            '''
    end = time.time()
    time_used = end - start
    print(time_used)
    return solved, time_used, gradf


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


def solve_according_to_csv_file_comparing_4_tools_with_timeout(read_file, write_file):
    # read python file and get varlist for all functions
    with open('objective_functions.py','r') as fr:
        lines = fr.readlines()
    var_list = {}
    for ii,line in enumerate(lines):
        if line.startswith('def') == -1:
            varname = line.strip().split()[1][:line.strip().split()[1].index('(')]
            var_list[varname] = lines[ii+1].strip()[:lines[ii+1].strip().index('=')-1].replace(',','')
    # print(var_list)


    write_data = []
    '''
    cvc_model_dir = 'baselines/models/cvc5/'
    object_dir = '/home/chenqian/Documents/gradient_solve/QF_FP-master/'
    read_smt_dir = 'checksat/QF_FP-JFS/'
    write_smt_dir = 'checksat/write_QF_FP-JFS/'
    '''
    if not os.path.exists('checksat/'):
        os.popen('mkdir checksat')
    with open(read_file, 'r') as fr:
            #, open(write_file, 'w') as fw:
        read_data = csv.reader(fr)
        for index, line in enumerate(read_data):
            gradf = None
            # line = line.strip().split(',')
            # one_to_write = list(map(str, line[:]))
            one_to_write = []
            one_to_write.extend(line[:])
            line_1_split = '.'.join(line[1].split('.')[:-1]).split('/')
            if 'QF_FP' in line[1]:
                idx = line_1_split.index('QF_FP')
            elif 'FP' in line[1]:
                idx = line_1_split.index('FP')
            else:
                idx = len(line_1_split) - 2
            filepath = line_1_split[idx + 1:]
            # print(filepath)
            if filepath[0][0].isdigit():
                if len(filepath) <= 1 or filepath[1][0].isdigit():
                    fun = 'test_' + '_'.join(filepath[0:]).replace('-', '_').replace('.', '_')
                else:
                    fun = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
                #fun = 'test_' + '_'.join(filepath[0:]).replace('-', '_').replace('.', '_')
                #fun = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
            else:
                fun = '_'.join(filepath).replace('-', '_').replace('.', '_')
            # print(f'\nfun name:[{fun}]')
            not_supported = line[-1] == 'unsupported operation'
            if not_supported:
                one_to_write.append('not-supported')
                one_to_write.append('not-supported')
                one_to_write.append('contain not support operation')
                one_to_write.append('')
                write_data.append(one_to_write)
                data = np.array(write_data).tolist()
                df = pd.DataFrame(data)
                df.to_csv(write_file, index=False, header=False)
                continue
            '''
            cvc_filename = line[1].split('/')[-1]
            print(cvc_filename)
            cvc_filename = cvc_filename.replace('smt2','txt')
            # varname = []
            # varvalue = []
            # precision = []
            var_pair = {}
            fr_data = []
            with open(cvc_model_dir + cvc_filename, 'r') as fmodel, open(read_smt_dir + '/'.join(filepath) + '.smt2', 'r') as fr_smt:
                fmodel_data = fmodel.readlines()
                fr_data = fr_smt.readlines()
                for ii,one in enumerate(fr_data):
                    if one.startswith('(declare-fun'):
                        var_pair[one.split()[1]] = ii
                print(var_pair)
                for two in fmodel_data:
                    if two.startswith('(define-fun'):
                        # to replace line in original smt file
                        split_data = two.split()
                        fr_data[var_pair[split_data[1]]] = two
                        
                        # varname.append(split_data[1])
                        # precision1 = split_data[5]
                        # precision2 = split_data[6][:-1]
                        # precision.append([precision1,precision2])
                        # value = {}
                        # sign = split_data[8].replace('#','0')
                        # exponent = split_data[9].replace('#','0')
                        # mantissa = split_data[10].replace('))','').replace('#','0')
                        # value['sign'] = sign
                        # value['exponent'] = exponent
                        # value['mantissa'] = mantissa
                        # varvalue.append(value)
                        
                        # varvalue.append(z3.z3.fpFP(z3.z3.BitVecVal(sign, 1), z3.z3.BitVecVal(exponent, precision1), z3.z3.BitVecVal(mantissa, precision2)))
            with open(write_smt_dir + fun + '.smt2', 'w') as fw:
                fw.writelines(fr_data)
            solver = z3.z3.Solver()
            solver.from_file(write_smt_dir + fun + '.smt2')
            print(solver.check())
            print(solver.check() == z3.z3.sat)
            # print(varname)
            # print(varvalue)
            # assert len(varname) == len(varvalue)
            
            # write a new python script to check, did not work
            # with open('checksat/' + fun + '.py','w') as fc:
            #     fc.write('from z3 import *\n')
            #     fc.write('ctx = Context()\n')
            #     for ii, one in enumerate(varname):
            #         fc.write(one + ' = FP(\'' + one + '\', FPSort(' + precision[ii][0] + ',' + precision[ii][1] + '), ctx)\n')
            #     fc.write('solver = Solver(ctx=ctx)\n')
            #     fc.write('astvec = parse_smt2_file(\'' + object_dir + '/'.join(filepath) + '.smt2\')\n')
            #     fc.write('for one in astvec:\n')
            #     fc.write('    solver.add(one)\n')
            #     for ii, one in enumerate(varname):
            #         fc.write('input_' + one + ' = fpFP(BitVecVal(' + varvalue[ii]['sign'] + ', 1), BitVecVal(' + varvalue[ii]['exponent'] + ', ' + precision[ii][0] + '), BitVecVal(' + varvalue[ii]['mantissa'] + ', ' + precision[ii][1] + '))\n')
            #     fc.write('solver.push()\n')
            #     for ii, one in enumerate(varname):
            #         fc.write('solver.add(' + one + ' == input_' + one + ')\n')
            #     fc.write('result = solver.check()\n')
            #     fc.write('solver.pop()\n')
            #     fc.write('print(result)\n')
            exit(0)
            '''
            # TODO use the value to check whether it satisfy the original constraint
            # if fun.startswith('schanda'):
            # print(line)
            # exit()
            if re.match('^\d.*', fun):
                print(f'function name error. need to process')
                exit(-2)
                one_to_write.append('not-supported')
                one_to_write.append('not-supported')
                one_to_write.append('function name error')
                one_to_write.append('')
                write_data.append(one_to_write)
                data = np.array(write_data).tolist()
                df = pd.DataFrame(data)
                df.to_csv(write_file, index=False, header=False)
                # fw.write(','.join(one_to_write) + '\n')
                continue
            # variable_num = int(line[2])
            if filepath[0][0].isdigit():
                if len(filepath) > 1 and '_'.join(filepath[1:]).replace('-', '_').replace('.', '_') in var_list.keys():
                    one_var_list = var_list['_'.join(filepath[1:]).replace('-', '_').replace('.', '_')]
                    assert int(line[2]) == len(one_var_list.split())
                else:
                    one_var_list = None
            else:
                if '_'.join(filepath).replace('-', '_').replace('.', '_') in var_list.keys():
                    one_var_list = var_list['_'.join(filepath).replace('-', '_').replace('.', '_')]
                    assert int(line[2]) == len(one_var_list.split())
                else:
                    one_var_list = None
            var_num = int(line[2])
            try:
                solved, time_used, gradf = solve_one_in_benchmark(variable_num=var_num, filepath=filepath, var_list=one_var_list, gradf=gradf)
            except func_timeout.exceptions.FunctionTimedOut:
                print(f'\033[35m execution time out\033[0m')
                one_to_write.append('timeout')
                one_to_write.append(str(timeout))
                one_to_write.append('timeout')
                one_to_write.append('')
                write_data.append(one_to_write)
                # fw.write(','.join(one_to_write) + '\n')
                data = np.array(write_data).tolist()
                df = pd.DataFrame(data)
                df.to_csv(write_file, index=False, header=False)
                continue
            print(f'time used:{time_used}')
            one_to_write.append(str(time_used))
            if is_float(line[-1]):
                one_to_write.append(str(float(line[-1]) + time_used))
            else:
                one_to_write.append((''))
            if not solved:
                print(f'iteration reaches the max value! Did not find the minimum value. Did not cover the path.')
                one_to_write.append('unsat')
            else:
                print(f'Have found minimum value that is equal to 0! Cover the test case!')
                # print(min)
                # print(min[1])
                # print(min[1] == 0.0)
                one_to_write.append('sat')
            if gradf is None:
                one_to_write.append('get autograd function error')
            else:
                one_to_write.append('')
            write_data.append(one_to_write)
            # fw.write(','.join(one_to_write) + '\n')
            data = np.array(write_data).tolist()
            df = pd.DataFrame(data)
            df.to_csv(write_file, index=False, header=False)



def solve_one_function(filename, variable_num):
    fun = ''.join(filename.split('.')[:-1]).replace('/', '_')
    gradf = grad(eval(fun))
    start = time.time()
    ix0 = randfloat(variable_num, -100, 100)
    solved = False
    for i in range(ITERATION):
        # print(f'Initial inputs:{ix0}')
        try:
            min = scipy.optimize.fmin_cg(eval(fun), ix0, fprime=gradf
                                         , full_output=True)  # CQ how to convert a string to a callble function in python module]
            print(min)
            print(min[1])
            print(min[1] == 0.0)
        except:
            # print(f'Cannot get minimum value')
            min = [1, 1]
        if min[1] == 0.0:
            solved = True
            break
        ix0 = randfloat(variable_num, -100, 100)
    if not solved:
        print(f'iteration reaches the max value! Did not find the minimum value. Did not cover the path.')
    else:
        print(f'Have found minimum value that is equal to 0! Cover the test case!')
    end = time.time()
    print(f'time used:{end - start}')


def randfloat(num, low, high):
    if low > high:
        return None
    else:
        a = high - low
        out = (np.random.rand(num) * a + low).tolist()
        out = np.array(out)
        return out


def count_no_solution_in_csv_file(filename):
    read_data = pd.read_csv(filename)
    read_data = read_data.values.tolist()
    unsat_count = 0
    sat_count = 0
    # print(read_data)
    for line in read_data:
        if 'has-no-other-solution' in line[0]:
            unsat_count += 1
        else:
            sat_count += 1
    print(f'all data:{len(read_data)}')
    print(f'unsat data: {unsat_count}')
    print(f'sat data: {sat_count}')
    print(f'unsat + sat = {unsat_count + sat_count}')


def get_variable_num_from_source_code_file(filename):
    with open(filename + '.py', 'r') as fr:
        all_code_snippet = fr.read()
    benchmarks = all_code_snippet.split('\n\n')
    var_num_dic = {}
    for one in benchmarks:
        if one.split('\n')[0] == '':
            continue
        variable_num = one.split('\n')[1].count(',') + 1
        left_parenthesis_index = one.split('\n')[0].find('(')
        fun = one.split('\n')[0][4:left_parenthesis_index]
        var_num_dic[fun] = variable_num
    return var_num_dic


def solve_negation_unsat(read_file, write_file, final_file):
    write_data = []
    final_data = []
    with open(read_file, 'r') as fr, open(write_file, 'w') as fw:
        read_data = csv.reader(fr)
        for index, line in enumerate(read_data):
            if line[18].strip() == 'unsat' and line[15].strip() != 'unsupported operation':
                has_sat = False
                min_time = 100000000
                gradf = None
                idx = '.'.join(line[1].split('.')[:-1]).split('/').index('QF_FP')
                filepath = '.'.join(line[1].split('.')[:-1]).split('/')[idx + 1:]
                print(f'filepath:{filepath}')
                if filepath[0][0].isdigit():
                    fun = '_'.join(filepath[1:]).replace('-', '_').replace('.', '_')
                else:
                    fun = '_'.join(filepath).replace('-', '_').replace('.', '_')
                print(f'\nfun name:[{fun}]')
                if re.match('^\d.*', fun):
                    print(f'function name error. need to process')
                    exit(-2)
                variable_num = int(line[2])
                negation_num = int(line[21])
                for ii in range(negation_num):
                    one_to_write = []
                    one_to_write.extend(line[:])
                    try:
                        solved, time_used, gradf = solve_one_in_benchmark(fun, variable_num, gradf = gradf, negation_idx = ii)
                    except func_timeout.exceptions.FunctionTimedOut:
                        print(f'\033[35m execution exceed 500 s\033[0m')
                        one_to_write[0] = str(ii)
                        one_to_write.append('timeout')
                        one_to_write.append('timeout')
                        one_to_write.append('timeout')
                        one_to_write.append('')
                        write_data.append(one_to_write)
                        # fw.write(','.join(one_to_write) + '\n')
                        continue
                    print(f'time used:{time_used}')
                    one_to_write[0] = str(ii)
                    one_to_write.append(str(time_used))
                    if is_float(line[-1]):
                        one_to_write.append(str(float(line[-1]) + time_used))
                    else:
                        one_to_write.append((''))
                    if not solved:
                        print(
                            f'iteration reaches the max value! Did not find the minimum value. Did not cover the path.')
                        one_to_write.append('unsat')
                    else:
                        print(f'Have found minimum value that is equal to 0! Cover the test case!')
                        one_to_write.append('sat')
                        has_sat = True
                        if time_used < min_time:
                            min_time = time_used
                    if gradf is None:
                        one_to_write.append('get autograd function error')
                    else:
                        one_to_write.append('')
                    # fw.write(','.join(one_to_write) + '\n')
                write_data.append(one_to_write)

                final_write = one_to_write[:20]
                if has_sat:
                    final_write[18] = 'unsat'
                    final_write[17] = str(min_time)
                else:
                    final_write[18] = 'unknown'
                final_data.append(final_write)
            else:
                one_to_write = []
                one_to_write.extend(line[:])
                one_to_write.extend(['', '', '', ''])
                write_data.append(one_to_write)

                final_write = one_to_write[:20]
                if line[18].strip() == 'unsat':
                    final_write[18] = 'unknown'
                final_data.append(final_write)
    data = np.array(write_data).tolist()
    df = pd.DataFrame(data)
    df.to_csv(write_file, index=False, header=False)

    data2 = np.array(final_data).tolist()
    df2 = pd.DataFrame(data2)
    df2.to_csv(final_file, index=False, header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", "-b", help = "specify the output directory of benchmark to run", default="output")
    args = parser.parse_args()
    benchmark = args.benchmark
 
    # solve_according_to_py_file('generated_objective_functions/objective_functions_1018.py')
    # solve_according_to_py_file('generated_objective_functions/objective_functions.py')

    # solve_according_to_csv_file_comparing_4_tools_with_timeout('jfs/mpcs_result_for_constructing_objective_functions.csv','jfs/mpcs_result_for_solving.csv')
    # solve_according_to_csv_file_comparing_4_tools('/home/chenqian/Desktop/testcq.csv', 'mpcs_result_for_solving.csv')

    # solve_according_to_csv_file('mpcs_result_for_constructing_objective_functions.csv','mpcs_result_for_solving.csv')
    # count_no_solution_in_csv_file('mpcs_result_for_constructing_objective_functions.csv')

    # benchmark = 'jfs'
    read_file = benchmark + '/construct.csv'
    write_file = benchmark + '/solving_results.csv'
    # os.popen('cp -r /home/chenqian/Documents/gradient_solve/QF_FP-JFS/ checksat/')
    solve_according_to_csv_file_comparing_4_tools_with_timeout(read_file, write_file)
    # print(f' \033[31m functions whose value < 0: {fun_whose_function_value_less_than_0}\033[0m')
    print(f'succeed function value to bring into the original constraint: {succeed_function_value}')
    '''
    benchmark = 'jfs'
    read_file = benchmark + '/mpcs_result_for_constructing_final_after_negation.csv'
    write_file = benchmark + '/mpcs_result_for_solving_final_after_negation.csv'
    final_file = benchmark + '/mpcs_result_for_solving_final.csv'
    solve_negation_unsat(read_file, write_file, final_file)
    '''

    # solve_one_function('griggio/fmcad12/mult2.c.3.smt2',7)
    # griggio/fmcad12/test_v3_r8_vr10_c1_s4660.smt2
