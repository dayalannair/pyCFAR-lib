function [fft_up, fft_dw, up_det, dw_det] = CFAR(trn, grd, ...
    Pfa, iq_u, iq_d, n_fft)
    
    %F = 0.015; % see relevant papers
    
    CFAR = phased.CFARDetector('NumTrainingCells',trn, ...%20
        'NumGuardCells',grd, ...%4
        'ThresholdFactor', 'Auto', ...
        'ProbabilityFalseAlarm', Pfa, ...
        'Method', 'SOCA');
    
    % FFT
    %n_fft = 200;%512;
    fft_up = fftshift(fft(iq_u,n_fft,2));
    fft_dw = fftshift(fft(iq_d,n_fft,2));
    
    % modify CFAR code to simultaneously record beat frequencies
    up_det = CFAR(abs(fft_up)', 1:n_fft);
    dw_det = CFAR(abs(fft_dw)', 1:n_fft);
return