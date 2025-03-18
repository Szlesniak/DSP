% Parametry
fs = 8000; % Czestotliwosc probkowania
czas = 4; % Czas trwania nagrania w sekundach

[y, fs] = audioread('mowa.wav')

% Wyswietlenie sygnalu
figure;
plot(y);
title('Oryginalny sygnal');

% Odsłuchanie sygnału
soundsc(y, fs);
pause(czas + 1);

% Wykonanie DCT
c = dct(y);
figure;
stem(c);
title('Wspolczynniki DCT');

% Synteza mowy z 25% pierwszych wspolczynnikow
c1 = [c(1:round(0.25*length(c))); zeros(length(c)-round(0.25*length(c)),1)];
y1 = idct(c1);
figure;
plot(y1);
title('Synteza mowy z 25% wspolczynnikow');
soundsc(y1, fs);
pause(czas + 1);

% Synteza mowy z 75% ostatnich wspolczynnikow
c2 = [zeros(length(c)-round(0.75*length(c)),1); c(end-round(0.75*length(c))+1:end)];
y2 = idct(c2);
figure;
plot(y2);
title('Synteza mowy z 75% wspolczynnikow');
soundsc(y2, fs);
pause(czas + 1);

% Usuwanie wspolczynnikow ponizej 50
c3 = c;
c3(abs(c) < 50) = 0;
y3 = idct(c3);
figure;
plot(y3);
title('Mowa po usunięciu wspolczynnikow <50');
soundsc(y3, fs);
pause(czas + 1);

% Usuwanie wspolczynnikow od 100 do 200
c4 = c;
c4(100:200) = 0;
y4 = idct(c4);
figure;
plot(y4);
title('Mowa po usunieciu wspolczynnikow 100-200');
soundsc(y4, fs);
pause(czas + 1);

% Dodanie zaklocenia sinusoidalnego
zaklocenie = 0.5 * sin(2 * pi * 250 / fs * (0:length(y)-1)');
y_zak = y + zaklocenie;
figure;
plot(y_zak);
title('Sygnał z zakloceniem');
soundsc(y_zak, fs);
pause(czas + 1);

% DCT sygnalu z zakloceniem
c_zak = dct(y_zak);
figure;
stem(c_zak);
title('DCT sygnalu z zakloceniem');

% Usuniecie zaklocenia
[~, idx] = max(abs(c_zak));
c_zak(idx) = 0;
y_filt = idct(c_zak);
figure;
plot(y_filt);
title('Sygnał po usunięciu zaklocenia');
soundsc(y_filt, fs);
