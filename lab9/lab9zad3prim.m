% ############################################
% RADIO FM: DEKODER - przyklad
% Dekoder RDS wedlug standardu IEC 62106
% Program fm_dekoder_stereo.m - wersja rozszerzona
% Autor: Tomasz ZIELINSKI, tzielin@agh.edu.pl
% Modyfikacje: [Twoje imię]

clear all; close all;

% Parametr: wybierz przypadek do analizy
% 0 - bez PLL, idealny c38 (dla f = 38 kHz, 38001 Hz, z przesuniętą fazą)
% 1 - z PLL
mode_PLL = 1;

% Parametr: typ pilota zniekształconego
% 'a' - przesunięcie fazy
% 'b' - odstrojenie częstotliwości
% 'c' - przesunięcie + odstrojenie
pilot_type = 'b';

ifigs = 0;
fm_param_samples_LR   % wczytaj parametry
bwSERV = 250e3;     % bandwidth of an FM service

% Wczytanie odpowiedniego pliku
switch pilot_type
    case 'a'
        load stereo_fm_broken_pilot_a;
    case 'b'
        load stereo_fm_broken_pilot_b;
    case 'c'
        load stereo_fm_broken_pilot_b_7;
    otherwise
        error('Nieznany typ pilota');
end

y = I + 1i*Q;
N = length(y);

% Przesunięcie do DC
y = y .* exp(-1i*2*pi*bwSERV/fs*(0:N-1)');

% Filtracja pasmowa i zmiana próbkowania
[b,a] = butter( 4, (bwSERV)/(fs/2) );
y = filter( b, a, y );
y = y( 1 : fs/bwSERV : end );
fs = bwSERV;

% Demodulacja FM
dy = (y(2:end).*conj(y(1:end-1)));
y = atan2( imag(dy), real(dy) ); clear dy;

% MONO (L+R)
hLPaudio = fir1(L,(Abw/2)/(fs/2),kaiser(L+1,7));
ym = filter( hLPaudio, 1, y );
ym = ym(1:fs/Abw:end);

% PILOT 19 kHz - pasmo
fcentr = fpilot; df1 = 1000; df2 = 2000;
ff = [ 0 fcentr-df2 fcentr-df1 fcentr+df1 fcentr+df2 fs/2 ]/(fs/2);
fa = [ 0 0.01 1 1 0.01 0 ];
hBP19 = firpm(L,ff,fa);
p = filter(hBP19,1,y);

% --- SYGNAŁ NOŚNY c38 ---
%4: Generacja c38 bez PLL
Ny = length(p);
switch mode_PLL
    case 0  % BEZ PLL
        % Zadanie 4: Idealna nośna 38kHz
        f_test = 38e3;          % 38 kHz
        phi_test = 0;           % Brak przesunięcia fazowego
        c38 = cos(2*pi*f_test*(0:Ny-1)/fs + phi_test);
        
        % Zadanie 5: Test z częstotliwością 38001 Hz
        % f_test = 38001;      
        % c38 = cos(2*pi*f_test*(0:Ny-1)/fs + phi_test);
        
        % Zadanie 5: Test z przesunięciem fazowym
        % phi_test = pi/4;     
        % c38 = cos(2*pi*f_test*(0:Ny-1)/fs + phi_test);
        
    case 1  % Z PLL (Zadanie 6)
        mi1 = 1e-2; mi2 = mi1^2/4;
        theta = zeros(1,Ny);
        freq = 2*pi*fpilot/fs;
        for n = 1:Ny-1
            pherr = sin(theta(n)) * real(p(n));
            theta(n+1) = theta(n) + freq - mi1 * pherr;
            freq = freq - mi2 * pherr;
        end
        c38 = cos(2 * theta);  % Podwojenie częstotliwości do 38 kHz
end

% SYGNAŁ L-R: filtracja pasmowa
fcentr = fstereo; df1 = 10000; df2 = 12500;
ff = [ 0 fcentr-df2 fcentr-df1 fcentr+df1 fcentr+df2 fs/2 ]/(fs/2);
fa = [ 0 0.01 1 1 0.01 0 ];
hBP38 = firpm(L,ff,fa);
ys = filter(hBP38,1,y);

% Przesunięcie L-R do DC
ys = real(ys(:) .* c38(:));
ys = filter( hLPaudio, 1, ys );
ys = ys(1:fs/Abw:end);

% Synchronizacja opóźnień
opoz = (L/2)/(fs/Abw);
ym = ym(1:end-opoz);
ys = 2 * ys(1+opoz:end);  % 2 od demodulacji DSB

% Lewy i prawy kanał
yL = 0.5*(ym + ys);
yR = 0.5*(ym - ys);

% Filtr de-emfazy
yL = filter(b_de,a_de,yL);
yR = filter(b_de,a_de,yR);

% Obliczenie separacji kanałów (wzajemne przecieki)
separacja_LR = 10*log10(mean(yL.^2)/mean((yL-yR).^2));
separacja_RL = 10*log10(mean(yR.^2)/mean((yR-yL).^2));
disp(['Separacja kanałów L->R: ' num2str(separacja_LR) ' dB']);
disp(['Separacja kanałów R->L: ' num2str(separacja_RL) ' dB']);

% Wykres kanałów
figure;
subplot(2,1,1);
plot(yL,'b'); hold on; plot(yR,'r'); 
legend('Lewy','Prawy'); title('Kanały stereo');
xlabel('Próbki'); ylabel('Amplituda');

% Spektrogram (dla scenariusza 7)
subplot(2,1,2);
spectrogram(real(y), hanning(1024), 512, 2048, fs, 'yaxis');
title(['Sygnał hybrydowy (pilot ' pilot_type ')']);

% Odtwarzanie
soundsc([yL yR], Abw);