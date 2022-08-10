import numpy as np
import math as mt
# train = training cells on either side
# guard = guard cells on either side
# rank = 
# data = data set
# Pfa = probability of false alarm
# This version ignores all cells with insufficient lead/lag cells
# for training
def os_cfar(half_train, half_guard, rank, SOS, data):

    ns = len(data) # number of samples
    result = np.zeros(ns)
    th = np.zeros(ns)
    lead = half_train + half_guard # max num cells considered on either side of cut
    lag = ns - lead
    # k = rank
    N = 2*half_train - 2*half_guard
    
    # Try these methods
    # k = round(3*N/4)
    k = rank

    # print(data)
    # print("N (num training) = ", N)
    # print("train half = ", half_train)
    # print("Guard half = ", half_guard)
    # print("k = ", k)
    # print("ns = ", ns)
    # Pfa_numer = k*mt.factorial(N)* mt.factorial(k-1)*mt.factorial(SOS+N-k)
    # Pfa_denom = (mt.factorial(k)*mt.factorial(N-k))*mt.factorial(SOS+N)
    # Pfa = Pfa_numer/Pfa_denom
    Pfa = k*mt.factorial(N)/(mt.factorial(k)*mt.factorial(N-k)) \
        * mt.factorial(k-1)*mt.factorial(SOS+N-k)/mt.factorial(SOS+N)

    for cutidx in range(ns): #cutidx = index of cell under test

        # ******************* Set up training cells *****************
        # If no LHS training cells, take cells right of RHS
        if (cutidx<lead and cutidx-half_guard==0):
            rhs_train = data[cutidx+half_guard:cutidx+lead]
            lhs_train = data[cutidx+lead:cutidx+lead+half_train]

        # IF some LHS cells, use these and take remainder from RHS
        elif (cutidx<lead and cutidx-half_guard>0):
            # RHS train cells set as normal
            rhs_train = data[cutidx+half_guard:cutidx+lead]
            # add all cells from pos 0 up to guard to train set
            lhs_train = data[0:cutidx-half_guard]
            # space = number of lhs train cells still to be filled
            lhs_fill = half_train-len(lhs_train)
            # add cells to the right of rhs train cells to the lhs side
            lhs_train.append(data[cutidx+lead:cutidx+lead+lhs_fill])

        # IF enough train cells on either side
        elif (lead<cutidx<lag):
            # print("In range. Cutidx = ", cutidx)
            lhs_train = data[cutidx-lead:cutidx-half_guard]
            rhs_train = data[cutidx+half_guard:cutidx+lead]
            # print("Size lhs = ", np.size(lhs_train))
            # print("Size rhs = ", np.size(rhs_train))

        # IF too few cells on the right, take some from left of LHS    
        elif (cutidx>(ns-lead) and cutidx+half_guard<ns):
            # LHS as normal 
            lhs_train = data[cutidx-lead:cutidx-half_guard]

            rhs_train = data[cutidx+half_guard:]
            rhs_fill = half_train-len(lhs_train)
            rhs_train.append(data[cutidx-lead-rhs_fill:cutidx-lead])

        elif (cutidx>(ns-lead) and cutidx+half_guard==ns):
            lhs_train = data[cutidx-lead:cutidx-half_guard]

            rhs_train = data[cutidx-lead-half_train:cutidx-lead]


        training_cells = np.concatenate((lhs_train,rhs_train))

        # ******************** Perform OS CFAR ***********************
        cut = data[cutidx]
        # print("Train cells number = ", np.size(training_cells))
        training_cells.sort()
        ZOS = training_cells[k]
        # print(ZOS)
        TOS = SOS*ZOS
        # print('TOS =', TOS)
        th[cutidx] = TOS
        # print('TOS =', th[cutidx])
        if cut > TOS:
            # index implies frequency. return magnitude for use in
            # determining max value
            result[cutidx] = cut
        # ************************************************************
    return Pfa, result, th





