clear all; close all; clc;

%% Parametry sygnału
fs = 400e3;            % Częstotliwość próbkowania sygnału radiowego [Hz]
fc1 = 100e3;           % Częstotliwość nośna pierwszej stacji [Hz]
fc2 = 110e3;           % Częstotliwość nośna drugiej stacji [Hz]
dA = 0.25;              % Głębokość modulacji

%% Wczytanie sygnałów mowy
[x1, fsx] = audioread('mowa8000.wav');
x2 = flipud(x1);        % Sygnał od tyłu

% Normalizacja sygnałów
x1 = x1 / max(abs(x1)) * dA;
x2 = x2 / max(abs(x2)) * dA;

%% Nadpróbkowanie sygnałów modulujących
upsample_factor = fs / fsx;
x1_up = interp(x1, upsample_factor);
x2_up = interp(x2, upsample_factor);

% Dopasowanie długości
N = min(length(x1_up), length(x2_up));
x1_up = x1_up(1:N);
x2_up = x2_up(1:N);
t = (0:N-1)'/fs;

%% Implementacja własnego filtra Hilberta
M = 100;                % Rząd filtra
n = -M:M;
h = (1 - cos(pi * n)) ./ (pi * n);   % Filtr Hilberta z oknem
h(M+1) = 0;                          % Wartość w n=0

% Filtracja Hilberta
x1h = conv(x1_up, h, 'same');
x2h = conv(x2_up, h, 'same');

%% Generacja sygnałów zmodulowanych

% 1. DSB-C (Double Side Band with Carrier)
y_DSB_C = (1 + x1_up) .* cos(2*pi*fc1*t) + (1 + x2_up) .* cos(2*pi*fc2*t);

% 2. DSB-SC (Double Side Band with Suppressed Carrier)
y_DSB_SC = x1_up .* cos(2*pi*fc1*t) + x2_up .* cos(2*pi*fc2*t);

% 3. SSB-SC (Single Side Band with Suppressed Carrier)
% Dla pierwszej stacji używamy wersji z górną wstęgą boczną (USB, znak "-")
% Dla drugiej stacji używamy wersji z dolną wstęgą boczną (LSB, znak "+")
y_SSB_SC = 0.5 * x1_up .* cos(2*pi*fc1*t) - 0.5 * x1h .* sin(2*pi*fc1*t) ...
         + 0.5 * x2_up .* cos(2*pi*fc2*t) + 0.5 * x2h .* sin(2*pi*fc2*t);

%% Wykresy w dziedzinie czasu i częstotliwości
figure;

% DSB-C
subplot(3,2,1);
plot(t(1:1000), y_DSB_C(1:1000));
title('DSB-C w dziedzinie czasu');
xlabel('Czas [s]');
ylabel('Amplituda');

subplot(3,2,2);
plot_spectrum(y_DSB_C, fs);
title('Widmo DSB-C');
xlim([0 fs/2]);

% DSB-SC
subplot(3,2,3);
plot(t(1:1000), y_DSB_SC(1:1000));
title('DSB-SC w dziedzinie czasu');
xlabel('Czas [s]');
ylabel('Amplituda');

subplot(3,2,4);
plot_spectrum(y_DSB_SC, fs);
title('Widmo DSB-SC');
xlim([0 fs/2]);

% SSB-SC
subplot(3,2,5);
plot(t(1:1000), y_SSB_SC(1:1000));
title('SSB-SC w dziedzinie czasu');
xlabel('Czas [s]');
ylabel('Amplituda');

subplot(3,2,6);
plot_spectrum(y_SSB_SC, fs);
title('Widmo SSB-SC');
xlim([0 fs/2]);

% Funkcja do wyświetlania widma
function plot_spectrum(signal, fs)
    N = length(signal);
    f = (0:N-1)*fs/N;
    spectrum = abs(fft(signal))/N;
    plot(f(1:N/2), spectrum(1:N/2));
    xlabel('Częstotliwość [Hz]');
    ylabel('Amplituda');
    grid on;
end

%% Demodulacja sygnałów

% Funkcja demodulacji z wykorzystaniem filtra Hilberta
function demod_signal = demodulate_AM(signal, fc, fs, fsx, mode)
    % mode: 'DSB-C', 'DSB-SC', 'SSB-USB', 'SSB-LSB'
    
    t = (0:length(signal)-1)'/fs;
    
    % Generowanie sygnałów nośnych
    carrier = cos(2*pi*fc*t);
    carrier_h = sin(2*pi*fc*t); % Nośna przesunięta o 90 stopni
    
    % Implementacja filtra Hilberta
    M = 100;
    n = -M:M;
    h = (1 - cos(pi * n)) ./ (pi * n);
    h(M+1) = 0;
    
    switch mode
        case 'DSB-C'
            % Demodulacja DSB-C - detekcja obwiedni
            demod_signal = abs(hilbert(signal)) - 1;
            
        case 'DSB-SC'
            % Demodulacja synchroniczna DSB-SC
            mixed = signal .* carrier;
            % Filtr dolnoprzepustowy
            [b,a] = butter(6, fc/fs);
            demod_signal = filtfilt(b, a, mixed);
            
        case {'SSB-USB', 'SSB-LSB'}
            % Demodulacja SSB-SC - metoda synchroniczna z filtrem Hilberta
            mixed_i = signal .* carrier;
            mixed_q = signal .* carrier_h;
            
            % Filtracja Hilberta
            mixed_q_filtered = conv(mixed_q, h, 'same');
            
            if strcmp(mode, 'SSB-USB')
                demod_signal = mixed_i - mixed_q_filtered;
            else % SSB-LSB
                demod_signal = mixed_i + mixed_q_filtered;
            end
            
            % Filtr dolnoprzepustowy
            [b,a] = butter(6, fc/fs);
            demod_signal = filtfilt(b, a, demod_signal);
    end
    
    % Dekimacja do oryginalnej częstotliwości próbkowania audio
    downsample_factor = fs/fsx;
    demod_signal = decimate(demod_signal, downsample_factor);
    
    % Normalizacja
    demod_signal = demod_signal / max(abs(demod_signal));
end

% DSB-C
x1_DSB_C = demodulate_AM(y_DSB_C, fc1, fs, fsx, 'DSB-C');
x2_DSB_C = demodulate_AM(y_DSB_C, fc2, fs, fsx, 'DSB-C');
x2_DSB_C = flipud(x2_DSB_C); % Odwrócenie sygnału

% DSB-SC
x1_DSB_SC = demodulate_AM(y_DSB_SC, fc1, fs, fsx, 'DSB-SC');
x2_DSB_SC = demodulate_AM(y_DSB_SC, fc2, fs, fsx, 'DSB-SC');
x2_DSB_SC = flipud(x2_DSB_SC); % Odwrócenie sygnału

% SSB-SC (pierwsza stacja to USB, druga to LSB)
x1_SSB_SC = demodulate_AM(y_SSB_SC, fc1, fs, fsx, 'SSB-USB');
x2_SSB_SC = demodulate_AM(y_SSB_SC, fc2, fs, fsx, 'SSB-LSB');
x2_SSB_SC = flipud(x2_SSB_SC); % Odwrócenie sygnału

%% Odtworzenie sygnałów dźwiękowych
fprintf('Odtwarzanie zdekodowanych sygnałów...\n');

% DSB-SC
fprintf('\nDSB-SC - Stacja 1:\n');
sound(x1_DSB_C, fsx);
pause(length(x1_DSB_C)/fsx + 1);

fprintf('DSB-SC - Stacja 2 (odwrócony):\n');
sound(x2_DSB_C, fsx);
pause(length(x2_DSB_C)/fsx + 1);

% DSB-SC
fprintf('\nDSB-SC - Stacja 1:\n');
sound(x1_DSB_SC, fsx);
pause(length(x1_DSB_SC)/fsx + 1);

fprintf('DSB-SC - Stacja 2 (odwrócony):\n');
sound(x2_DSB_SC, fsx);
pause(length(x2_DSB_SC)/fsx + 1);

% SSB-SC
fprintf('\nSSB-SC - Stacja 1 (USB):\n');
sound(x1_SSB_SC, fsx);
pause(length(x1_SSB_SC)/fsx + 1);

fprintf('SSB-SC - Stacja 2 (LSB, odwrócony):\n');
sound(x2_SSB_SC, fsx);
pause(length(x1_SSB_SC)/fsx + 1);


%% Ocena jakości transmisji - współczynnik SNR
function snr_val = calculate_snr(original, received)
    error = original - received;
    snr_val = 10*log10(sum(original.^2)/sum(error.^2));
end

% Obliczenie SNR dla wszystkich demodulacji
snr_results = zeros(6,1);
snr_results(1) = calculate_snr(x1, x1_DSB_C);
snr_results(2) = calculate_snr(x2, x2_DSB_C);
snr_results(3) = calculate_snr(x1, x1_DSB_SC);
snr_results(4) = calculate_snr(x2, x2_DSB_SC);
snr_results(5) = calculate_snr(x1, x1_SSB_SC);
snr_results(6) = calculate_snr(x2, x2_SSB_SC);

% Wykresy porównawcze
figure;

% DSB-C
subplot(3,2,1);
plot(x1); hold on; plot(x1_DSB_C);
title(['DSB-C Stacja 1, SNR = ' num2str(snr_results(1)) ' dB']);
legend('Oryginał', 'Odtworzony');

subplot(3,2,2);
plot(x2); hold on; plot(x2_DSB_C);
title(['DSB-C Stacja 2, SNR = ' num2str(snr_results(2)) ' dB']);
legend('Oryginał', 'Odtworzony');

% DSB-SC
subplot(3,2,3);
plot(x1); hold on; plot(x1_DSB_SC);
title(['DSB-SC Stacja 1, SNR = ' num2str(snr_results(3)) ' dB']);
legend('Oryginał', 'Odtworzony');

subplot(3,2,4);
plot(x2); hold on; plot(x2_DSB_SC);
title(['DSB-SC Stacja 2, SNR = ' num2str(snr_results(4)) ' dB']);
legend('Oryginał', 'Odtworzony');

% SSB-SC
subplot(3,2,5);
plot(x1); hold on; plot(x1_SSB_SC);
title(['SSB-SC Stacja 1 (USB), SNR = ' num2str(snr_results(5)) ' dB']);
legend('Oryginał', 'Odtworzony');

subplot(3,2,6);
plot(x2); hold on; plot(x2_SSB_SC);
title(['SSB-SC Stacja 2 (LSB), SNR = ' num2str(snr_results(6)) ' dB']);
legend('Oryginał', 'Odtworzony');


% SSB-SC: dwie stacje na jednej nośnej (fc1)
x1_SSB_SC_fc1 = demodulate_AM(y_SSB_SC, fc1, fs, fsx, 'SSB-USB');
x2_SSB_SC_fc1 = demodulate_AM(y_SSB_SC, fc1, fs, fsx, 'SSB-LSB');
x2_SSB_SC_fc1 = flipud(x2_SSB_SC_fc1); % Odwrócenie sygnału

fprintf('Odtwarzanie stacji 1 (USB na fc1):\n');
sound(x1_SSB_SC_fc1, fsx);
pause(length(x1_SSB_SC_fc1)/fsx + 1);

fprintf('Odtwarzanie stacji 2 (LSB na fc1, odwrócony):\n');
sound(x2_SSB_SC_fc1, fsx);
