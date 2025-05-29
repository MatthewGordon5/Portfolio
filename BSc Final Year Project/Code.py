import random, copy, time, matplotlib.pyplot as plt

# HOW TO USE --------------------------------------------------------------------
    
'''Comments on how to use:
        Run main_menu(killers) to activate user interface
        Run results_generator(killers,puzzles_generated) to generate results
            After running results_generator(killers,puzzles_generator) run analytics_seperate(analytics_list) 
            to split the results into lists for just easy, medium or hard difficulty puzzles
            Once this is done you can uncomment list_analytics and the plots to generate graphs and analytics
            for each difficulty.
        If you just want to generate one puzzle, run generator(killers,puzzles_generated).'''

# GENERATION CODE-----------------------------------------------

# GENERATING SOLUTION CODE

def generate_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    numbers = list(range(1, 10))

    # Randomize the order in which numbers are tried
    random.shuffle(numbers)

    # Use backtracking to fill the grid
    if backtracker_sudoku(grid,numbers):
        return grid
    else:
        # If no solution is found, try generating again
        return False

def backtracker_sudoku(grid,numbers):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid_sudoku(grid, row, col, num):
                        grid[row][col] = num
                        if backtracker_sudoku(grid, numbers):
                            return True
                        # If this doesn't lead to a solution, backtrack
                        grid[row][col] = 0
                # If no valid number is found, return False
                return False
    # If all cells are filled, return True
    return True

def is_valid_sudoku(grid, row, col, num):
    # Check if the number exists in the row
    if num in grid[row]:
        return False

    # Check if the number exists in the column
    if num in [grid[i][col] for i in range(9)]:
        return False

    # Check if the number exists in the 3x3 box
    box_row = 3 * (row // 3)
    box_col = 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False

    return True

# GENERATING SOLUTION CODE ENDS

# GENERATING CAGES

def generate_seed_cells(cages_num):
    cells = [[row, col] for row in range(9) for col in range(9)]
    
    starter_seeds = [[0,0],[0,4],[0,8],[4,0],[4,8],[8,0],[8,4],[8,8]]
    
    seeds = starter_seeds[:]
    
    for seed in seeds:
        cells.remove(seed)
    
    # 10 ungrowable seeds
    ungrowables = []
    for j in range(10):
        seed = random.choice(cells)
        cells.remove(seed)
        seeds.append(seed)
    
    
    num_of_cages = cages_num - len(seeds) - len(ungrowables)
    

    for i in range(num_of_cages):
        seed2 = random.choice(cells)
        cells.remove(seed2)
        seeds.append(seed2)
        
    return seeds,ungrowables

def find_neighbours(cage,cage_cells):
    
    pot_neighbours = []

    #Goes through each cell in the cage
    for i in cage:
        seed_x = i[0]
        seed_y = i[1]
        
        #Neighbours must be inside the grid
        if seed_x - 1 >= 0:
            pot_neighbours.append([seed_x-1,seed_y])
            
        if seed_x + 1 <= 8:
            pot_neighbours.append([seed_x+1,seed_y])
            
        if seed_y - 1 >= 0:
            pot_neighbours.append([seed_x,seed_y-1])
            
        if seed_y + 1 <= 8:
            pot_neighbours.append([seed_x,seed_y+1])
            
    #Neighbours can only appear once in the neighbours list
    unique_neighbours = []
    for k in pot_neighbours:
        if k not in unique_neighbours:
            unique_neighbours.append(k)

    #Neighbours must not be in other cages  
    for j in cage_cells:
        if j in unique_neighbours:
            unique_neighbours.remove(j)

    return unique_neighbours

#NEED TO IMPORT NUM OF CAGES OR MERGE SEEDS WITH GEN CAGES

def generate_cages(cages_num):
    #Generate seeds
    seeds,ungrowables = generate_seed_cells(cages_num)
    
    
    #Generate empty cages
    cages = [[] for i in range(cages_num)]

    for j in range(cages_num):
        cages[j].append(seeds[j])
        
    #Each seed cell is in a cage
    cage_cells = seeds[:]
    
    while len(cage_cells) < 81:

        for cage in cages:
            
            x = find_neighbours(cage,cage_cells)
            
            if len(x) >= 1 and x not in ungrowables:
                y = random.choice(x)
                cage.append(y)
                cage_cells.append(y)
    
    return cages

def check_for_duplicates(list):
    return len(list) != len(set(list))


# This function regenerates cages and solutions until the cages do not contain any duplicate values
def generate_eligable_cages(cages_num):

    cages = generate_cages(cages_num)
    grid = generate_grid()
    
    while True:
        
        duplicates_found = False
        #Checks for same number in same cage

        for cage in cages:
            cell_value = [grid[cell[0]][cell[1]] for cell in cage]
            
            if check_for_duplicates(cell_value):
                #if there are 2 of the same number in the same cage, 
                #generate the grid and cages again
                duplicates_found = True
                break
            
        if not duplicates_found:
            break
        
        cages = generate_cages(cages_num)
        grid = generate_grid()
        
    return cages,grid

# GENERATING CAGES CODE ENDS

# GENERATING CAGE VALUES CODE

def assign_cage_values(cages,grid):
    
    #Sorts the cells inside each cage
    for i in cages:
        i.sort()
    
    #Sorts the cages in order using the first cell in each cage
    cages.sort()
            
    #Finds the value of each cage
    cage_values = []
    cage_value = 0
    for cage in cages:
        cage_values.append(cage_value)
        cage_value = 0
        for cell in cage:
            cage_value += grid[cell[0]][cell[1]]
            
    #Add in the last cage value to the list
    cage_values.append(cage_value)
    #Delete the 0 at the start of the list
    del cage_values[0]
        
    return cages, cage_values

#GENERATING CAGE VALUES CODE ENDS

# GENERATING PUZZLE CODE
        
def puzzle_generator(cages_num):
    
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    cages_initial,grid_initial = generate_eligable_cages(cages_num)
    
    cages,values = assign_cage_values(cages_initial,grid_initial)
    
    killer = []

    killer.append(cages)
    killer.append(values)
    killer.append(grid)
    
    return killer

# GENERATING PUZZLE CODE ENDS

# GENERATOR CODE ENDS----------------------------------------------

# SOLVER CODE

# INITIAL STEPS CODE

# KILLER COMBINATIONS CODE


# KILLER COMBOS CODE

def find_combinations(cage,value):
    
    size = len(cage)
    
    result = []
    combo_search(1,size,value,[],result)
    
    return result

def combo_search(start,size,value,path,result):
    
    # If size = 0 and value needed = 0 then weve done it
    if size == 0 and value == 0:
        result.append(path)
        return
    
    # If size = 0 and value does not = 0 or
    # If value less than 0 weve failed
    if size == 0 or value <= 0:
        return
    
    # Try numbers from start to 9 where start keeps track of the numbers weve already tried
    for num in range(start,10):
        if num > value:
            break
        
        # Try the next number along until we run out of numbers
        combo_search(num+1,size-1,value-num,path + [num],result)
        
    return result

def possible_cell_values(combinations):
    
    possible_numbers = []
    
    for combination in combinations:
        for num in combination:
            possible_numbers.append(num)

        
    # We only want each possibility to appear once
    
    unique_possible_numbers = []
    
    for number in possible_numbers:
        if number not in unique_possible_numbers:
            unique_possible_numbers.append(number)
            
    # We want them sorting into order
    unique_possible_numbers.sort()
            
    return unique_possible_numbers

    
def find_cage(row,col,killer):
    
    for cage in killer[0]:
        for cell in cage:
            if cell == [row,col]:
                return cage
    
    return False

def find_cage_value(cage,killer):
    cage_index = killer[0].index(cage)
    return killer[1][cage_index]


def killer_combinations(grid,killer):
    
    for row in range(9):
        for col in range(9):
            cage = find_cage(row,col,killer)
            value = find_cage_value(cage,killer)
            combinations = find_combinations(cage,value)
            potentials = possible_cell_values(combinations)
            grid[row][col] = potentials
            
    return grid

# KILLER COMBINATIONS CODE END

def initial_steps(grid,killer):
    
    puzzle = killer_combinations(grid,killer)

    return puzzle

# INITIAL STEPS CODE END

# SIMPLE ELIM CODE

def row_remover(grid):
    
    for row in grid:
        for col in range(9):
            if len(row[col]) > 1:
                for pos in range(9):
                    if len(row[pos]) == 1 and row[pos][0] in row[col]:
                        row[col].remove(row[pos][0])
                        break
                        
    return grid

def col_remover(grid):
    
    for row in grid:
        for col in range(9):
            if len(row[col]) > 1:
                for pos in range(9):
                    if len(grid[pos][col]) == 1 and grid[pos][col][0] in row[col]:
                        row[col].remove(grid[pos][col][0])
                        break
                        
    return grid

def box_remover(grid):
    
    for row in range(9):
        for col in range(9):
            if len(grid[row][col]) > 1:
                box_row = (row // 3) * 3
                box_col = (col // 3) * 3
                for b_row in range(box_row,box_row + 3):
                    for b_col in range(box_col,box_col + 3):
                        if len(grid[b_row][b_col]) == 1 and grid[b_row][b_col][0] in grid[row][col]:
                            grid[row][col].remove(grid[b_row][b_col][0])
                            break
                        
    return grid
                        

def simple_elim(grid):
    
    grid_reduced = row_remover(grid)
    grid_reduced2 = col_remover(grid_reduced)
    grid_reduced3 = box_remover(grid_reduced2)
    
    return grid_reduced3
    

# SIMPLE ELIM CODE END

# HIDDEN CODE

def hidden_rows(grid):

    for num in range(1,10):
        for row in range(9):
            appears = []
            for col in range(9):
                if num in grid[row][col]:
                    appears.append([row,col])
                    
            if len(appears) == 1:
                #we have a hidden single in this row
                grid[appears[0][0]][appears[0][1]] = [num]
                
    return grid
    
def hidden_cols(grid):
    
    for num in range(1,10):
        for col in range(9):
            appears = []
            for row in range(9):
                if num in grid[row][col]:
                    appears.append([row,col])
                    
            if len(appears) == 1:
                grid[appears[0][0]][appears[0][1]] = [num]
                
    return grid

def hidden_box(grid):
    
    for num in range(1,10):
        
        for row in range(9):
            for col in range(9):
                box_row = (row // 3) * 3
                box_col = (col // 3) * 3
                appears = []
                
                for b_row in range(box_row, box_row + 3):
                    for b_col in range(box_col, box_col + 3):
                        if num in grid[b_row][b_col]:
                            appears.append([b_row,b_col])
                            
                if len(appears) == 1:
                    grid[appears[0][0]][appears[0][1]] = [num]
                    return grid
                        
    return grid
        

def hidden_singles(grid):
    
    grid_reduced = hidden_rows(grid)
    grid_reduced2 = hidden_cols(grid_reduced)
    grid_reduced3 = hidden_box(grid_reduced2)
    
    return grid_reduced3
    

# HIDDEN CODE END

# POINTING CODE

def pointing_rows(grid):
    for num in range(1, 10):
        for row in range(9):
            for col in range(9):
                box_row = (row // 3) * 3
                box_col = (col // 3) * 3
                index = [i for i in range(9)]
                index.remove(box_col)
                index.remove(box_col + 1)
                index.remove(box_col + 2)
                
                box_count = 0
                for b_row in range(box_row, box_row + 3):
                    for b_col in range(box_col, box_col + 3):
                        if num in grid[b_row][b_col]:
                            box_count += 1
                            
                row_count = 0
                for r_col in range(box_col, box_col + 3):
                    if num in grid[row][r_col]:
                        row_count += 1
                        
                if box_count == row_count and box_count != 0:
                    for item in index:
                        if len(grid[row][item]) > 1 and num in grid[row][item]:
                            grid[row][item].remove(num)
    return grid


def pointing_cols(grid):
    for num in range(1, 10):
        for row in range(9):
            for col in range(9):
                box_row = (row // 3) * 3
                box_col = (col // 3) * 3
                index = [i for i in range(9)]
                index.remove(box_row)
                index.remove(box_row + 1)
                index.remove(box_row + 2)
                
                box_count = 0
                for b_row in range(box_row, box_row + 3):
                    for b_col in range(box_col, box_col + 3):
                        if num in grid[b_row][b_col]:
                            box_count += 1
                            
                col_count = 0
                for r_row in range(box_row, box_row + 3):
                    if num in grid[r_row][col]:
                        col_count += 1
                        
                if box_count == col_count and box_count != 0:
                    for item in index:
                        if len(grid[item][col]) > 1 and num in grid[item][col]:
                            grid[item][col].remove(num)
    return grid


def pointing_reduction(grid):
    
    grid_reduced = pointing_rows(grid)
    grid_reduced2 = pointing_cols(grid_reduced)
    
    return grid_reduced2

# POINTING CODE END

# BOX LINE CODE

def box_line_row(grid):
    
    for num in range(1,10):
    
        for row in range(9):
    
            box_row = (row // 3) * 3
            row_index = [i for i in range(box_row,box_row + 3) if i != row]
            
            #how many times does num appear in row
            row_count = 0
            for col in range(9):
                if len(grid[row][col]) > 1 and num in grid[row][col]:
                    row_count += 1
                    
            #check each box
            box_count = []
            for col2 in range(0,9,3):
                
                #how many times does num appear in this box in the original row
                count = 0
                for box_col in range(col2,col2 + 3):
                    if len(grid[row][box_col]) > 1 and num in grid[row][box_col]:
                        count += 1
                box_count.append(count)
                
            for item in box_count:
                if item == row_count and row_count != 0:
                    index = box_count.index(item)
                    box_col2 = index * 3
                    
                    for r_row in row_index:
                        for r_col in range(box_col2,box_col2 + 3):
                            if len(grid[r_row][r_col]) > 1 and num in grid[r_row][r_col]:
                                grid[r_row][r_col].remove(num)

    return grid

def box_line_col(grid):
    
    for num in range(1,10):
    
        for col in range(9):
    
            box_col = (col // 3) * 3
            col_index = [i for i in range(box_col,box_col + 3) if i != col]
            
            #how many times does num appear in row
            col_count = 0
            for row in range(9):
                if len(grid[row][col]) > 1 and num in grid[row][col]:
                    col_count += 1
                    
            #check each box
            box_count = []
            for row2 in range(0,9,3):
                
                #how many times does num appear in this box in the original row
                count = 0
                for box_row in range(row2,row2 + 3):
                    if len(grid[box_row][col]) > 1 and num in grid[box_row][col]:
                        count += 1
                box_count.append(count)
                
            for item in box_count:
                if item == col_count and col_count != 0:
                    index = box_count.index(item)
                    box_row2 = index * 3
                    
                    for r_row in range(box_row2,box_row2 + 3):
                        for r_col in col_index:
                            if len(grid[r_row][r_col]) > 1 and num in grid[r_row][r_col]:
                                grid[r_row][r_col].remove(num)

    return grid

def box_line_reduction(grid):
    
    grid_reduced = box_line_row(grid)
    
    grid_reduced2 = box_line_col(grid_reduced)
            
    return grid_reduced2

# SOLVER CODE

# grid input must be a grid of all zeros
# no starting numbers
# keeps applying pen and papers until no further changes are made

def solver(puzzle,simpleE,hidden,pointing,boxline):
    
    puzzle_copy = copy.deepcopy(puzzle)
    puzzle = simple_elim(puzzle)
    if not puzzle_copy == puzzle:
        simpleE[0] += 1
        solver(puzzle,simpleE,hidden,pointing,boxline)
    else:
        puzzle_copy = copy.deepcopy(puzzle)
        hidden_singles(puzzle)
        if not puzzle_copy == puzzle:
            hidden[0] += 1
            solver(puzzle,simpleE,hidden,pointing,boxline)
        else:
            puzzle_copy = copy.deepcopy(puzzle)
            puzzle = pointing_reduction(puzzle)
            if not puzzle_copy == puzzle:
                pointing[0] += 1
                solver(puzzle,simpleE,hidden,pointing,boxline)
            else:
                puzzle_copy = copy.deepcopy(puzzle)
                puzzle = box_line_reduction(puzzle)
                if not puzzle_copy == puzzle:
                    boxline[0] += 1
                    solver(puzzle,simpleE,hidden,pointing,boxline)
                    
    return puzzle

def list_to_int(puzzle):
    for row in puzzle:
        for cols in range(9):
            if len(row[cols]) == 1:
                row[cols] = row[cols][0]
            else:
                row[cols] = 0
                
    return puzzle

# PRINTING CODE

def print_killer(killer):
    
    cage_no = 1
    for i in killer[0]:
        print("Cage",cage_no,"contains cells", i,"and has value",killer[1][cage_no-1])
        cage_no += 1
        
    print("Grid after solver:")
        
    for row in killer[2]:
        print(" ".join(map(str, row)))
        
# PRINTING CODE ENDS

# UNIQUE SOLUTION CODE

# SOLVER FORWARDS AND SOLVER BACKWARDS INPUT GRID AS
# THE FINAL IDEA IS TO RUN MY SOLVER FIRST TO TRY AND GET SOME NUMBERS SO THAT
# THE BACKTRACKER CAN FINISH UP

def solver_forwards(grid,killer):
    
    numbers = list(range(1, 10))
    counter = [0]

    # Use backtracking to fill the grid
    if backtracker(grid,numbers,killer,counter):
        print("Iterations:", counter[0])
        return grid
    else:
        # If no solution is found, alert
        return False
    
def solver_backwards(grid,killer):
    
    numbers = list(range(1, 10))
    numbers.reverse()
    counter = [0]

    # Use backtracking to fill the grid
    if backtracker(grid,numbers,killer,counter):
        print("Iterations:", counter[0])
        return grid
    else:
        # If no solution is found, alert
        return False

def backtracker(grid, numbers, killer, counter):
    
    counter[0] += 1
    if counter[0] >= 100000:
        return False

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in numbers:
                    if is_move_valid_killer(grid, row, col, num, killer):
                        grid[row][col] = num
                        if backtracker(grid, numbers, killer, counter):
                            return True
                        # If this doesn't lead to a solution, backtrack
                        grid[row][col] = 0
                # If no valid number is found, return False
                return False
    # If all cells are filled, return True
    return True

def is_move_valid_killer(grid,row,col,num,killer):
    # Check if the number is valid in the current cell
    if not is_valid_sudoku(grid,row,col,num):
        return False
    
    # Check if adding the number exceeds the cage value
    if not is_valid_killer(grid,row,col,num,killer):
        return False
    
    return True

def is_valid_killer(grid,row,col,num,killer):
    # Find the cage and its value
    cage = find_cage(row, col, killer)
    value = find_cage_value(cage, killer)

    # Check if adding the number would exceed the cage value
    current_sum = sum(grid[cell[0]][cell[1]] for cell in cage if grid[cell[0]][cell[1]] != 0)
    if current_sum + num > value:
        return False
    
    #NEED TO CHECK IF THE VALUE IS CORRECT SOMEHOW

    # Check if the number already exists in the cage
    if num in [grid[cell[0]][cell[1]] for cell in cage]:
        return False

    return True

def unique_solution(killer):
    
    grid = killer[2]
    
    # ANALYTICS CODE
    analytics = []
    
    simpleE = [0]
    hidden = [0]
    pointing = [0]
    boxline = [0]

    #track time
    start_time = time.time()
    
    grid2 = initial_steps(grid,killer)
    grid3 = solver(grid2,simpleE,hidden,pointing,boxline)
    grid4 = list_to_int(grid3)
    
    #track time
    end_time = time.time()
    execution_time = end_time - start_time
    
    breakdown = []
    
    breakdown.append(simpleE)
    breakdown.append(hidden)
    breakdown.append(pointing)
    breakdown.append(boxline)
    
        
    cage_num = 0
    for j in killer[0]:
        cage_num += 1
        
    difficulty = 0
    
    if cage_num <= 38:
        difficulty = 3
    
    if 39 <= cage_num <=42:
        difficulty = 2
    
    if cage_num >=43 :
        difficulty = 1
        
    solved_counter = 0
    for row in range(9):
        for col in range(9):
            if grid4[row][col] != 0:
                solved_counter += 1
                
    perc_solved = solved_counter / 81
    
    perc_solved2 = perc_solved * 100
    
    analytics.append([difficulty])
    analytics.append([execution_time])
    analytics.append([perc_solved2])
    analytics.append(breakdown)
    
    #ANALYTICS END
    
    grid5 = copy.deepcopy(grid4)

    grid6 = copy.deepcopy(grid4)
    
    solved_forwards = solver_forwards(grid5,killer)

    solved_backwards = solver_backwards(grid6,killer)
    
    if solved_forwards == False or solved_backwards == False:
        print("Unable to find unique solution within iteration limit")
        print("Generating fresh puzzle")
        return False,analytics
    
    if solved_forwards == solved_backwards and solved_forwards != False:
        killer.append(solved_forwards)
        print("Puzzle found")
        return killer,analytics
    
    if solved_forwards != False and solved_backwards != False and solved_forwards != solved_backwards:
        print("Puzzle did not have a unique solution")
        print("Generating fresh puzzle")
        
    
    return False,analytics

    
# UNIQUE SOLUTION CODE ENDS

killers = [] #--------------------------------------KILLERS---------------------------------
# Keeps track of how many successful puzzles we have generated
puzzles_generated = [0]
analytics_list = []

def generator(killers,puzzles_generated):
    
    while True:

        # The number of cages should be between 28 and 40 to keep the average cage size > 2 and < 3
        # < 2 >> too easy
        # < 3 .. too hard
        cages_num = random.randint(35,46)
        killer = puzzle_generator(cages_num)

        outcome,analytics = unique_solution(killer)
        
        if outcome != False:
            puzzles_generated[0] += 1
            
            if outcome not in killers:
                print("Puzzle added to killers")
                analytics_list.append(analytics)
                killers.append(killer)
            
            return outcome
            
    
# USER INTERFACE CODE

def user_interface(killers):
    
    while True:
    
        error_counter = 0
    
        killer = []
        cages = []
        values = []
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        no_of_cages = int(input("How many cages are you wanting in your puzzle? "))
        
        print("Please input cage coordinates as 12 to represent [1,2] where 1 is the row number and 2 is the column number.")
        print("To add multiple coordinates to a cage simply add a space between cell coordinates.")
        print("EG:")
        print("Type 12 34 56 78, to give the cage,")
        print("[[1,2],[3,4],[5,6],[7,8]].")
        print("Once you have finished entering the coordinates for a particular cage, press enter to move onto the next.")
        
        for i in range(no_of_cages):
            counter = str(i+1)
            c = input("Please input the coordinates of cage number " + counter + ": ")
            value = input("Please enter the value of this cage: ")
            values.append(int(value))
        
            # Remove spaces from the string
            c = c.replace(' ', '')
        
            # Convert each character to integer and group them into pairs
            cage = [[int(c[i]), int(c[i+1])] for i in range(0, len(c), 2)]
            
            cages.append(cage)
        
        killer.append(cages)
        killer.append(values)
        killer.append(grid)
        
        cage_cells = []
        
        
        for j in cages:
            for k in j:
                cage_cells.append(k)
                
        if len(cage_cells) < 81:
            print("The cages you have entered do not fill the grid, you need top add more cages or increase the size of the cages you have already entered.")
            print("You only have " + str(len(cage_cells)) + " cells filled, you need 81 to fill the grid.")
            error_counter += 1
        
        if len(cage_cells) > 81:
            print("The cages you have entered overfill the grid")
            print("You have entered" + str(len(cage_cells)) + " cells, the grid only has 81 cells.")
            error_counter += 1
            
        
        cage_cells2 = set()
        duplicates = []
        
        for cell in cage_cells:
            # Convert the sublist to a tuple so it can be hashable
            cell_tuple = tuple(cell)
            
            # If the tuple is already in the set, it's a duplicate
            if cell_tuple in cage_cells2:
                duplicates.append(cell)
            else:
                cage_cells2.add(cell_tuple)
        
        if len(duplicates) > 0:
            print("Duplicates detected!")
            print("The following cells appeared more than once: " + str(duplicates) +".")
            error_counter += 1
            
        total = sum(values)
        
        if total != 405:
            print("The total value of your cages must be equal to 405, your cage values sum to " + str(total) + ".")
            error_counter += 1
            
        if error_counter == 0:
            print("Your puzzle has passed eligibility criteria!")
            print("Your puzzle will now be tested to see if it has a unique solution")
            
            outcome = unique_solution(killer)
        
            if outcome != False:
                print("Your puzzle has a unique solution")
                print("Here is your puzzle")
                print_killer(killer)
                #Only adds to killers is not already in killers
                if outcome not in killers:
                    killers.append(killer)
                return killer
            
            print("Your puzzle does not have a unique solution")

        
        # ADD IN CODE RESTRICTING CELLS IN GRID CAN CURENTLY ENTER [10,10] ETC
        # ADD IN UNIQUE_SOLUTION CHECK
        
        print("Your puzzle has failed eligibility criteria.")
        

def main_menu(killers):
    
    # Choose whether to enter a puzzle, take to user interface, or 
    # to generate one for me 
    # the generator will generate problems with a unique solution where the initial 
    # grid is not populated with any clues
    # all cells are empty only cage locatioons and values are given
    
    while True:
    
        print("Hello, welcome to Matthew's Killer Sudoku Solver")
        print("Would you like me to generate you a Killer Sudoku puzzle, or would you prefer to enter your own?")
        
        # INPUT LOOP
        
        # This makes sure that the user can only input one of the 2 options
        
        option = 0
        
        while True:
            choice = input("Press 'G' to generate a puzzle, or I to input a puzzle ")
            
            if choice == 'g' or choice == 'G':
                print("Generate")
                option = 1
                break
            
            if choice == 'i' or choice == 'I':
                print("Input")
                option = 2
                break
                
            else:
                print("Please enter either 'G' to generate a puzzle, or 'I' to input your own")
                
        if option == 1:
            killer = generator(killers,puzzles_generated)
            print_killer(killer)
            
        if option == 2:
            killer = user_interface(killers)
            
        while True:
            print("Would you like to see the full solution?")
            
            choice = input("Enter 'Y' for the full solution, or enter 'N' to continue ")
            
            if choice == 'y' or choice == 'Y':
                print("Full Solution:")
                for row in killer[3]:
                    print(" ".join(map(str, row)))

                print("Goodbye")
                return
                     
            if choice == 'n' or choice == 'N':
                print("Goodbye")
                return

                
            else:
                print("Please enter either 'Y' to see the full solutiom, or 'N' to continue")
                
                
def results_generator(killers,puzzles_generated):
    
    
    while len(killers) < 100:
        
        generator(killers,puzzles_generated)
        
    return

'''
analytics_list = [[[1], [0.02692723274230957], [50.617283950617285], [[8], [4], [1], [0]]], [[3], [0.04086494445800781], [37.03703703703704], [[15], [4], [2], [0]]], [[1], [0.033913612365722656], [27.160493827160494], [[7], [2], [1], [1]]], [[1], [0.030944347381591797], [14.814814814814813], [[4], [1], [1], [1]]], [[2], [0.032907962799072266], [22.22222222222222], [[5], [1], [1], [1]]], [[1], [0.03889775276184082], [32.098765432098766], [[11], [5], [1], [1]]], [[3], [0.024931907653808594], [18.51851851851852], [[4], [1], [1], [0]]], [[2], [0.056817054748535156], [25.925925925925924], [[11], [2], [4], [1]]], [[2], [0.030945301055908203], [17.28395061728395], [[4], [1], [1], [1]]], [[1], [0.03294181823730469], [30.864197530864196], [[7], [2], [2], [0]]], [[1], [0.04089999198913574], [25.925925925925924], [[7], [2], [2], [1]]], [[1], [0.024933576583862305], [92.5925925925926], [[20], [6], [0], [0]]], [[2], [0.029920339584350586], [12.345679012345679], [[3], [0], [1], [1]]], [[3], [0.031903743743896484], [12.345679012345679], [[4], [1], [1], [1]]], [[1], [0.04288887977600098], [32.098765432098766], [[8], [3], [2], [1]]], [[2], [0.019945859909057617], [17.28395061728395], [[3], [0], [1], [0]]], [[2], [0.04089045524597168], [18.51851851851852], [[5], [1], [2], [1]]], [[1], [0.038896799087524414], [40.74074074074074], [[7], [3], [2], [1]]], [[2], [0.02193927764892578], [20.98765432098765], [[5], [1], [1], [0]]], [[1], [0.022909164428710938], [90.12345679012346], [[18], [5], [0], [0]]], [[1], [0.035904884338378906], [58.0246913580247], [[14], [3], [1], [1]]], [[1], [0.03490638732910156], [40.74074074074074], [[8], [4], [1], [1]]], [[1], [0.03294014930725098], [25.925925925925924], [[6], [2], [1], [1]]], [[1], [0.03587532043457031], [51.85185185185185], [[11], [4], [1], [1]]], [[2], [0.0323796272277832], [18.51851851851852], [[5], [2], [1], [1]]], [[1], [0.03393721580505371], [75.30864197530865], [[22], [8], [1], [0]]], [[1], [0.05786943435668945], [27.160493827160494], [[7], [2], [3], [2]]], [[1], [0.03390979766845703], [29.629629629629626], [[9], [2], [1], [1]]], [[1], [0.03291153907775879], [32.098765432098766], [[8], [2], [2], [0]]], [[1], [0.023921966552734375], [28.39506172839506], [[7], [1], [1], [0]]], [[3], [0.04191756248474121], [16.049382716049383], [[6], [2], [2], [1]]], [[2], [0.06080961227416992], [24.691358024691358], [[8], [5], [4], [1]]], [[1], [0.03986859321594238], [55.55555555555556], [[12], [4], [1], [1]]], [[3], [0.04189252853393555], [23.456790123456788], [[7], [3], [3], [0]]], [[1], [0.04584980010986328], [43.20987654320987], [[10], [2], [3], [1]]], [[1], [0.02495718002319336], [28.39506172839506], [[7], [3], [1], [0]]], [[1], [0.03191423416137695], [41.9753086419753], [[10], [2], [2], [0]]], [[1], [0.031914710998535156], [43.20987654320987], [[11], [2], [2], [0]]], [[1], [0.02995014190673828], [25.925925925925924], [[5], [1], [1], [1]]], [[1], [0.022940635681152344], [38.2716049382716], [[7], [2], [1], [0]]], [[1], [0.029947996139526367], [41.9753086419753], [[11], [6], [1], [0]]], [[1], [0.03291153907775879], [66.66666666666666], [[16], [9], [1], [0]]], [[1], [0.03786778450012207], [20.98765432098765], [[5], [1], [2], [1]]], [[1], [0.03886747360229492], [27.160493827160494], [[6], [2], [2], [1]]], [[2], [0.040859222412109375], [51.85185185185185], [[18], [7], [2], [0]]], [[1], [0.02390885353088379], [19.753086419753085], [[4], [1], [1], [0]]], [[1], [0.03293967247009277], [23.456790123456788], [[6], [2], [1], [1]]], [[2], [0.04787087440490723], [25.925925925925924], [[6], [5], [2], [1]]], [[2], [0.029919147491455078], [13.580246913580247], [[3], [1], [1], [1]]], [[2], [0.0379488468170166], [27.160493827160494], [[8], [3], [1], [1]]], [[1], [0.024933338165283203], [38.2716049382716], [[9], [3], [1], [0]]], [[2], [0.05083489418029785], [19.753086419753085], [[6], [4], [3], [1]]], [[2], [0.023907899856567383], [23.456790123456788], [[6], [1], [1], [0]]], [[1], [0.03890228271484375], [24.691358024691358], [[7], [1], [2], [1]]], [[1], [0.02290964126586914], [48.148148148148145], [[8], [2], [1], [0]]], [[2], [0.031884193420410156], [20.98765432098765], [[4], [1], [1], [1]]], [[2], [0.06429409980773926], [44.44444444444444], [[16], [7], [4], [1]]], [[2], [0.015985965728759766], [20.98765432098765], [[5], [1], [0], [0]]], [[1], [0.0249330997467041], [39.50617283950617], [[7], [3], [1], [0]]], [[2], [0.023935556411743164], [18.51851851851852], [[6], [1], [1], [0]]], [[1], [0.03388071060180664], [65.4320987654321], [[12], [5], [2], [0]]], [[1], [0.031914472579956055], [60.49382716049383], [[11], [3], [2], [0]]], [[2], [0.041887521743774414], [23.456790123456788], [[7], [3], [2], [1]]], [[1], [0.04488825798034668], [35.80246913580247], [[11], [4], [2], [1]]], [[1], [0.03191375732421875], [71.60493827160494], [[16], [5], [1], [0]]], [[2], [0.030916690826416016], [7.4074074074074066], [[2], [0], [1], [1]]], [[1], [0.028922080993652344], [16.049382716049383], [[3], [1], [1], [1]]], [[2], [0.05083465576171875], [20.98765432098765], [[9], [2], [3], [1]]], [[2], [0.022962093353271484], [13.580246913580247], [[4], [1], [1], [0]]], [[1], [0.034906625747680664], [65.4320987654321], [[16], [7], [0], [1]]], [[1], [0.045874595642089844], [55.55555555555556], [[16], [6], [2], [1]]], [[1], [0.02290177345275879], [35.80246913580247], [[6], [2], [1], [0]]], [[1], [0.043882131576538086], [37.03703703703704], [[8], [4], [2], [1]]], [[2], [0.043910980224609375], [32.098765432098766], [[10], [4], [2], [1]]], [[1], [0.025930404663085938], [59.25925925925925], [[10], [3], [1], [0]]], [[1], [0.03989124298095703], [35.80246913580247], [[8], [3], [2], [1]]], [[1], [0.041887760162353516], [29.629629629629626], [[7], [4], [2], [1]]], [[2], [0.03088521957397461], [24.691358024691358], [[6], [1], [1], [1]]], [[1], [0.03989291191101074], [20.98765432098765], [[5], [2], [2], [1]]], [[2], [0.041887760162353516], [20.98765432098765], [[6], [4], [3], [0]]], [[2], [0.03550553321838379], [35.80246913580247], [[8], [4], [1], [1]]], [[1], [0.030916213989257812], [49.382716049382715], [[10], [1], [1], [1]]], [[3], [0.04288458824157715], [25.925925925925924], [[13], [5], [2], [0]]], [[1], [0.033908843994140625], [56.79012345679012], [[12], [4], [1], [1]]], [[2], [0.029920339584350586], [27.160493827160494], [[9], [4], [1], [0]]], [[2], [0.0334324836730957], [19.753086419753085], [[6], [2], [1], [1]]], [[1], [0.03192710876464844], [32.098765432098766], [[7], [2], [1], [1]]], [[1], [0.03886675834655762], [24.691358024691358], [[9], [5], [1], [1]]], [[3], [0.043852806091308594], [19.753086419753085], [[9], [2], [2], [1]]], [[1], [0.03992152214050293], [27.160493827160494], [[7], [2], [2], [1]]], [[1], [0.03992009162902832], [28.39506172839506], [[8], [1], [2], [1]]], [[1], [0.0508577823638916], [25.925925925925924], [[8], [3], [2], [2]]], [[1], [0.04487943649291992], [43.20987654320987], [[12], [5], [2], [1]]], [[1], [0.031914472579956055], [27.160493827160494], [[7], [1], [1], [1]]], [[2], [0.03293943405151367], [18.51851851851852], [[5], [2], [1], [1]]], [[1], [0.04191780090332031], [28.39506172839506], [[7], [4], [2], [1]]], [[2], [0.04089021682739258], [24.691358024691358], [[6], [3], [2], [1]]], [[1], [0.03195357322692871], [33.33333333333333], [[8], [4], [2], [0]]], [[2], [0.0359036922454834], [23.456790123456788], [[7], [2], [1], [1]]], [[2], [0.05083465576171875], [23.456790123456788], [[7], [4], [3], [1]]]]'''
easy_list = []
medium_list = []
hard_list = []

def analytics_seperate(analytics_list):
    
    for analytics in analytics_list:
        
        if analytics[0] == [1]:
            easy_list.append(analytics)
            
        if analytics[0] == [2]:
            medium_list.append(analytics)
            
        if analytics[0] == [3]:
            hard_list.append(analytics)
    
    return

 
'''   
def list_analytics(easy_list):
    
    length = len(easy_list)
    
    total_time = 0
    for analytics in easy_list:
        total_time += analytics[1][0]
    
    avg_time = total_time / length
    
    perc_solved = 0
    for analytics2 in easy_list:
        perc_solved += analytics[2][0]
        
    avg_perc_solved = perc_solved / length
    
    simple_elim_counter = 0
    hidden_counter = 0
    
    pointing_counter = 0
    boxline_counter = 0
    
    for analytics in easy_list:
        simple_elim_counter += analytics[3][0][0]
        hidden_counter += analytics[3][1][0]
        pointing_counter += analytics[3][2][0]
        boxline_counter += analytics[3][3][0]
        
    simple = simple_elim_counter / length
    hidden = hidden_counter / length
    pointing = pointing_counter / length
    boxline = boxline_counter / length
    
    return length,avg_time,avg_perc_solved,simple,hidden,pointing,boxline




length_easy,avg_time_easy,avg_perc_solved_easy,simple_easy,hidden_easy,pointing_easy,boxline_easy = list_analytics(easy_list)
    
length_med,avg_time_med,avg_perc_solved_med,simple_med,hidden_med,pointing_med,boxline_med = list_analytics(medium_list)    

length_hard,avg_time_hard,avg_perc_solved_hard,simple_hard,hidden_hard,pointing_hard,boxline_hard = list_analytics(hard_list)

    
x = ["Easy","Medium","Hard"]
y = [avg_time_easy,avg_time_med,avg_time_hard]
    
plt.bar(x,y)

plt.xlabel("Difficulty")
plt.ylabel("Average time taken until solver stopped")

plt.show()


x2 = ["Easy","Medium","Hard"]
y2 = [avg_perc_solved_easy,avg_perc_solved_med,avg_perc_solved_hard]
    
plt.bar(x2,y2)

plt.xlabel("Difficulty")
plt.ylabel("Average percentage solved by the solver")

plt.show()

x3 = ["Easy","Medium","Hard"]
y3 = [simple_easy,simple_med,simple_hard]
    
plt.bar(x3,y3)

plt.xlabel("Difficulty")
plt.ylabel("Average usage of simple elimination")

plt.show()

x4 = ["Easy","Medium","Hard"]
y4 = [hidden_easy,hidden_med,hidden_hard]
    
plt.bar(x4,y4)

plt.xlabel("Difficulty")
plt.ylabel("Average usage of hidden singles")

plt.show()

x5 = ["Easy","Medium","Hard"]
y5 = [pointing_easy,pointing_med,pointing_hard]
    
plt.bar(x5,y5)

plt.xlabel("Difficulty")
plt.ylabel("Average usage of pointing pairs")

plt.show()

x6 = ["Easy","Medium","Hard"]
y6 = [boxline_easy,boxline_med,boxline_hard]
    
plt.bar(x6,y6)

plt.xlabel("Difficulty")
plt.ylabel("Average usage of box line reduction")

plt.show()


'''



