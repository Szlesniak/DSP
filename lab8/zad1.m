close all; clc; clear;

% Wczytywanie pliku
data = open("lab08_am.mat");

% Wybieranie sygnału zgodnego z przedostatnią cyfrą indeksu
x = data.s4;

% Parametry
Fs = 1e3;             % częstotliwość próbkowania
Fc = 200;
M = 100;               % połowa rzędu filtru
N = 2*M + 1;          % rząd filtru (nieparzysty)
n = -M:M;             % indeksy próbek

% Ręczna definicja filtru Hilberta z oknem (raised cosine window)
h = (1 - cos(pi * n)) ./ (pi * n);   % wzór na filtr Hilberta z oknem
h(M+1) = 0;                          % wartość w n=0 jest osobno nadpisywana

% Konwolucja (pełna)
xh_full = conv(x, h,'same');               % wynik dłuższy niż x

% % Synchronizacja wejścia i wyjścia filtra
% Nx = length(x);
% x_sync  = x(M+1 : Nx-M);                          % ucięcie brzegów wejścia
% xh_sync = xh_full(2*M+1 : 2*M+length(x_sync));    % wyrównanie opóźnienia

% Sygnał analityczny
z = x + 1i * xh_full;  
m = abs(z);     % obwiednia (amplituda chwilowa)

figure;
plot(x,"b"); hold on;
plot(xh_full,"w"); hold on;
title("Sygnał przed i po Filtrze Hilberta")
xlabel('Numer próbki'); ylabel('Amplituda')
legend('x','HT(x)'); grid on;

figure;
plot(x,"b"); hold on;
plot(xh_full,"w"); hold on;
plot(m, 'r','LineWidth',1);
title("Sygnał przed i po Filtrze Hilberta (synchroizacja) oraz Obwiednia AM")
xlabel('Numer próbki'); ylabel('Amplituda')
legend('x','HT(x)','amp'); grid on;

% Analiza widmowa
M = abs(fft(m));
norM = M/max(M);
f = (0:length(M)-1)*(Fs/length(M));
figure;
plot(f, norM); xlim([0 100]);  % skup się na niskich częstotliwościach
title("Widmo obwiedni"); xlabel("Częstotliwość [Hz]"); ylabel("Amplituda");
grid on;

t = (0:length(m)-1)/Fs;
sig = m .* sin(2*pi*t*Fc);
plot(t,sig,'b'); hold on;
plot(t,xh_full,'w'); hold on;
