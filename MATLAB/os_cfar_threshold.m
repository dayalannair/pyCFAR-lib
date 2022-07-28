addpath('../')
addpath('matlab_lib\')
pytbl = readtable("threshold.txt");
pyfftutbl = readtable("pyFFTup.txt");
iq_tbl=readtable('IQ_tri_20kmh.txt','Delimiter' ,' ');
sweeps = 1500; % Same as in Python
i_up = table2array(iq_tbl(sweeps,1:200));
i_down = table2array(iq_tbl(sweeps,201:400));
q_up = table2array(iq_tbl(sweeps,401:600));
q_down = table2array(iq_tbl(sweeps,601:800));

% Square Law detector
iq_u= i_up.^2 + q_up.^2;
iq_d = i_down.^2 + q_down.^2;

% Taylor Window
% n_samples = 200;
% nbar = 4;
% sll = -38;
% twinu = taylorwin(n_samples, nbar, sll);
% twind = taylorwin(n_samples, nbar, sll);
% iq_u = iq_u.*twinu.';
% iq_d = iq_d.*twind.';

% FFT 
n_fft = 512;
IQ_UP = fft(iq_u,n_fft);
IQ_DN = fft(iq_d,n_fft);

% Halve FFTs
IQ_UP = IQ_UP(1:n_fft/2);
IQ_DN = IQ_DN(n_fft/2+1:end);
IQ_UP1 = IQ_UP;
%     disp(IQ_DN)
% Null feedthrough
nul_width_factor = 0.04;
num_nul = round((n_fft/2)*nul_width_factor);
IQ_UP(1:num_nul) = 0;
IQ_DN(end-num_nul+1:end) = 0;

% flip
IQ_DN = flip(IQ_DN,2);

% From Python for SOS = 10
% Pfa = 1.816061631396838e-05;
% Pfa = 10e-3
Pfa = 0.02127659574468085
train = 50;
guard = 4;
N = train - guard;
% k = round(3*N/4);
% k = N;
k = train
OS = proc_oscfar(train, guard, k, Pfa);

% Filter peaks/ peak detection
[up_os, upth] = OS(abs(IQ_UP)', 1:n_fft/2);
[dn_os, dnth] = OS(abs(IQ_DN)', 1:n_fft/2);

IQ_UP_mag = absmagdb(IQ_UP);
pyth = table2array(pytbl);
pyfftup = table2array(pyfftutbl);
%%
close all
figure
tiledlayout(1,2)
nexttile
plot(absmagdb(pyth'), 'DisplayName','Python threshold')
axis([0 256 100 160])
hold on
plot(absmagdb(pyfftup), 'DisplayName','Python FFT')
title('Python FFT and OS-CFAR threshold')
hold off
legend
nexttile
plot(absmagdb(IQ_UP'), 'DisplayName','MATLAB FFT')
axis([0 256 100 160])
hold on
plot(absmagdb(upth'), 'DisplayName','MATLAB threshold')
title('MATLAB FFT and OS-CFAR threshold')
hold off
legend
% hold on
% plot(absmagdb(IQ_UP1))