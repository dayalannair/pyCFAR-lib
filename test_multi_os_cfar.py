# from cfar_lib import os_cfar
from operator import length_hint
from turtle import up
from os_cfar_v2 import os_cfar
import numpy as np
from scipy.fft import fft
from scipy import signal
print("testing OS cfar")
with open("IQ_tri_20kmh.txt", "r") as raw_IQ:
		# split into sweeps
		sweeps = raw_IQ.read().split("\n")

fft_array       = np.empty([len(sweeps)-5000, 256])
threshold_array = np.empty([len(sweeps)-5000, 256])
up_peaks        = np.empty([len(sweeps)-5000, 256])
for sweep in range(len(sweeps)-5000):
    # Extract samples from 1 sweep
    samples = np.array(sweeps[sweep].split(" "))
    i_data = samples[  0:400-1]
    q_data = samples[400:800-1]

    # 32 bit for embedded systems e.g. raspberry pi
    i_data = i_data.astype(np.int32)
    q_data = q_data.astype(np.int32)
    # test = np.power([1,2,3,4],2)
    # print(test)
    # print(i_data)
    # NOTE: last element in slice not included
    iq_u = np.power(i_data[  0:200],2) + np.power(q_data[  0:200],2)
    iq_d = np.power(i_data[200:400],2) + np.power(q_data[200:400],2)
    # SLL specified as positive
    twinu = signal.windows.taylor(200, nbar=4, sll=38, norm=False)
    twind = signal.windows.taylor(200, nbar=4, sll=38, norm=False)

    iq_u = np.multiply(iq_u, twinu)
    iq_d = np.multiply(iq_u, twind)

    n_fft = 512 
    IQ_UP = fft(iq_u,n_fft)
    IQ_DN = fft(iq_d,n_fft)
    # print(len(IQ_UP))
    # IQ_UP = np.fft.fft(iq_u,n_fft)
    # IQ_DN = np.fft.fft(iq_d,n_fft)
    # Halve FFTs
    # note: python starts from zero for this!
    IQ_UP = IQ_UP[0:round(n_fft/2)]
    IQ_DN = IQ_DN[round(n_fft/2):]
    # print(len(IQ_UP))   
    # Null feedthrough
    nul_width_factor = 0.04
    num_nul = round((n_fft/2)*nul_width_factor)
    # note: python starts from zero for this!
    IQ_UP[0:num_nul-1] = 0
    IQ_DN[len(IQ_DN)-num_nul:] = 0
    # print(len(IQ_UP))
    # CFAR
    n_samples = len(iq_u)
    half_guard = n_fft/n_samples
    half_guard = int(np.floor(half_guard/2)*2) # make even

    half_train = round(20*n_fft/n_samples)
    half_train = int(np.floor(half_train/2))
    rank = 2*half_train -2*half_guard
    # rank = half_train*2
    Pfa_expected = 15e-3
    # factorial needs integer values
    SOS = 2
    # note the abs

    Pfa, cfar_res_up, th = os_cfar(half_train, half_guard, rank, SOS, abs(IQ_UP))
    # print("Expected Pfa = ", Pfa_expected)
    # print("SOS = ", SOS)
    # print("Actual Pfa for SOS = ", Pfa)
    
    # np.append(threshold_array, th)
    # np.append(fft_array, abs(IQ_UP))
    
    # NOTE: no need to multiply as cfar function returns scaled values
    # up_peaks[sweep] = np.multiply(abs(IQ_UP), cfar_res_up)
    up_peaks[sweep] = cfar_res_up
    threshold_array[sweep] = th

    fft_array[sweep] = abs(IQ_UP)



print(fft_array)
print("PFA for SOS = ", Pfa)
print("Train = ", 2*half_train)
print("Guard = ", 2*half_guard)
fthname = "threshold.txt"
np.savetxt(fthname, threshold_array, delimiter=' ', newline='\n')

fftupname = "pyFFTup.txt"
np.savetxt(fftupname,  fft_array, delimiter=' ', newline='\n')

uppkname = "oscfar_up_pks.txt"
np.savetxt(uppkname,  up_peaks, delimiter=' ', newline='\n')


# print(th)
# with open(fthname, 'w') as fth:
	# fth.write(th)
# print(cfar_res_up)