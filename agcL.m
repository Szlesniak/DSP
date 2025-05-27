function [Y,G]=agcL(Xin,alfa)
A=0;
    for i=1:length(Xin)
        Y(i)=exp(A)*Xin(i);
        A = A - alfa*log10(abs(Y(i))); %domyslny poziom odniesienia przyjmujemy na 1 zeby nie mnozyc parametrow
        G(i)=exp(A);
    end
end