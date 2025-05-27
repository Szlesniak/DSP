function [Y,G]=agc(Xin,alfa)
A=0;
    for i=1:length(Xin)
        Y(i)=A*Xin(i);
        A = A + alfa*(1-abs(Y(i))); %domyslny poziom odniesienia przyjmujemy na 1 zeby nie mnozyc parametrow
        G(i)=A;
    end
end