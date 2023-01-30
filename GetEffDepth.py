import numpy as np

def get_eff_depth(rebar, cover, link_d, h):
    
    la = []  # initialise vector to store area of reinforcement for each layer
    rebar_d = [] # initialise vector to store diameters of rebar in each layer
    lcx = []  # initialise vector to store coordinate of reinforcement for each layer
    
    # get area of each layer and coordinates
    i = 0  # i is a counter for each layer (0 - is first layer, 1 - second layer, ...)
    for layer in rebar:
        n = layer[0]
        d = layer[1]
        la.append(n*np.pi*(d**2)/4)  # store reinforcement area for layer 
        rebar_d.append(d)  # store current rebar diameter
        if i < 1:  # this is for first layer
            lcx.append(cover + link_d + d/2)
        else:  # if is not first layer, add the sum of half diameter already placed plus the spacing of one diameter in between
                lcx.append(lcx[-1] + rebar_d[-2]/2 + rebar_d[-2] + d/2)
        i += 1
    
    As = sum(la)  # determine total area of reinforcement
    
    # get center of gravity reinforcement
    cg = sum(np.array(la)*np.array(lcx))/As
    
    eff_depth = h-cg  # d is effective depth
    
    return eff_depth, As


