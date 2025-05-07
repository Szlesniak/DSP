% Wczytaj dane
load('lab08_fm.mat');  % zmienna to 'x'
fs = 2e6;              % częstotliwość próbkowania 2 MHz

% Filtr różniczkujący
diff_kernel = [-1 1];
x_diff = filter(diff_kernel, 1, x);

% Filtr pasmowo-przepustowy (200 kHz ± 100 kHz)
bpFilt = designfilt('bandpassfir', ...
    'FilterOrder', 200, ...
    'CutoffFrequency1', 100e3, ...
    'CutoffFrequency2', 300e3, ...
    'SampleRate', fs, ...
    'StopbandAttenuation1', 80, ...
    'StopbandAttenuation2', 80);
x_filtered = filter(bpFilt, x_diff);

% Obwiednia sygnału (moduł)
env = abs(x_filtered);

% Filtr dolnoprzepustowy (cutoff ~8 kHz)
lpFilt = designfilt('lowpassfir', ...
    'FilterOrder', 100, ...
    'CutoffFrequency', 8000, ...
    'SampleRate', fs);
demodulated = filter(lpFilt, env);

% Decymacja do 8000 Hz
fs_target = 8000;
decimation_factor = round(fs / fs_target);
output = downsample(demodulated, decimation_factor);

% Normalizacja i zapis
output = output / max(abs(output));
audiowrite('fm_decoded.wav', output, fs_target);

%% Opcjonalne
% Parametry
fs = 2e6;             % częstotliwość próbkowania
f_pass = [100e3 300e3]; % pasmo przepustowe
order = 200;          % rząd filtru

% Normalizacja częstotliwości (0–1)
f = [0 90e3 100e3 300e3 310e3 fs/2] / (fs/2);  % przejścia w okolicach 100k i 300k
m = [0 0 1 1 0 0];     % amplituda (1 w paśmie, 0 poza)

% Pożądana charakterystyka różniczkująca: mnożymy przez częstotliwość
w = f * (fs/2);        % częstotliwości w Hz
hd = m .* w;           % idealna charakterystyka różniczkująca

% Projektowanie filtru
b = firls(order, f, hd);  % filtr FIR LS

% Filtracja sygnału x
load('lab08_fm.mat');     % zakładam, że zmienna to 'x'
x_filtered = filter(b, 1, x);

% Reszta jak wcześniej (obwiednia, LPF, decymacja...)
env = abs(x_filtered);
lp = designfilt('lowpassfir', 'FilterOrder', 100, ...
    'CutoffFrequency', 8000, 'SampleRate', fs);
demod = filter(lp, env);
output = downsample(demod, round(fs / 8000));
output = output / max(abs(output));
sound(output, fs_target)
