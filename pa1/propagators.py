#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

A propagator is a function with the following template:
    propagator(csp, newly_instaniated_variable=None)
        ...
        returns (True/False, [(Variable, Value),(Variable,Value),...])
        
    csp is a CSP object, which the propagator can use to get access to
    the variables and constraints of the problem
    
    newly_instaniated_variable is an optional argument;
        if it is not None, then:
            newly_instaniated_variable is the most recently assigned variable
        else:
            the propagator was called before any assignment was made
    
    the prop returns True/False and a list of variable-value pairs;
        the former indicates whether a DWO did NOT occur,
        and the latter specifies each value that was pruned
     
The propagator SHOULD NOT prune a value that has already been pruned
or prune a value twice

In summary, this is what the propagator must do:

    If newly_instantiated_variable = None
      
        for plain backtracking;
            we do nothing...return true, []

        for forward checking;
            we check all unary constraints of the CSP
            
        for gac;
            we establish initial GAC by initializing the GAC queue
            with all constaints of the CSP


     If newly_instantiated_variable = a variable V
      
         for plain backtracking;
            we check all constraints with V that are fully assigned
            (use csp.get_cons_with_var)

         for forward checking;
            we check all constraints with V that have one unassigned variable

         for gac;
            we initialize the GAC queue with all constraints containing V
   '''

def prop_BT(csp, newVar=None):
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    #IMPLEMENT

    pruned = []

    if newVar is None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)

    for c in cons:
        if c.get_n_unasgn() == 1:
            v = None
            i = None
            vals = []
            for idx, var in enumerate(c.get_scope()):
                val = var.get_assigned_value()
                vals.append(val)
                if val is None:
                    v = var
                    i = idx
            for val in v.cur_domain():
                vals[i] = val
                if not c.check(vals):
                    v.prune_value(val)
                    pruned.append((v, val))
            if v.cur_domain_size() == 0:
                return False, pruned

    return True, pruned

def prop_GAC(csp, newVar=None):
    #IMPLEMENT

    pruned = []

    if newVar is None:
        cons = dict.fromkeys(csp.get_all_cons())
    else:
        cons = dict.fromkeys(csp.get_cons_with_var(newVar))

    while cons:
        c = next(iter(cons))
        del cons[c]
        for v in c.get_scope():
            for val in v.cur_domain():
                if not c.has_support(v, val):
                    v.prune_value(val)
                    pruned.append((v, val))
                    cons.update({i: None for i in csp.get_cons_with_var(v) if i != c})
            if v.cur_domain_size() == 0:
                return False, pruned

    return True, pruned
