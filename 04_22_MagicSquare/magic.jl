using JuMP
using HiGHS
magic = Model(HiGHS.Optimizer)
set_optimizer_attribute(magic, "threads", 4)
set_optimizer_attribute(magic, "parallel", "on")
set_optimizer_attribute(magic, "write_model_to_file", "true")
set_optimizer_attribute(magic, "write_model_file", "magic_Simple.txt")
set_optimizer_attribute(magic, "mip_report_level", 2)

set_optimizer_attribute(magic, "write_solution_to_file", "true")
set_optimizer_attribute(magic, "solution_file", "Solution.txt")


num_bound = 100
# Start the magic board
@variable(magic, x[i = 1:6, j = 1:6, k = 1:num_bound], Bin)

# These are the magic square constants 
@variable(magic, a)
@variable(magic, b)
@variable(magic, c)
@variable(magic, d)

@constraint(magic, 15 <= a <= 250)
@constraint(magic, 15 <= b <= 250)
@constraint(magic, 15 <= c <= 250)
@constraint(magic, 15 <= d <= 250)


v = ones(6,6,num_bound)
for k in 1:num_bound
    v[:,:,k] *= k
end

### Setting up which cells can and can't have digits
# First row
for j in 1:1
    @constraint(magic, sum(x[1,j,k] for k in 1:num_bound) == 0)
end

for j in 2:4
    @constraint(magic, sum(x[1,j,k] for k in 1:num_bound) == 1)
end

for j in 5:6
    @constraint(magic, sum(x[1,j,k] for k in 1:num_bound) == 0)
end

# Second Row
for j in 1:1
    @constraint(magic, sum(x[2,j,k] for k in 1:num_bound) == 0)
end

for j in 2:6
    @constraint(magic, sum(x[2,j,k] for k in 1:num_bound) == 1)
end

# Third Row
for j in 1:6
    @constraint(magic, sum(x[3,j,k] for k in 1:num_bound) == 1)
end

# Fourth Row
for j in 1:6
    @constraint(magic, sum(x[4,j,k] for k in 1:num_bound) == 1)
end

# Fifth Row
for j in 1:5
    @constraint(magic, sum(x[5,j,k] for k in 1:num_bound) == 1)
end

for j in 6:6
    @constraint(magic, sum(x[5,j,k] for k in 1:num_bound) == 0)
end


# Sixth Row
for j in 1:2
    @constraint(magic, sum(x[6,j,k] for k in 1:num_bound) == 0)
end

for j in 3:5
    @constraint(magic, sum(x[6,j,k] for k in 1:num_bound) == 1)
end

for j in 6:6
    @constraint(magic, sum(x[6,j,k] for k in 1:num_bound) == 0)
end



# Make sure there is only 1 of each number in solution
for k in 1:num_bound
    @constraint(magic, sum(x[:,:,k]) <= 1)
end

sumMatrix = sum((x .* v), dims = 3)


for i in 1:3
    # Row and Col constraints
    @constraint(magic, sum(sumMatrix[i,2:4]) <= a)
    @constraint(magic, sum(sumMatrix[1,2:4]) >= a-1)

    @constraint(magic, sum(sumMatrix[1:3,i+1]) <= a)
    @constraint(magic, sum(sumMatrix[1:3,i+1]) >= a-1)


    @constraint(magic, sum(sumMatrix[i+1,4:6]) <= b)
    @constraint(magic, sum(sumMatrix[i+1,4:6]) >= b-1)

    @constraint(magic, sum(sumMatrix[2:4,i+3]) <= b)
    @constraint(magic, sum(sumMatrix[2:4,i+3]) >= b-1)


    @constraint(magic, sum(sumMatrix[i+2,1:3]) <= c)
    @constraint(magic, sum(sumMatrix[i+2,1:3]) >= c-1)

    @constraint(magic, sum(sumMatrix[3:5,i]) <= c)
    @constraint(magic, sum(sumMatrix[3:5,i]) >= c-1)


    @constraint(magic, sum(sumMatrix[i+3,3:5]) <= d)
    @constraint(magic, sum(sumMatrix[i+3,3:5]) >= d-1)

    @constraint(magic, sum(sumMatrix[4:6,i+2]) <= d)
    @constraint(magic, sum(sumMatrix[4:6,i+2]) >= d-1)
end

# # Diagonals
@constraint(magic, sum(sumMatrix[i,i+1] for i in 1:3) <= a)
@constraint(magic, sum(sumMatrix[i,i+1] for i in 1:3) >= a-1)

@constraint(magic, sum(sumMatrix[i,5-i] for i in 1:3) <= a)
@constraint(magic, sum(sumMatrix[i,5-i] for i in 1:3) >= a-1)

@constraint(magic, sum(sumMatrix[i+1,i+3] for i in 1:3) <= b)
@constraint(magic, sum(sumMatrix[i+1,i+3] for i in 1:3) >= b-1)

@constraint(magic, sum(sumMatrix[i+1,7-i] for i in 1:3) <= b)
@constraint(magic, sum(sumMatrix[i+1,7-i] for i in 1:3) >= b-1)

@constraint(magic, sum(sumMatrix[i+2,i] for i in 1:3) <= c)
@constraint(magic, sum(sumMatrix[i+2,i] for i in 1:3) >= c-1)

@constraint(magic, sum(sumMatrix[i+2,4-i] for i in 1:3) <= c)
@constraint(magic, sum(sumMatrix[i+2,4-i] for i in 1:3) >= c-1)

@constraint(magic, sum(sumMatrix[i+3,i+2] for i in 1:3) <= d)
@constraint(magic, sum(sumMatrix[i+3,i+2] for i in 1:3) >= d-1)

@constraint(magic, sum(sumMatrix[i+3,6-i] for i in 1:3) <= d)
@constraint(magic, sum(sumMatrix[i+3,6-i] for i in 1:3) >= d-1)

@objective(magic, Min, sum(x .* v))
#@constraint(magic, sum(x.*v) <= 650)
optimize!(magic)
x_val = value.(x)

# v = zeros(Int, 6, 6)

# for k in 1:num_bound
#     v[:,:] += k*x_val[:,:,k]
# end

sol = zeros(Int, 6, 6) 

for i in 1:6
    for j in 1:6
        for k in 1:num_bound
            if round(Int, x_val[i, j, k]) == 1
                sol[i, j] = k
            end
        end
    end
end

sol
display(sol)
println()
println([value.(a), value.(b), value.(c) ,value.(d)])
println(sum(sol))
#display(findfirst(x_val[:,:] .> 0, dims = 3))