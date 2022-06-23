from nsum import findNsum
import numpy as np
import defs
import create_board
import matplotlib.pyplot as plt
import time
import itertools
import sys
from create_board import make_board
from collections import defaultdict
import subsetsum
import pickle
import os
import copy
import random


plot = False
alt = False


def is_unique(x):
    return len(x) == len(set(x))


def unstack(a, axis=0):
    return np.moveaxis(a, axis, 0)


def fill_hook(hook_map):
    filled_arr = []
    for i, num in enumerate(hook_map):
        hook = [num] * num
        hook += [0] * (2 * (i + 1) - 1 - num)
        filled_arr.append(hook)
    return filled_arr

def dfs(grid,i,j):
    if i<0 or j<0 or i>=len(grid) or j>=len(grid) or grid[i][j]==0:
        return
    grid[i][j]= 0
    dfs(grid,i+1,j)
    dfs(grid,i-1,j)
    dfs(grid,i,j+1)
    dfs(grid,i,j-1)

## Does dfs to count islands
def numIslands(grid):
    count=0
    if len(grid)<=0:
        return 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]!=0:
                count+=1
                dfs(grid,i,j)
    return count


def sum_group(board, group):
    sum = 0
    for cell in group_coords[group]:
        sum += board[cell[0]][cell[1]]
    return sum



if __name__ == '__main__':
    size = 5 if alt else 9

    v_make_boards = np.vectorize(make_board, otypes=[np.ndarray])

    if alt:
        possible_nums = defs.possible_nums_alt
        regions = defs.regions_alt
        trigger_cells = defs.trigger_cells_alt
        target = 11
        nums = defs.nums_alt
    else:
        possible_nums = defs.possible_nums
        regions = defs.regions
        trigger_cells = defs.trigger_cells
        target = 15
        nums = defs.nums
    group_coords = defaultdict(list)
    for i in range(size):
        for j in range(size):
            try:
                group_coords[regions[i][j]].append([i, j])
            except KeyError:
                group_coords[regions[i][j]] = [i, j]

    # print(group_coords)

    # Inefficient but takes 1 sec and appeases the APL side of me
    # Enumerates all possible placements of nums in hooks
    hook_num_map = np.array(list(itertools.product(*possible_nums)))
    b_mask = np.array(list(map(is_unique, hook_num_map)))
    hook_num_map = hook_num_map[b_mask].tolist()

    print(hook_num_map[0])

    print(len(hook_num_map))

    start = time.process_time()
    inputs = create_board.valid_inputs(size)
    boards = v_make_boards(inputs)
    print(time.process_time() - start)

    if plot:
        figure, ax = plt.subplots()
        figure.show()
        plot = plt.imshow(make_board(inputs[0]), cmap='plasma_r')
        for i in range(len(inputs)):
            plot.set_data(boards[i])
            figure.canvas.draw_idle()
            figure.canvas.flush_events()
        plt.show()


    def verify_boards():
        valid_indices = []
        if not alt:
            # Check that 2 sums add up to 15, and the top hook has 8s in it
            for b_idx, board in enumerate(boards):
                print(b_idx)
                for h_idx, hook_map in enumerate(hook_num_map):
                    if hook_map[board[0, 4] - 1] + hook_map[board[1, 4] - 1] != 15:
                        continue
                    elif hook_map[board[3, 7] - 1] + hook_map[board[3, 8] - 1] != 15:
                        continue
                    elif hook_map[board[0, 2] - 1] != 8:
                        continue

                    groups = defaultdict(list)
                    for i in range(len(regions)):
                        for j in range(len(regions)):
                            try:
                                groups[hook_map[board[i, j] - 1]].append(regions[i][j])
                            except KeyError:
                                groups[hook_map[board[i, j] - 1]] = [regions[i][j]]
                    if len(set(groups[9])) < 9 or len(set(groups[8])) < 8:
                        continue

                    if len(set(groups[7])) < 7:
                        if groups[7].count(groups[1]) < 2:
                            continue
                        # if groups[1] not in groups[7]:
                        #     continue

                    # if len(groups[8]) < 8:
                    #     continue
                    #
                    valid_indices.append([b_idx, h_idx])

        if alt:
            print(hook_num_map)
            for b_idx, board in enumerate(boards):
                print(b_idx)
                for h_idx, hook_map in enumerate(hook_num_map):
                    if hook_map[board[0, 1] - 1] != 4:
                        continue
                    elif hook_map[board[4, 0] - 1] != 5:
                        continue
                    elif hook_map[board[4, 3] - 1] != 5:
                        continue
                    elif hook_map[board[0, 4] - 1] != 3:
                        continue

                    valid_indices.append([b_idx, h_idx])
        return valid_indices


    if os.path.exists("indices_" + str(size) + ".obj"):
        filehandler = open("indices_" + str(size) + ".obj", "rb")
        valid_indices = pickle.load(filehandler)
        filehandler.close()
    else:
        valid_indices = verify_boards()
        filehandler = open("indices_" + str(size) + ".obj", "wb")
        pickle.dump(valid_indices, filehandler)
        filehandler.close()


    # print(len(valid_indices))
    #
    # print(boards[valid_indices[-1][0]])
    # print(hook_num_map[valid_indices[-1][1]])
    #
    # print(fill_hook(hook_num_map[valid_indices[-1][1]]))

    # def solve(board, hook_board, nums_left, triggers):

    def create_group_vals(hook_board, hook_nums, regions):
        group_vals = defaultdict(list)
        for i in range(size):
            for j in range(size):
                try:
                    group_vals[regions[i][j]].append(hook_nums[hook_board[i, j] - 1])
                except KeyError:
                    group_vals[regions[i][j]] = hook_nums[hook_board[i, j] - 1]
        # print(group_vals)
        return group_vals


    missing = 0
    not_missing = 0
    start = time.time()
    filtered_indices = []
    for index in valid_indices:
        hook_board = boards[index[0]]
        hook_nums = hook_num_map[index[1]]
        group_sums = create_group_vals(hook_board, hook_nums, regions)
        full_sols = []
        for group, values in group_sums.items():
            solutions = subsetsum.solutions(values, target)
            group_sols = []
            for solution in solutions:
                group_sols.append(solution)
            full_sols.append(group_sols)

        if [] in full_sols:
            missing += 1
        else:
            not_missing += 1
            filtered_indices.append(index)

        # print(group_sols)
        # print(solutions[0])

    print(missing)
    print(not_missing)
    print(filtered_indices)
    print(time.time() - start)

    blank_board = [[None] * size for _ in range(size)]


    def backtrack(board, nums_left, hook_board, triggers, n, cell=1):

        # print(cell)
        trigger = triggers[0][0]
        y = (cell - 1) % size
        x = (cell - 1) // size

        # print(x, y)

        hook_num = hook_board[x][y] - 1

        if n == -1:
            if nums_left[hook_num][0] == nums_left[hook_num][-1]:
            #if len(nums_left[hook_num]) == 1:
                print("Bail early")
                return False
        nums = nums_left
        print("-----")
        print(cell)
        print(x, y)
        print(nums)
        print(nums[hook_num][n])
        print("Hook num: " + str(hook_num))
        print(np.reshape(board, (size, size)))

        #board[x][y] = nums[hook_num].pop(n)
        board[x][y] = nums[hook_num][n]
        nums[hook_num].remove(board[x][y])

        if cell > size ** 2:
            print("Made it to the end??")
            print(board)
            if sum_group(board, trigger) == 15:
                return True

        if cell == trigger:
            if sum_group(board, triggers[0][1]) != 15:
                print("Failed")
                return False
            triggers.pop(0)
        nums1 = nums.copy()
        nums2 = nums.copy()
        return backtrack(board.copy(), nums1, hook_board, triggers[:], -1, cell=cell + 1) or backtrack(board.copy(), nums2, hook_board, triggers[:], 0, cell=cell + 1)


    #def backtrack2(board, hook_board, hook_map, nums_used, triggers, n, cell = 1):
    def backtrack2(board, nums_used, triggers, n, cell = 1):
        y = (cell - 1) % size
        x = (cell - 1) // size

        hook_num = hook_board[x][y] - 1


        num = hook_map[hook_num]*n

        board[x][y] = num
        # print(nums_used)
        # print(np.reshape(board, (size, size)))
        if num > 0:
            nums_used[num] += 1

            if nums_used[num] > num:
                #print("Too many nums")
                return False

        if cell == size ** 2:

            print("-----")
            print("Made it to the end??")
            print(num)
            print(np.reshape(board, (size, size)))
            if sum_group(board, trigger_cells[-1][1]) == target:
                print("good sum!")
                passes = True
                for i in range(size-1):
                    for j in range(size-1):
                        if board[i][j] * board[i+1][j] * board[i][j+1] * board[i+1][j+1] != 0:
                            passes = False
                print("Good window")
                if alt:
                    if not(board[0][1] == 4 and board[0][4] == 3 and board[4][0] == 5 and board[4][3] == 5):
                        passes = False
                else:
                    if board[0][2] != 8:
                        passes = False
                print("Good values")

                dfs_board = copy.deepcopy(board)
                if numIslands(dfs_board) != 1:
                    passes = False
                print("All connected")


                if passes:
                    print("Found it!")
                    print(np.reshape(board, (size, size)))
                    return board

                else:
                    #print("Failed Checks")
                    return False
            else:
                #print("Bad sum")
                return False

        trigger = triggers[0][0]

        if cell == trigger:
            if sum_group(board, triggers[0][1]) != target:
                #print("Bad sum")
                return False
            #print("Good sum!")
            triggers.pop(0)

        randnum = random.random()
        if randnum > 0.5:
            return backtrack2(board.copy(), nums_used.copy(), triggers.copy(), 1, cell=cell + 1) or backtrack2(
                board.copy(), nums_used.copy(), triggers.copy(), 0, cell=cell + 1)
        else:
            return backtrack2(board.copy(), nums_used.copy(), triggers.copy(), 0, cell= cell+1) or backtrack2(board.copy(), nums_used.copy(), triggers.copy(), 1, cell= cell+1)


    num_dict = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0
    }

    i = 0

    for index in filtered_indices[::-1]:
        i+=1
        hook_board = boards[index[0]]
        hook_map = hook_num_map[index[1]]
        filled_hooks = fill_hook(hook_num_map[index[1]])
        print(hook_board)
        print(hook_map)
        print("Start backtrack:")
        #print(filled_hooks)
        start = time.time()
        #sol = backtrack2(blank_board, num_dict.copy(), trigger_cells, 1)
        sol = backtrack2(blank_board, num_dict.copy(), trigger_cells, 0)
        print("Time taken: " + str(time.time()-start))
        if sol:
            print("Found solution")
            print(np.reshape(sol, (size, size)))
            #print(sol)
            break
        #backtrack(blank_board, filled_hooks, hook_board, trigger_cells, -1)
