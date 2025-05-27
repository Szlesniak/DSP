% LPC-10 z wykorzystaniem pelnego sygnalu resztkowego (residual)

clear all; clf;

[x, fpr] = audioread('mowa1.wav');
x = x(:); 

plot(x); title('sygnał mowy'); 
% soundsc(x,fpr);  pause

N = length(x);
Mlen = 256;
Mstep = 180;
Np = 10;

lpc = [];
s = [];
ss = [];
bs = zeros(1, Np);
Nramek = floor((N - Mlen) / Mstep + 1);

residual_all = cell(1, Nramek);  % przechowuje sygnaly resztkowe

use_simplified_residual = 1; % ustal na 0 lub 1

for nr = 1 : Nramek
    idx = 1 + (nr-1)*Mstep : Mlen + (nr-1)*Mstep;
    bx = x(idx);
    bx = bx - mean(bx);
    
    % --- AUTOKORELACJA i LPC ---
    for k = 0:Mlen-1
        r(k+1) = sum(bx(1:Mlen-k) .* bx(1+k:Mlen));
    end
    rr = r(2:Np+1)';
    for m = 1:Np
        R(m, :) = [r(m:-1:2), r(1:Np-(m-1))];
    end
    a = -inv(R) * rr;
    wzm = r(1) + r(2:Np+1) * a;

    % --- SYGNAŁ RESZTKOWY ---
    residual = filter([1; a], 1, bx);
    
    if use_simplified_residual
        % --- 1. FFT z zerowaniem do 256 ---
        if length(residual) > 256
            res_padded = residual(1:256);
        else
            res_padded = [residual; zeros(256 - length(residual), 1)];
        end
        W = abs(fft(res_padded));
        W_half = W(1:128);
        
        % --- 2. Wygładzenie (np. filtr dolnoprzepustowy) ---
        smooth_W = smoothdata(W_half, 'movmean', 5);
        
        % --- 3. Aproksymacja wielomianowa ---
        f = (0:127)'; % oś częstotliwości
        poly_order = 5;
        f_scaled = (f - mean(f)) / max(f);
        p_coeffs = polyfit(f, smooth_W, poly_order);
        
        % --- 4. Rekonstrukcja widma w dekoderze ---
        recon_W_half = polyval(p_coeffs, f);
        recon_W_half(recon_W_half < 0) = 0; % brak ujemnych wartości
        
        recon_W = [recon_W_half; flipud(recon_W_half(2:end-1))]; % symetria
        
        % --- 5. Odwrotna FFT (tylko amplituda, bez fazy) ---
        res_recon = real(ifft(recon_W));
        res = res_recon(1:Mstep);
        if nr == 10  % np. tylko dla 1. ramki
            figure; % otwarcie jednego okna

            subplot(2,1,1); % pierwszy wykres na górze
            plot(f, smooth_W);
            title(['Widmo przed aproksymacją (ramka ', num2str(nr), ')']);
        end
    else
        % Pełny sygnał resztkowy
        res = residual(1:Mstep);
    end
    
    % --- SYNTEZA ---
    bs = zeros(1, Np);
    for n = 1:Mstep
        pob = res(n);
        ss(n) = wzm * pob - bs * a;
        bs = [ss(n), bs(1:Np-1)];
    end
    
    s = [s, ss];
end

subplot(2,1,2); % drugi wykres pod spodem
plot(s); 
title('mowa zsyntezowana (resztkowa)');
soundsc(s,fpr)
