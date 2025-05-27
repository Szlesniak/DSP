clear all; clc; close all;

try
    [x, fpr] = audioread('mowa.wav');
catch
    error('Audio file not found');
end
phase_accum = 0;
global_sample_idx = 0;
N = length(x);
Mlen = 240;
Mstep = 180;
Np = 10;
gdzie = Mstep+1;
Nramek = floor((N-Mlen)/Mstep)+1;

s = zeros(1, Nramek*Mstep);
prev_T = [];

for nr = 1:Nramek
    n = (1:Mlen) + (nr-1)*Mstep;
    bx = x(n);
    bx = bx - mean(bx);

    % ---------------------------------------------------------------------
    % [4.1] ULEPSZONY ALGORYTM DETEKCJI U/V (0.5 pkt)
    % Uwzględnia: energię, adaptacyjne śledzenie tonu podstawowego, brak skoków,
    % analizę periodiczności z wykorzystaniem korelacji.
    % ---------------------------------------------------------------------
    r = zeros(Mlen, 1);
    for k = 0:Mlen-1
        r(k+1) = sum(bx(1:Mlen-k) .* bx(1+k:Mlen));
    end
    [T, voiced] = improved_uv_detection(r, Mlen, prev_T);
    prev_T = T;

    % ---------------------------------------------------------------------
    % [4.2] ALGORYTM LEVINSONA zamiast inv(R) (0.5 pkt)
    % Obliczamy współczynniki LPC algorytmem Levinsona.
    % ---------------------------------------------------------------------
    a = levinson_durbin(r, Np);

    % ---------------------------------------------------------------------
    % [4.3] STRUKTURA KRATOWA + KWANTYZACJA gamma (0.5 pkt)
    % Zamiana LPC -> gamma (parametry kratowe), potem ich kwantyzacja.
    % ---------------------------------------------------------------------
    [gamma, quantized_gamma] = convert_to_lattice(a, 8);
    E = r(1) - a' * r(2:Np+1);
    wzm = sqrt(abs(E));
    if T ~= 0
        gdzie = gdzie - Mstep;
    end

    ss = zeros(1, Mstep);
    for n = 1:Mstep
        global_sample = (nr - 1)*Mstep + n;
        if T == 0
            pob = 2*(rand-0.5);  % szum dla bezdźwięcznych
        else
            f0 = fpr / T;
            phase_accum = phase_accum + 2*pi*f0 / fpr;
            pob = sin(phase_accum) + 0.1*(2*(rand-0.5));
        end
        % Symulacja filtru syntezy w strukturze kratowej (z użyciem gamma)
        f = pob;
        b = pob;
        for m = 1:Np
            f_new = f + quantized_gamma(m)*b;
            b = quantized_gamma(m)*f + b;
            f = f_new;
        end
        ss(n) = wzm * f;
    end

    start_idx = (nr-1)*Mstep + 1;
    end_idx = nr*Mstep;
    s(start_idx:end_idx) = ss;
    global_sample_idx = global_sample_idx + Mstep;
end

s = s(1:min(length(s), N));
s(~isfinite(s)) = 0;
s = s / (max(abs(s)) + eps);

figure;
subplot(2,1,1); plot(x); title('Original');
subplot(2,1,2); plot(s); title('Synthesized');
soundsc(s, fpr);

% ---------------------- FUNKCJE POMOCNICZE -------------------------------

function [T, voiced] = improved_uv_detection(r, Mlen, prev_T)
    energy = r(1);
    energy_threshold = 0.1 * max(r(:));
    
    f0_min = 50;
    f0_max = 400;
    min_lag = max(1, floor(1/f0_max * Mlen));
    max_lag = ceil(1/f0_min * Mlen);
    
    offset = max(20, min_lag);
    end_idx = min(max_lag, Mlen);
    [rmax, imax] = max(r(offset:end_idx));
    imax = imax + offset - 1;

    % Adaptacyjne śledzenie tonu podstawowego
    if ~isempty(prev_T) && isscalar(prev_T) && (prev_T > 0)
        if abs(imax - prev_T) > (0.2 * prev_T)
            imax = prev_T;
            rmax = r(imax);
        end
    end

    periodicity_ratio = rmax / (mean(r(offset:end_idx)) + eps);

    cond1 = isscalar(rmax) && isscalar(r(1)) && (rmax > 0.35*r(1));
    cond2 = isscalar(energy) && isscalar(energy_threshold) && (energy > energy_threshold);
    cond3 = isscalar(periodicity_ratio) && (periodicity_ratio > 1.5);

    if cond1 && cond2 && cond3
        T = imax;
        voiced = true;
    else
        T = 0;
        voiced = false;
    end

    if isscalar(T) && (T > max_lag)
        T = round(T/2);
    end
end

function a = levinson_durbin(r, Np)
    a = zeros(Np,1);
    E = r(1);
    for m = 1:Np
        if m > 1
            k = (r(m+1) - a(1:m-1)'*r(m:-1:2)) / (E + eps);
        else
            k = r(m+1)/E;
        end
        a(1:m) = [a(1:m-1); 0] - k*[0; flipud(a(1:m-1))];
        E = (1 - k^2) * E;
    end
end

function [gamma, quantized_gamma] = convert_to_lattice(a, bits)
    Np = length(a);
    gamma = zeros(Np,1);
    a_prev = a;
    for m = Np:-1:1
        gamma(m) = a_prev(m);
        if m > 1
            denom = max(1 - gamma(m)^2, eps);
            a_prev = (a_prev(1:m-1) - gamma(m)*flipud(a_prev(1:m-1))) / denom;
        end
    end
    levels = 2^(bits - 1) - 1;
    quantized_gamma = round((gamma + 1) * levels) / levels - 1;
end
