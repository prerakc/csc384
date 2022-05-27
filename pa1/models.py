#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = warehouse_binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the warehouse.

The grid-only models do not need to encode the cage constraints.

1. warehouse_binary_ne_grid
    - A model of the warehouse problem w/o room constraints built using only 
      binary not-equal constraints for the row/column constraints.

2. warehouse_nary_ad_grid
    - A model of the warehouse problem w/o room constraints built using only n-ary 
      all-different constraints for the row/column constraints. 

3. warehouse_full_model
    - A model of the warehouse problem built using either the binary not-equal or n-ary
      all-different constraints for the row/column constraints.
'''
from cspbase import *
import itertools

def warehouse_binary_ne_grid(warehouse_grid):
    ##IMPLEMENT

    size = warehouse_grid[0][0]

    dom = list(range(1, size+1))

    vars = []

    for row in dom[::-1]:
        var_row = []

        for col in dom:
            var = Variable("{}{}".format(col, row), dom)
            var_row.append(var)

        vars.append(var_row)

    csp = CSP("{}-warehouse_binary_ne_grid".format(size), [j for i in vars for j in i])

    sat_tup = list(itertools.permutations(dom, 2))

    for r in range(size):
        for c in range(size):
            for i in range(c+1, size):
                con = Constraint("Row Constraint", [vars[r][c], vars[r][i]])
                con.add_satisfying_tuples(sat_tup)
                csp.add_constraint(con)

            for j in range(r+1, size):
                con = Constraint("Column Constraint", [vars[r][c], vars[j][c]])
                con.add_satisfying_tuples(sat_tup)
                csp.add_constraint(con)

    return csp, vars

def warehouse_nary_ad_grid(warehouse_grid):
    ##IMPLEMENT 
    
    size = warehouse_grid[0][0]

    dom = list(range(1, size+1))

    vars = []

    for row in dom[::-1]:
        var_row = []

        for col in dom:
            var = Variable("{}{}".format(col, row), dom)
            var_row.append(var)

        vars.append(var_row)

    csp = CSP("{}-warehouse_nary_ad_grid".format(size), [j for i in vars for j in i])

    sat_tup = list(itertools.permutations(dom, size))

    for row in vars:
        con = Constraint("Row Constraint", row)
        con.add_satisfying_tuples(sat_tup)
        csp.add_constraint(con)

    for col in zip(*vars):
        con = Constraint("Column Constraint", col)
        con.add_satisfying_tuples(sat_tup)
        csp.add_constraint(con)

    return csp, vars

def warehouse_full_model(warehouse_grid):
    ##IMPLEMENT 
    
    size = warehouse_grid[0][0]

    csp, vars = warehouse_nary_ad_grid(warehouse_grid)

    n = len(vars)

    for seq in warehouse_grid[1:]:
        seq_vars = [vars[n - (cell % 10)][(cell // 10) - 1] for cell in seq[:-2]]

        if seq[-2] == 0:
            con = Constraint("Equal Constraint", seq_vars)
            sat_tup = [ [seq[-1]] * len(seq_vars) ]

        elif seq[-2] == 1:
            con = Constraint("Sum Constraint", seq_vars)
            sat_tup = itertools.filterfalse(lambda x: sum(x) != seq[-1], itertools.product(range(1, size+1), repeat=len(seq_vars)))

        elif seq[-2] == 2:
            con = Constraint("Min Constraint", seq_vars)
            sat_tup = itertools.product(range(seq[-1], size+1), repeat=len(seq_vars))

        else:
            con = Constraint("Max Constraint", seq_vars)
            sat_tup = itertools.product(range(1, seq[-1]+1), repeat=len(seq_vars))

        con.add_satisfying_tuples(sat_tup)
        csp.add_constraint(con)

    return csp, vars
