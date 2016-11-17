#!/usr/bin/python
# -*- coding: utf-8 -*-


from sudoku_solving import sudoku_solving

global DIFICULTY                    #values between 1-50
DIFICULTY       = 1                 #default value

def get_random_num(sudoku,index):  
   
    candidate = [1,2,3,4,5,6,7,8,9]

    row = index/9
    col = index%9

    grid_x = row/3*3
    grid_y = col/3*3

    j = 0
    while j < col:
        if sudoku[row*9 + j] in candidate:
            candidate.remove(sudoku[row*9 + j])
        j += 1

    i = 0
    while i < row:
        if sudoku[i*9 + col] in candidate:
            candidate.remove(sudoku[i*9 + col])
        i += 1

    for _i in range(0,3):
        for _j in range(0,3):
            if sudoku[(grid_x+_i)*9 + grid_y+_j] in candidate:
                candidate.remove(sudoku[(grid_x+_i)*9 + grid_y+_j])

    if len(candidate) == 0: 
        random_num = -1
    else:
        random_num = random.choice(candidate) 

    return random_num

def sudoku_generate_backtracking(): 
   
    sudoku = [0] * 81
    # for i in range(0,81):
    i = 0
    while i < 81:
        random_num = get_random_num(sudoku,i)  
        if random_num == -1:  
            sudoku = [0] * 81
            i = 0
        else:
            sudoku[i] = random_num
            i += 1
    return sudoku


def sudoku_puzzle_dibble(sudoku):  
    
    global DIFICULTY

    while True:
        sudoku_dibble = sudoku[:]
        i = 0
        while i < DIFICULTY:  
            random_index = random.choice(range(0,81))  
            if sudoku_dibble[random_index] != 0:
                sudoku_dibble[random_index] = 0
            else:  
                i -= 1
            i += 1
        sudoku_tmp = sudoku_dibble[:]
        ret = sudoku_solving(sudoku_tmp)  
        if ret != 0:  
            continue
        if sudoku_tmp == sudoku:  
            #----prints----#
            #out_sudoku(sudoku)
            #out_sudoku(sudoku_dibble)
            return sudoku, sudoku_dibble
            #break

def out_sudoku(sudoku):
    for i in range(len(sudoku)):
        # print str(sudoku[i])+',',
        print sudoku[i],

        if (i+1)%9 == 0:
            print
    print '-'*50

def generator():
    sudoku  = sudoku_generate_backtracking()    
    return sudoku_puzzle_dibble(sudoku)

def set_dificulty(value):
    global DIFICULTY
    DIFICULTY = int(value)

if __name__ == '__main__':
    sudoku = sudoku_generate_backtracking()
    sudoku_puzzle_dibble(sudoku)
