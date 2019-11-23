# -*- coding: utf-8 -*-
import re
import copy
import os, sys, glob
from shutil import copyfile

# from itertools import izip as zip, count # izip for maximum efficiency
# pathToFile = os.path.abspath(os.path.dirname(sys.argv[0]))
# pathToFile2 = 'C:\\User\\I.Nuriakhmetov\\Desktop\\filefoMichail'


def get_contents(path_to_file):
    with open(path_to_file) as fileStream:
        data = fileStream.read()
        fileStream.close()
        # print(data)
        return data

def put_contents(path_to_file, contents):
    open(path_to_file, 'w').write(contents)

def get_path_to_solver_file(paths_to_files, solver_key):
    for path_to_file in paths_to_files:
        for line in open(path_to_file).read().splitlines():
            if solver_key == line:
                return path_to_file

    return None

def get_subcases_and_loads_line_indexes(lines):
    subcases_and_loads_line_indexes = dict()
    subcase_line_index = None
    is_subcase_body = False

    for index, line in enumerate(lines):
        if '$' == line[0]:
            continue
        if is_subcase_body and '   ' == line[:3]:
            print('1')
            if 'LOAD' == line[3:7]:
                print('2')
                subcases_and_loads_line_indexes[subcase_line_index] = index
                print(subcases_and_loads_line_indexes)
        elif 'SUBCASE' == line[:7]:

            subcase_line_index = index
            is_subcase_body = True
            print('3', index)
        else:
            # print('4')
            is_subcase_body = False

    return subcases_and_loads_line_indexes

def insert_subcases_with_loads(lines, new_lines, subcases_and_loads_line_indexes):
    is_subcase_body = False
    subcase = load = index_after_subcase_1 = None

    for index, line in enumerate(lines):
        if '$' == line[0]:
            continue
        if is_subcase_body and '   ' != line[:3]:
            # lines.insert(index, subcase + "\n" + load)
            lines.insert(index, subcase)
            lines.insert(index + 1, load)
            index_after_subcase_1 = index + 1
            is_subcase_body = False

        for new_subcase_line_index, new_load_line_index in subcases_and_loads_line_indexes.items():
            if line == new_lines[new_subcase_line_index]:
                is_subcase_body = True
                subcase = line
                load = new_lines[new_load_line_index]
                lines[index] = '$ ' + line

    if index_after_subcase_1 is not None:
        for index, (new_subcase_line_index, new_load_line_index) in enumerate(subcases_and_loads_line_indexes.items()):
            if 0 == index:
                continue

            lines.insert(index_after_subcase_1 + (index * 2) - 1, new_lines[new_subcase_line_index])
            lines.insert(index_after_subcase_1 + (index * 2), new_lines[new_load_line_index])
            # lines.insert(index_after_subcase_1 + index,
            #              new_lines[new_subcase_line_index] + "\n" + new_lines[new_load_line_index])

    return lines

def main():
    solver_key_1 = 'SOL 103'
    solver_key_2 = 'SOL 101'
    os.chdir(os.path.abspath(os.curdir))
    paths_to_files = glob.glob('*.bdf')
    path_to_result_file_name = paths_to_files[0].split('_')[0] + '_nm_loads.bdf'

    if path_to_result_file_name in paths_to_files:
        paths_to_files.remove(path_to_result_file_name)

    path_to_solver_1_file = get_path_to_solver_file(paths_to_files, solver_key_1)
    path_to_solver_2_file = get_path_to_solver_file(paths_to_files, solver_key_2)

    if path_to_solver_1_file is None:
        raise Exception('Solver 1 file is not found!')

    if path_to_solver_2_file is None:
        raise Exception('Solver 2 file is not found!')

    # print([path_to_solver_1_file, path_to_solver_2_file])

    solver_2_file_lines = open(path_to_solver_2_file).read().splitlines()
    subcases_and_loads_line_indexes = get_subcases_and_loads_line_indexes(solver_2_file_lines)
    print(subcases_and_loads_line_indexes)

    copyfile(path_to_solver_1_file, path_to_result_file_name)

    result_file_lines = open(path_to_result_file_name).read().splitlines()

    lines = insert_subcases_with_loads(result_file_lines, solver_2_file_lines, subcases_and_loads_line_indexes)

    # print("\n".join(lines))
    # raise Exception('Exit')

    counttext = '$ Loads for Load Case :'
    replacementtext1 = '$ Referenced Coordinate Frames'
    textforreplace = "\n".join(lines)
    counttextnumber = 0

    for i in lines:
        if counttext in i:
            counttextnumber += 1
    print(counttextnumber)

    if counttextnumber < 2 and replacementtext1 in textforreplace:
        indexofreplacementtext1 = textforreplace.index(replacementtext1)
        sizeofreplacementtext = textforreplace[indexofreplacementtext1:]
        txt = ''
        textforreplace = textforreplace.replace(sizeofreplacementtext, txt)
        open(path_to_result_file_name, 'w').write(textforreplace)


    strwithendtext = solver_2_file_lines
    tx5 ='$ Loads for Load Case :'

    n = 0
    for i in strwithendtext:
        if tx5 in i:
            index = n
            break
        n += 1

    diapozon = strwithendtext[index:] #выделение необходимого диапазона
    tx7 = '$ Displacement Constraints of Load Set'
    tx8 = '$ Pressure Loads of Load Set'

    flag1 = False
    flag2 = False
    for i in diapozon:
        if tx7 in i:
            indextx7 = diapozon.index(i)
            flag1 = True
        if tx8 in i:
            indextx8 = diapozon.index(i)
            flag2 = True

    if flag2 == True and flag1 == True:
        del diapozon[indextx7:indextx7 + 1]
    print(diapozon)

    #textend = getFileContent(pathToFile + '\\' + solkey2file)
    #tx6 = ''
    #indextx5 = textend.index(tx5)
    #endtext = textend[indextx5:]
    #print('end:', endtext)

    textfinish = get_contents(path_to_result_file_name)
    textfinish1 = open(path_to_result_file_name)
    textfinish2 = textfinish1.readlines()
    textfinish1.close()
    n=0
    count = 0
    for i in diapozon:
        if i in textfinish2: # проверка вхождения диапозона из солвера 101 в 103, добавление его при отсутствии
            count += 1
        else:
            count -= 1

    elementsin = count >= 4

    print(elementsin)
    if elementsin == False:
        ff = open(path_to_result_file_name, '+a')
        for i in range(len(diapozon)):
            ff.write(diapozon[i] + "\n")
        ff.close()
    print(count)

main()



































"""
tx7 = '$ Displacement Constraints of Load Set'
tx8 = '$ Pressure Loads of Load Set'
if tx7 in textfinish:                       # проверка условия вхождения строк tx7,tx8 и их дальнейшее удаление
    if tx8 in textfinish:
        indextx7 = textfinish.index(tx7)
        indextx8 = textfinish.index(tx8)
        indextx9 = textfinish[indextx8 + len(tx8):].index(tx8) + indextx8 + len(tx8)
        finishtext = textfinish[indextx7:indextx9]
        textfinish = getFileContent(pathToFile + '\\' + apndx).replace(finishtext, '')
        fff = open(pathToFile + '\\' + apndx, 'w').write(textfinish)
"""
    #fff.close()
#print(textfinish)
"""
textold = getFileContent(pathToFile + '\\' + solkey2file)
tx1 = 'SUBCASE 1'
tx11 = '$ Subcase'
tx2 = '   ' + 'LOAD'
tx22 = '   DISPLACEMENT('
indextx1 = textold.index(tx1)
indextx11 = textold.index(tx11)
indextx2 = textold.index(tx2)
indextx22 = textold.index(tx22)
oldtext1 = textold[indextx1:indextx11]
oldtext2 = textold[indextx2:indextx22]
oldtext = oldtext1 + oldtext2
print('old:', oldtext1, 'old2:', oldtext2)

textnew = getFileContent(pathToFile + '\\' + apndx)
tx3 = 'SUBCASE 1'
tx4 = '   '
#tx33 = ''
#tx4 = '$ Direct Text Input for this Subcase'
tx11 = '$ Direct'
tx22 = '$ SUBCASE'
indextx3 = textnew.index(tx3)
indextx4 = textnew.index(tx4)
newtext = textnew[indextx3:indextx4]

textforchanges = getFileContent(pathToFile + '\\' + apndx).replace(newtext, oldtext)
f = open(pathToFile + '\\' + apndx,'w').write(textforchanges)

#oldtext - заменяемый текстs
#newtext - то, на что заменяется

textend = getFileContent(pathToFile + '\\' + solkey2file)
tx5 ='$ Loads for Load Case : Default'
tx6 = ''
indextx5 = textend.index(tx5)
indextx6 = textend.index(tx6)+ len(tx6)
endtext = textend[indextx5:]
ff = open(pathToFile + '\\' + apndx,'a+').write(endtext + '\n')
textfinish = getFileContent(pathToFile + '\\' + apndx)
#print('____',textfinish)
print('textfinish:', textfinish)
tx7 = '$ Displacement Constraints of Load Set'
tx8 = '$ Pressure Loads of Load Set'
indextx7 = textfinish.index(tx7)
indextx8 = textfinish.index(tx8)
indextx9 = textfinish[indextx8 + len(tx8):].index(tx8) + indextx8 + len(tx8)
#if tx8 in textfinish:
 #   indextx8 = textfinish.index(tx8)
  #  for n in range(2):
   #     n=n+1
    #    list.append(indextx8)
#print(list)

#if indextx7 <= indextx8:
#for tx8 in textfinish:
 #   k=k+1
#print(k)
 #else:
finishtext = textfinish[indextx7:indextx9]
textfinish = getFileContent(pathToFile + '\\' + apndx).replace(finishtext, '')
fff = open(pathToFile + '\\' + apndx, 'w').write(textfinish)
print(indextx7, indextx9, 'finish:', finishtext)
пропустить ввиду несостоятельности кода
"""









