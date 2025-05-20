%% Inicjalizacja
clear all;
close all;
clc;

%% Definicja rzeczywistej odpowiedzi impulsowej
h_true = zeros(256, 1);  % Indeksy od 1 do 256 (odpowiadające i=0 do 255)
h_true(256) = 0.8;        % i=255
h_true(121) = -0.5;       % i=120
h_true(31) = 0.1;         % i=30

%% 1. Identyfikacja przy użyciu sygnału mowy
% Wczytanie pliku dźwiękowego
[mowa, Fs] = audioread('mowa8000.wav');
mowa = mowa(:,1); % W przypadku stereo bierzemy tylko jeden kanał

% Ogranicz długość sygnału dla szybkości obliczeń
N = min(length(mowa), 8000); % 1 sekunda dla Fs=8000
mowa = mowa(1:N);

% Filtracja sygnału mowy przez obiekt (synteza sygnału referencyjnego)
mowa_znieksztalcona = filter(h_true, 1, mowa);

% Projektowanie filtru adaptacyjnego
order = 256; % Rząd filtru (dopasowany do długości h_true)
mu = 0.01;   % Krok adaptacji

% Inicjalizacja filtru LMS
lms = dsp.LMSFilter('Length', order, 'StepSize', mu);

% Adaptacja filtru
[y, e, w] = lms(mowa, mowa_znieksztalcona);

% Wizualizacja wyników
figure;
subplot(2,1,1);
stem(0:255, h_true, 'b', 'LineWidth', 1.5, 'MarkerSize', 5);
hold on;
stem(0:255, w, 'r', 'LineWidth', 1, 'MarkerSize', 3);
title('Identyfikacja odpowiedzi impulsowej - sygnał mowy');
legend('Rzeczywista odpowiedź impulsowa', 'Estymowana odpowiedź impulsowa');
xlabel('Próbka');
ylabel('Amplituda');
grid on;

subplot(2,1,2);
plot(abs(h_true - w));
title('Błąd estymacji');
xlabel('Próbka');
ylabel('Różnica amplitud');
grid on;

%% 2. Identyfikacja przy użyciu szumu białego - ulepszona wersja
% Generacja szumu białego o większej długości dla lepszej zbieżności
N_szum = 4*N; % 4 razy dłuższy sygnał niż dla mowy
szum = randn(N_szum, 1);

% Filtracja szumu przez obiekt
szum_znieksztalcony = filter(h_true, 1, szum);

% Optymalizacja parametrów filtru LMS
order_szum = 256; % Rząd filtru
mu_szum = 0.005;  % Mniejszy krok adaptacji dla precyzji

% Inicjalizacja filtru LMS z optymalnymi parametrami
lms_szum = dsp.LMSFilter('Length', order_szum, 'StepSize', mu_szum, ...
                         'Method', 'Normalized LMS', 'WeightsOutputPort', true);

% Adaptacja filtru - z dodatkowym śledzeniem błędów
[y_szum, e_szum, w_szum] = lms_szum(szum, szum_znieksztalcony);

% Ulepszona wizualizacja wyników
figure(2);
set(gcf, 'Position', [100 100 900 600]);

% Subplot 1: Porównanie odpowiedzi impulsowych
subplot(3,1,1);
stem(0:255, h_true, 'b', 'LineWidth', 1.5, 'MarkerSize', 8, 'MarkerFaceColor', 'b');
hold on;
stem(0:255, w_szum, 'r', 'LineWidth', 1.2, 'MarkerSize', 5, 'MarkerFaceColor', 'r');
title('Odpowiedź impulsowa: rzeczywista vs estymowana (szum biały)', 'FontSize', 12);
legend('Rzeczywista', 'Estymowana', 'Location', 'northeast');
xlabel('Indeks próbki');
ylabel('Amplituda');
grid on;
xlim([0 255]);
ylim([-0.6 0.9]);

% Subplot 2: Błąd estymacji z podkreśleniem kluczowych próbek
subplot(3,1,2);
error = h_true - w_szum;
stem(0:255, abs(error), 'm', 'LineWidth', 1.2, 'MarkerFaceColor', 'm');
hold on;
% Podświetlenie niezerowych punktów h_true
non_zero_idx = find(h_true ~= 0);
stem(non_zero_idx-1, abs(error(non_zero_idx)), 'g', 'LineWidth', 2, 'MarkerSize', 8);
title('Błąd estymacji z podkreśleniem kluczowych próbek', 'FontSize', 12);
legend('Całkowity błąd', 'Błąd dla niezerowych h_{true}', 'Location', 'northeast');
xlabel('Indeks próbki');
ylabel('|Błąd|');
grid on;
xlim([0 255]);

% Subplot 3: Śledzenie procesu adaptacji (średni błąd kwadratowy)
subplot(3,1,3);
window_size = 100;
mse = movmean(e_szum.^2, window_size);
plot(mse, 'LineWidth', 1.5);
title('Średni błąd kwadratowy (MSE) podczas adaptacji', 'FontSize', 12);
xlabel('Numer iteracji');
ylabel('MSE');
grid on;

% Dodatkowa analiza
fprintf('Średni błąd estymacji dla szumu białego: %.4f\n', mean(abs(error)));
fprintf('Maksymalny błąd: %.4f\n', max(abs(error)));
fprintf('Błąd dla kluczowych próbek:\n');
disp([non_zero_idx-1, h_true(non_zero_idx), w_szum(non_zero_idx), error(non_zero_idx)]);
%% Porównanie błędów estymacji
figure;
plot(0:255, abs(h_true - w), 'b', 'LineWidth', 1.5);
hold on;
plot(0:255, abs(h_true - w_szum), 'r', 'LineWidth', 1.5);
title('Porównanie błędów estymacji');
legend('Sygnał mowy', 'Szum biały');
xlabel('Próbka');
ylabel('Błąd estymacji');
grid on;