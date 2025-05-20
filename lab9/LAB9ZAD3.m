clear all; close all;
%% Parametry sygnału
Fs = 192e3;
t = 0:1/Fs:1;             % 1 sekunda
f_pilot = 19e3;
pilot = sin(2*pi*f_pilot*t);  % czysty pilot

%% Poziomy SNR do testu
SNRs = [0, 5, 10, 20];
alpha = 1e-2;
beta = alpha^2 / 4;

%% Przetwarzanie dla każdego poziomu szumu
figure;
for k = 1:length(SNRs)
    %% Dodanie szumu AWGN
    noisy = awgn(pilot, SNRs(k), 'measured');   % Sygnał z szumem
    
    %% Inicjalizacja PLL
    theta = zeros(1, length(t) + 1);
    freq = 2*pi*f_pilot/Fs;
    
    %% PLL
    for n = 1:length(noisy)
        perr = -noisy(n) * sin(theta(n));
        theta(n+1) = theta(n) + freq + alpha * perr;
        freq = freq + beta * perr;
    end
    
    %% Obliczenie błędu fazy (dla oceny zbieżności)
    true_phase = 2*pi*f_pilot/Fs * (0:length(t)-1);  % idealna faza (dopasowana do t)
    pll_phase = theta(1:end-1);                      % usuwamy ostatni punkt (PLL zawsze ma +1)
    phase_err = wrapToPi(pll_phase - true_phase);  % błąd fazy
    
    %% Wykres
    subplot(length(SNRs),1,k);
    plot(t, phase_err);
    title(['Błąd fazy PLL (SNR = ', num2str(SNRs(k)), ' dB)']);
    xlabel('Czas [s]');
    ylabel('Błąd [rad]');
    grid on;
end