function X = sftmag(fft_in)
    X = fftshift(abs(fft_in));
end