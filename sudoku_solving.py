#!/usr/bin/python
# -*- coding: utf-8 -*-


sudoku_candidate = [[]] * 81  

def check_candidate_unique(sudoku):  
   
    for i in range(len(sudoku)):  
        row = i/9
        if len(sudoku_candidate[i]) != 1:  #if sudoku[i] != 0:
            for j in range(0,9): 
                for value in sudoku_candidate[row*9 + j]:  
                    flag = False
                    for _j in range(0,9):  
                        if _j != j:
                            if value in sudoku_candidate[row*9 + _j]:
                                flag = True  
                                break
                    if flag is False: 
                        sudoku[row*9 + j] = value
                        candidate = [value]
                        sudoku_candidate[row*9 + j] = candidate[:]
                        break

    for col in range(0,9): 
        for row in range(0,9):
            i = row*9 + col 
            if sudoku[i] != 0:
                for j in range(0,9):  
                    for value in sudoku_candidate[j*9 + col]: 
                        flag = False
                        for _j in range(0,9): 
                            if _j != j:
                                if value in sudoku_candidate[_j*9 + col]:
                                    flag = True
                                    break
                        if flag is False:  
                            sudoku[j*9 + col] = value
                            candidate = [value]
                            sudoku_candidate[j*9 + col] = candidate[:]
                            break

    for i in range(len(sudoku)):  
        row = i/9
        col = i%9
        if sudoku[i] != 0:
            for k in range(0,3):
                for t in range(0,3):
                    for value in sudoku_candidate[(row/3*3+k)*9 + col/3*3+t]:  
                        flag = 'False'
                        for _k in range(0,3):  
                            for _t in range(0,3):
                                if _k != k or _t != t:
                                    if value in sudoku_candidate[(row/3*3+_k)*9 + col/3*3+_t]:
                                        flag = 'True'
                                        break
                            if flag == 'True':
                                break
                        if flag == 'False':
                            sudoku[(row/3*3+k)*9 + col/3*3+t] = value
                            candidate = [value]
                            sudoku_candidate[(row/3*3+k)*9 + col/3*3+t] = candidate[:]
                            break

def init_sudoku_candidate(sudoku):  
    for i in range(len(sudoku)):
        if sudoku[i] == 0:
            candidate = [1,2,3,4,5,6,7,8,9]
        else:
            candidate = [sudoku[i]]
        sudoku_candidate[i] = candidate[:]

def update_sudoku_row(sudoku):  
    for i in range(len(sudoku)):
        row = i/9
        if sudoku[i] != 0:
            for j in range(0,9):  
                if sudoku[i] in sudoku_candidate[row*9 + j] and len(sudoku_candidate[row*9 + j]) > 1:
                    sudoku_candidate[row*9 + j].remove(sudoku[i])  
        if len(sudoku_candidate[i]) == 1:  
            sudoku[i] = sudoku_candidate[i][0]

def update_sudoku_col(sudoku):  
    for col in range(0,9):
        for row in range(0,9):
            i = row*9 + col  
            if sudoku[i] != 0:
                for j in range(0,9):  
                    if sudoku[i] in sudoku_candidate[j*9 + col] and len(sudoku_candidate[j*9 + col]) > 1:
                        sudoku_candidate[j*9 + col].remove(sudoku[i])
            if len(sudoku_candidate[i]) == 1:
                sudoku[i] = sudoku_candidate[i][0]

def update_sudoku_grid(sudoku):  
    for i in range(len(sudoku)):
        row = i/9
        col = i%9
        if sudoku[i] != 0:
            for k in range(0,3):  
                for t in range(0,3):
                    if sudoku[i] in sudoku_candidate[(row/3*3+k)*9 + col/3*3+t] and len(sudoku_candidate[(row/3*3+k)*9 + col/3*3+t]) > 1:
                        sudoku_candidate[(row/3*3+k)*9 + col/3*3+t].remove(sudoku[i])
        if len(sudoku_candidate[i]) == 1:
            sudoku[i] = sudoku_candidate[i][0]

def out_sudoku(sudoku):
    for i in range(len(sudoku)):
        print sudoku[i],
        if (i+1)%9 == 0:
            print
    print '-'*50

def sudoku_solving(sudoku):
   
    init_sudoku_candidate(sudoku)
    i = 0
    ret = 0
    while True:  
        update_sudoku_row(sudoku)
        update_sudoku_col(sudoku)
        update_sudoku_grid(sudoku)
        check_candidate_unique(sudoku)
        if 0 not in sudoku:
            ret = 0
            break
        i += 1
        if i >= 5:  
            ret = -1
            break
    # print i,'+'*10
    return ret

if __name__ == '__main__':
    sudoku = [
        0, 9, 0, 1, 0, 0, 3, 7, 8,
        0, 0, 0, 7, 0, 9, 0, 0, 0,
        0, 1, 0, 4, 0, 8, 0, 0, 6,
        0, 0, 0, 2, 0, 0, 6, 5, 9,
        0, 0, 0, 0, 4, 3, 0, 0, 0,
        0, 5, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 2, 3, 5, 1, 7, 0, 0,
        0, 6, 0, 8, 9, 0, 5, 0, 2,
        0, 0, 0, 0, 0, 2, 8, 0, 0
    ]

    # sudoku = [
        # 0,0,0,0,0,0,8,0,0,
        # 4,0,0,2,0,8,0,5,1,
        # 0,8,3,9,0,0,0,0,7,
        # 0,4,0,5,0,0,0,8,2,
        # 0,0,5,0,0,0,4,0,0,
        # 8,7,0,0,0,9,0,3,0,
        # 2,0,0,0,0,7,1,6,0,
        # 3,6,0,1,0,5,0,0,4,
        # 0,0,4,0,0,0,0,0,0
    # ]

    ret = sudoku_solving(sudoku)
    out_sudoku(sudoku)
