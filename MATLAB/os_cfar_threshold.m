addpath('../')
pytbl = readtable("threshold.txt");
iq_tbl=readtable('IQ_tri_20kmh.txt','Delimiter' ,' ');
sweeps = 1; % Same as in Python
i_up = table2array(iq_tbl(sweeps,1:200));
i_down = table2array(iq_tbl(sweeps,201:400));
q_up = table2array(iq_tbl(sweeps,401:600));
q_down = table2array(iq_tbl(sweeps,601:800));

% Square Law detector
iq_u= i_up.^2 + q_up.^2;
iq_d = i_down.^2 + q_down.^2;

% FFT 
n_fft = 512;
IQ_UP = fft(iq_u,n_fft);
IQ_DN = fft(iq_d,n_fft);

% Halve FFTs
IQ_UP = IQ_UP(1:n_fft/2);
IQ_DN = IQ_DN(n_fft/2+1:end);

%     disp(IQ_DN)
% Null feedthrough
nul_width_factor = 0.04;
num_nul = round((n_fft/2)*nul_width_factor);
IQ_UP(1:num_nul) = 0;
IQ_DN(end-num_nul+1:end) = 0;

% flip
IQ_DN = flip(IQ_DN,2);

% From Python for SOS = 10
Pfa = 1.816061631396838e-05;
train = 50;
guard = 4;
N = train - guard;
k = round(3*N/4);
OS = proc_oscfar(train, guard, k, Pfa);

% Filter peaks/ peak detection
[up_os, upth] = OS(abs(IQ_UP)', double(1:n_fft/2));
[dn_os, dnth] = OS(abs(IQ_DN)', double(1:n_fft/2));


pyth = table2array(pytbl);
%%
close all
figure
plot(th)
hold on
plot(upth)
hold on
plot(abs(IQ_UP(1,:)))