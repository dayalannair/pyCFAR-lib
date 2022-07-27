function [fft_up, fft_dw, up_det, dw_det, detu_scaled, detd_scaled] = myCFAR(trn, grd, ...
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
    
    % null feedthrough
    % each sample is 1 kHz. therefore we are filtering 5 kHz which corresp
    % to 3 meterss
    fft_up(:,95:105) = 0;
    fft_dw(:,95:105) = 0;

    % modify CFAR code to simultaneously record beat frequencies
    up_det = CFAR(abs(fft_up).', 1:n_fft);
    dw_det = CFAR(abs(fft_dw).', 1:n_fft);

    % OPTIONAL
    % scale CFAR by FFT
    detu_scaled = up_det.'.*abs(fft_up);
    detd_scaled = dw_det.'.*abs(fft_dw);
return