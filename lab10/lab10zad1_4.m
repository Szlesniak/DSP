% --------------------------------------------
% Kwantyzacja współczynników „a” - punkt 4
% --------------------------------------------

clear all; clf;

[x,fpr]=audioread('mowa.wav');	      
[x,~] = audioread('mowa.wav');	      
Mlen = 240;    
Mstep = 180;   
Np = 10;       

[x, fpr] = audioread('mowa.wav');
x_preemf = filter([1 -0.9735], 1, x);
N = length(x);
Nramek = floor((N - Mlen) / Mstep + 1);
lpc = [];

% Zbierz parametry
for nr = 1:Nramek
    n = 1+(nr-1)*Mstep : Mlen+(nr-1)*Mstep;
    bx = x_preemf(n);
    bx = bx - mean(bx);
    for k = 0:Mlen-1
        r(k+1) = sum(bx(1:Mlen-k) .* bx(1+k:Mlen));
    end
    
    offset = 20;
    rmax = max(r(offset:Mlen));
    imax = find(r == rmax);
    if rmax > 0.35 * r(1)
        T = imax;
    else
        T = 0;
    end
    if T > 80
        T = round(T / 2);
    end
    
    rr = (r(2:Np+1))';
    for m = 1:Np
        R(m,:) = [r(m:-1:2) r(1:Np-(m-1))];
    end
    a = -inv(R) * rr;
    wzm = r(1) + r(2:Np+1) * a;
    
    lpc = [lpc; T; wzm; a];
end

disp(['Zebrano ' num2str(Nramek) ' ramek.']);

% Kwantyzacja
bit_pairs = [8, 6, 6, 4, 4]; % na parę współczynników
bits_G = 8;
bits_T = 6;

total_bits_per_frame = bits_G + bits_T;

for i = 1:Nramek
    idx_start = (i-1)*(Np + 2) + 1;
    T = lpc(idx_start);
    G = lpc(idx_start + 1);
    a_coeffs = lpc(idx_start + 2 : idx_start + 1 + Np);
    
    % Kwantyzacja współczynników a (pary)
    pair_bits = 0;
    for p = 1:5
        a1 = a_coeffs(2*p - 1);
        a2 = a_coeffs(2*p);
        
        bits_for_pair = bit_pairs(p);
        pair_bits = pair_bits + 2 * bits_for_pair;
        
        % Tu można zrobić rzeczywistą kwantyzację np.:
        % max_a = max(abs([a1 a2]));
        % quant_a1 = round((a1 / max_a) * (2^(bits_for_pair - 1) - 1));
        % quant_a2 = round((a2 / max_a) * (2^(bits_for_pair - 1) - 1));
        % Ale do liczenia bitrate liczymy tylko bity.
    end
    
    total_bits_per_frame = total_bits_per_frame + pair_bits;
end

% Obliczenie przepływności
frame_duration_sec = Mstep / fpr; % ile sekund trwa jedna ramka
bitrate = total_bits_per_frame / Nramek / frame_duration_sec;

disp(['Średnia liczba bitów na ramkę: ' num2str(total_bits_per_frame / Nramek)]);
disp(['Przepływność kodeka (bitrate): ' num2str(bitrate/1000) ' kb/s']);

