#
#
#
#
# train = num training cells on one side. Must be even!
# guard = same format as train
# cut = cell under test
# idx = index

import numpy as np


def os_cfar(train, guard, rank, Pfa, data):
    # window length is 2*num train cells
    window = np.zeros(len(data))
    for cutidx in range(len(data)):
        print(cutidx)
        print(data[0])
        # if not enough training cells,
        # set first cells to the first cut
        if cutidx <= train + guard:

            win_gap = len(data[0:cutidx])

            # set window elements out of data range to first element
            window[0:train-1-cutidx] = data[0]
            # set rest of left side cells
            window[train-cutidx:train-1] = data[0:cutidx-guard]
            # cells to the right of cutidx
            window[train:2*train - 1] = data[cutidx+guard:cutidx+train]
        
        # for the opposite side    
        elif cutidx + guard + train > len(data):
            win_gap = len(data) - cutidx
            # cells to the left of CUT excl. guard
            window[    0:train-1] = data[cutidx-guard-train:cutidx-guard]
            # cells on right up to the end
            window[train:2*train - 1 + win_gap] = data[cutidx+guard:]
            # pad additional training cells with last cell in range
            window[2*train + win_gap:2*train - 1] = data[len(data)]

        else:
            # cells to the left of CUT excl. guard
            window[    0:train-1] = data[cutidx-guard-train:cutidx-guard]
            # cells to the right of CUT excl. guard
            window[train:2*train - 1] = data[cutidx+guard:cutidx+guard+train]

