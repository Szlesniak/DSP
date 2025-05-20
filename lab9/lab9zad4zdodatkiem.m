clear all; close all;
load('ECG100.mat');
Fs = 500;
val = val(1,:);  % używamy pierwszego kanału
t = (0:length(val)-1) / Fs;

%% Dodanie szumu 50 Hz
noise_freq = 50;
noise = 0.3 * sin(2*pi*noise_freq*t);
ekg_noisy = val + noise;

%% Dodanie szumu mięśniowego (losowy + filtr dolnoprzepustowy)
muscle_noise = 0.5 * randn(size(t));  % losowy szum
fc = 1;  % dolnoprzepustowy filtr o f_c = 250 Hz
[b, a] = butter(4, fc/(Fs/2), 'low');
muscle_noise_filtered = filter(b, a, muscle_noise);

%% Sygnał zaszumiony 50 Hz + szum mięśniowy
ekg_total_noise = ekg_noisy + muscle_noise_filtered;

%% 1) LMS – usuwanie interferencji 50 Hz
mu = 0.001;
N = 32;
ref = sin(2*pi*noise_freq*t);  % sygnał odniesienia (50 Hz)
w = zeros(1, N);
y = zeros(size(ekg_total_noise));
e1 = zeros(size(ekg_total_noise));
x_ref = zeros(1, N);

for n = N:length(ekg_total_noise)
    x_ref = ref(n:-1:n-N+1);
    y(n) = w * x_ref';
    e1(n) = ekg_total_noise(n) - y(n);
    w = w + 2*mu*e1(n)*x_ref;
end

%% 2) LMS – predyktor liniowy (usuwanie szumu mięśniowego)
w = zeros(1, N);
y = zeros(size(ekg_total_noise));
e2 = zeros(size(ekg_total_noise));
x_pred = zeros(1, N);

for n = N+1:length(ekg_total_noise)
    x_pred = ekg_total_noise(n-1:-1:n-N);
    y(n) = w * x_pred';
    e2(n) = ekg_total_noise(n) - y(n);
    w = w + 2*mu*e2(n)*x_pred;
end

%% WIZUALIZACJA wyników
figure;
subplot(4,1,1); plot(t, ekg_total_noise); title('EKG + 50Hz + szum mięśniowy');
subplot(4,1,2); plot(t, e1); title('Po LMS (usuwanie 50Hz)');
subplot(4,1,3); plot(t, e2); title('Po LMS jako predyktor (szum mięśniowy)');
subplot(4,1,4); plot(t, val); title('Oryginalny EKG');
xlabel('Czas [s]');
