function X = sftmagdb(fft_in)
    X = mag2db(fftshift(abs(fft_in)));
end
