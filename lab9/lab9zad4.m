clear all; close all;
load('ECG100.mat');   % zmienna: val, czemu val jest 2x2000 ?? czemu to 2?
Fs=500

t = (0:length(val)-1) / Fs;
val  = val(1,:);
% 50 hz szum 
noise_freq = 50;
noise = 0.3 * sin(2*pi*noise_freq*t);  % 30% ampl


ekg_noisy = val + noise;

% org syg
figure;
subplot(2,1,1); plot(t, val);
title('Oryginalny sygnał EKG');
xlabel('Czas [s]'); ylabel('Amplituda');
legend();

%zaszumiony
subplot(2,1,2); plot(t, ekg_noisy);
title('Sygnał EKG z zakłóceniem 50 Hz');
xlabel('Czas [s]'); ylabel('Amplituda');

% Parametry filtra adaptacyjnego
mu = 0.01;               % krok adaptacji
N = 32;                  % liczba współczynników (rozmiar filtra)
ref = sin(2*pi*noise_freq*t);   % odniesienie: czysty 50 Hz sygnał

% Inicjalizacja
w = zeros(1, N);                 % współczynniki filtra
y = zeros(size(ekg_noisy));      % wyjście filtra
e = zeros(size(ekg_noisy));      % błąd (oczyszczony sygnał)

% Bufor odniesienia
x_ref = zeros(1, N);

% LMS
size(ekg_noisy)
size(val)
for n = N:length(ekg_noisy)
    x_ref = ref(n:-1:n-N+1);          % wektor referencyjny
    y(n) = w * x_ref';                % wyjście filtra
    e(n) = ekg_noisy(n) - y(n);       % błąd (to jest oczyszczony sygnał)
    w = w + 2*mu*e(n)*x_ref;          % aktualizacja współczynników
    
end

% Wykresy porównawcze
figure;
subplot(3,1,1); plot(t, ekg_noisy); title('Sygnał EKG z zakłóceniem 50 Hz');
subplot(3,1,2); plot(t, e); title('Sygnał po filtrze LMS');
subplot(3,1,3); plot(t, val); title('Oryginalny sygnał EKG (dla porównania)');
xlabel('Czas [s]');
