from defs import nums
import math




def findNsum(nums, target, N, result, results = []):
    if len(nums) < N or N < 2 or target < nums[0] * N or target > nums[-1] * N:  # early termination
        return
    if N == 2:  # two pointers solve sorted 2-sum problem
        l, r = 0, len(nums) - 1
        while l < r:
            s = nums[l] + nums[r]
            if s == target:
                results.append(result + [nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
            elif s < target:
                l += 1
            else:
                r -= 1
    else:  # recursively reduce N
        for i in range(len(nums) - N + 1):
            if i == 0 or (i > 0 and nums[i - 1] != nums[i]):
                findNsum(nums[i + 1:], target - nums[i], N - 1, result + [nums[i]], results)

res = []
def subset_sum(numbers, target, partial=[], result = []):
    s = sum(partial)
    # check if the partial sum is equals to target
    if s == target:
        result.append(partial)
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i + 1:]
        subset_sum(remaining, target, partial + [n])


area: int = 0
def dfs(grid,i,j):
    if i<0 or j<0 or i>=len(grid) or j>=len(grid) or grid[i][j]!=0:
        return
    global area
    grid[i][j]='#'
    area = area + 1
    dfs(grid,i+1,j)
    dfs(grid,i-1,j)
    dfs(grid,i,j+1)
    dfs(grid,i,j-1)

## Does dfs to count islands
areas = []
def numIslands(grid):
    global area
    global areas
    count=0
    if len(grid)<=0:
        return 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]==0:
                count+=1
                dfs(grid,i,j)
                areas.append(area)
                area = 0
    return count

grid = [[5, 7, 8, 0, 6, 0, 6, 0, 6,],
 [5, 0, 0, 9, 9, 9, 9, 9, 6],
 [5, 7, 8, 4, 0, 4, 0, 9, 0],
 [0, 0, 0, 4, 2, 2, 3, 9, 6],
 [0, 0, 8, 4, 0, 1, 0, 9, 0],
 [0, 0, 0, 3, 0, 0, 3, 9, 6],
 [0, 7, 8, 8, 8, 0, 8, 0, 8],
 [0, 0, 7, 0, 7, 0, 7, 0, 7],
 [0,0 ,0 ,0 ,0 ,5 ,5 ,0 ,0]]

print(numIslands(grid))
print(areas)
print(math.prod(areas))
print(grid)