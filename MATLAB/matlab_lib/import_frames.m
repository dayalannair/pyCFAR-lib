function [iq, fft_frames, iq_frames, n_frames] = import_frames(n_spf, n)
    % path relative to folder that function is called in
%     addpath('../../../../OneDrive - University of Cape Town/RCWS_DATA/M3_sawtooth_data/');
    addpath('../../../../OneDrive - University of Cape Town/RCWS_DATA/m4_rustenberg/');
%     iq_tbl=readtable('IQ_sawtooth75_60.txt', 'Delimiter' ,' ');
    iq_tbl=readtable('IQ_saw_100_40_2022-07-08 12-02-00.txt', 'Delimiter' ,' ');
    i_dat = table2array(iq_tbl(:,1:n));
    q_dat = table2array(iq_tbl(:,n+1:2*n));
    iq = i_dat + 1i*q_dat;
    
    n_samples = size(iq,2);
    n_sweeps = size(iq,1);
    n_frames = round(n_sweeps/n_spf);

    fft_frames = zeros(n_samples, n_spf, n_frames);
    iq_frames = zeros(n_samples, n_spf, n_frames);
    for i = 1:n_frames
        p1 = (i-1)*n_spf + 1;
        p2 = i*n_spf;
        fft_frames(:,:,i) = fft2(iq(p1:p2, :).');
        iq_frames(:,:,i) = iq(p1:p2, :).';
    end
end