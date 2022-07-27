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
    k = round(3*N/4)
    
    print("N (num training) = ", N)
    print("train half = ", half_train)
    print("Guard half = ", half_guard)
    print("k = ", k)
    print("ns = ", ns)
    # Pfa_numer = k*mt.factorial(N)* mt.factorial(k-1)*mt.factorial(SOS+N-k)
    # Pfa_denom = (mt.factorial(k)*mt.factorial(N-k))*mt.factorial(SOS+N)
    # Pfa = Pfa_numer/Pfa_denom
    Pfa = k*mt.factorial(N)/(mt.factorial(k)*mt.factorial(N-k)) \
        * mt.factorial(k-1)*mt.factorial(SOS+N-k)/mt.factorial(SOS+N)

    for cutidx in range(ns): #cutidx = index of cell under test
        if (lead<cutidx<lag):
            # print("In range. Cutidx = ", cutidx)
            cut = data[cutidx]
            lhs_train = data[cutidx-lead:cutidx-half_guard]
            rhs_train = data[cutidx+half_guard:cutidx+lead]
            # print("Size lhs = ", np.size(lhs_train))
            # print("Size rhs = ", np.size(rhs_train))

            training_cells = np.concatenate((lhs_train,rhs_train))
           
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

    return Pfa, result, th





