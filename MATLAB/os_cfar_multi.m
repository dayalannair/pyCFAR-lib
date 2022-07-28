addpath('../')
addpath('matlab_lib\')
% ---------------- MATLAB -------------------------------
iq_tbl=readtable('IQ_tri_20kmh.txt','Delimiter' ,' ');
sweeps = 1:500; % Same as in Python
i_up = table2array(iq_tbl(sweeps,1:200));
i_down = table2array(iq_tbl(sweeps,201:400));
q_up = table2array(iq_tbl(sweeps,401:600));
q_down = table2array(iq_tbl(sweeps,601:800));

% Square Law detector
iq_u= i_up.^2 + q_up.^2;
iq_d = i_down.^2 + q_down.^2;

% Taylor Window
n_samples = 200;
nbar = 4;
sll = -38;
twinu = taylorwin(n_samples, nbar, sll);
twind = taylorwin(n_samples, nbar, sll);
iq_u = iq_u.*twinu.';
iq_d = iq_d.*twind.';

% FFT 
n_fft = 512;%512;
nul_width_factor = 0.04;
num_nul = round((n_fft/2)*nul_width_factor);

IQ_UP = fft(iq_u,n_fft,2);
IQ_DN = fft(iq_d,n_fft,2);

% Halve FFTs
IQ_UP = IQ_UP(:, 1:n_fft/2);
IQ_DN = IQ_DN(:, n_fft/2+1:end);

% Null feedthrough
IQ_UP(:, 1:num_nul) = 0;
IQ_DN(:, end-num_nul+1:end) = 0;


% flip
IQ_DN = flip(IQ_DN,2);

% From Python for SOS = 10
% Pfa = 1.816061631396838e-05;
% Pfa = 10e-3
Pfa = 0.0008865248226950354
train = 50;
guard = 4;
N = train - guard;
% k = round(3*N/4);
% k = N;
k = train
OS = proc_oscfar(train, guard, k, Pfa);
[up_os, upth] = OS(abs(IQ_UP)', 1:n_fft/2);
[dn_os, dnth] = OS(abs(IQ_DN)', 1:n_fft/2);
os_pku = abs(IQ_UP).*up_os';
os_pkd = abs(IQ_DN).*dn_os';
% ----------------- PYTHON --------------------------
pythtbl = readtable("threshold.txt");
pyfftutbl = readtable("pyFFTup.txt");
pypkutbl = readtable("oscfar_up_pks.txt");
pyIQ_UPmag = table2array(pyfftutbl);
pythresh = table2array(pythtbl);
pypksup = table2array(pypkutbl);
sweeps = size(pyfftutbl, 2);
%%
close all
figure

for sweep = 1:sweeps
    tiledlayout(2,1)
    nexttile
    plot(absmagdb(pyIQ_UPmag(sweep,:)))
    title('Python OS CFAR with Pfa = 0.00089, Train = 50, Guard = 4')
    hold on
    plot(absmagdb(pythresh(sweep,:)))
    hold on
    stem(absmagdb(pypksup(sweep,:)))
    hold off
    nexttile
    plot(absmagdb(IQ_UP(sweep,:)))
    title('MATLAB OS CFAR with Pfa = 0.00089, Train = 50, Guard = 4')
    hold on
    % Note the swapped rows and cols
    plot(absmagdb(upth(:, sweep)))
    hold on
    stem(absmagdb(os_pku(sweep,:)))
    pause(0.1)
    drawnow;
end