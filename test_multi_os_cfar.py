# from cfar_lib import os_cfar
from os_cfar_v4 import os_cfar
import numpy as np
from scipy.fft import fft
from scipy import signal
import matplotlib.pyplot as plt
from time import sleep
print("testing OS cfar")
with open("IQ_tri_20kmh.txt", "r") as raw_IQ:
		# split into sweeps
		sweeps = raw_IQ.read().split("\n")

fft_array       = np.empty([len(sweeps)-5000, 256])
threshold_array = np.empty([len(sweeps)-5000, 256])
up_peaks        = np.empty([len(sweeps)-5000, 256])

# ------------------------ Frequency axis -----------------
nfft = 512
n_fft = 512 
n_half = round(nfft/2)
fs = 200e3
# kHz Axis
fax = np.linspace(0, round(fs/2), round(n_half))
# c*fb/(2*slope)
tsweep = 1e-3
bw = 240e6
slope = bw/tsweep
c = 3e8
rng_ax = c*fax/(2*slope)

upth = np.full(n_half, 250)
dnth = np.full(n_half, 250)
fftu = np.full(n_half, 250)
fftd = np.full(n_half, 250)

plt.ion()

figure, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
line1, = ax[0].plot(rng_ax, fftd)
line2, = ax[0].plot(rng_ax, dnth)
line3, = ax[1].plot(rng_ax, fftu)
line4, = ax[1].plot(rng_ax, upth)

ax[0].set_title("Down chirp spectrum negative half flipped")
ax[1].set_title("Up chirp spectrum positive half")

ax[0].set_xlabel("Coupled Range (m)")
ax[1].set_xlabel("Coupled Range (m)")

ax[0].set_ylabel("Magnitude (dB)")
ax[1].set_ylabel("Magnitude (dB)")
ax[0].set_ylim([200, 400])
ax[1].set_ylim([200, 400])
for sweep in range(len(sweeps)-5000):
    # Extract samples from 1 sweep
    samples = np.array(sweeps[sweep].split(" "))
    i_data = samples[  0:400]
    q_data = samples[400:800]

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
    twin = signal.windows.taylor(200, nbar=3, sll=100, norm=False)

    iq_u = np.multiply(iq_u, twin)
    iq_d = np.multiply(iq_d, twin)

    fftu = fft(iq_u,n_fft)
    fftd = fft(iq_d,n_fft)
    # fftu = np.fft.fft(iq_u,n_fft)
    # fftd = np.fft.fft(iq_d,n_fft)
    # Halve FFTs
    # note: python starts from zero for this!
    fftu = fftu[0:round(n_fft/2)]
    fftd = fftd[round(n_fft/2):]
  
    # Null feedthrough
    nul_width_factor = 0.04
    num_nul = round((n_fft/2)*nul_width_factor)
    # note: python starts from zero for this!
    fftu[0:num_nul-1] = 0
    fftd[len(fftd)-num_nul:] = 0

    fftd = np.flip(fftd)

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

    Pfa, cfar_res_up, upth = os_cfar(half_train, half_guard, rank, SOS, abs(fftu))
    Pfa, cfar_res_dn, dnth = os_cfar(half_train, half_guard, rank, SOS, abs(fftd))
    # print("Expected Pfa = ", Pfa_expected)
    # print("SOS = ", SOS)
    # print("Actual Pfa for SOS = ", Pfa)
    
    # np.append(threshold_array, th)
    # np.append(fft_array, abs(fftu))
    
    # NOTE: no need to multiply as cfar function returns scaled values
    # up_peaks[sweep] = np.multiply(abs(fftu), cfar_res_up)
    up_peaks[sweep] = cfar_res_up
    threshold_array[sweep] = upth

    fft_array[sweep] = abs(fftu)
    
    upth = 20*np.log(upth)
    dnth = 20*np.log(dnth)
    fftu = 20*np.log(abs(fftu))
    fftd = 20*np.log(abs(fftd))

    # print(fftu)
    # print(len(cfar_res_up))
    line1.set_ydata(fftd)
    line2.set_ydata(dnth)
    line3.set_ydata(fftu)
    line4.set_ydata(upth)

    figure.canvas.draw()
    # sleep(0.1)
    figure.canvas.flush_events()


# print(fft_array)
# print("PFA for SOS = ", Pfa)
# print("Train = ", 2*half_train)
# print("Guard = ", 2*half_guard)
# fthname = "threshold.txt"
# np.savetxt(fthname, threshold_array, delimiter=' ', newline='\n')

# fftupname = "pyFFTup.txt"
# np.savetxt(fftupname,  fft_array, delimiter=' ', newline='\n')

# uppkname = "oscfar_up_pks.txt"
# np.savetxt(uppkname,  up_peaks, delimiter=' ', newline='\n')


# print(th)
# with open(fthname, 'w') as fth:
	# fth.write(th)
# print(cfar_res_up)