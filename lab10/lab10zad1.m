% ----------------------------------------------------------
% Tabela 19-4 (str. 567)
% Ćwiczenie: Kompresja sygnału mowy według standardu LPC-10
% ----------------------------------------------------------

clear all; clf;

[x,fpr]=audioread('mowa.wav');	      
subplot(2,1,1); plot(x); title('sygnał mowy - oryginalny'); 
pause	
soundsc(x,fpr);								% odtwórz na głośnikach

% 1a) Preemfaza
x_preemf = filter([1 -0.9735], 1, x);	% filtracja wstępna (preemfaza)
subplot(2,1,2); plot(x_preemf); title('sygnał mowy po preemfazie');
pause

N=length(x);	  
Mlen=240;		   
Mstep=180;		   
Np=10;			   
gdzie=Mstep+1;	

lpc=[];								  
s=[];									  
ss=[];								   
bs=zeros(1,Np);					   
Nramek=floor((N-Mlen)/Mstep+1);	

for  nr = 1 : Nramek
    
    % pobierz kolejny fragment sygnału
    n = 1+(nr-1)*Mstep : Mlen + (nr-1)*Mstep;
    bx = x_preemf(n);
    
    % ANALIZA - wyznacz parametry modelu ---------------------------------------------------
    bx = bx - mean(bx);  % usuń wartość średnią
    
    % autokorelacja
    for k = 0 : Mlen-1
        r(k+1) = sum( bx(1 : Mlen-k) .* bx(1+k : Mlen) ); 
    end
    
    figure(2); clf;
    subplot(4,1,1); plot(bx); title(['fragment sygnału mowy, ramka nr ' num2str(nr)]);
    
    subplot(4,1,2); plot(r); hold on;
    threshold = 0.35 * r(1);
    yline(threshold, 'r--', 'Próg 0.35*r(1)');
    title('funkcja autokorelacji z zaznaczonym progiem');
    
    % maksimum autokorelacji po przesunięciu offset
    offset=20; 
    rmax=max( r(offset : Mlen) );	   
    imax=find(r==rmax);								   
    if ( rmax > threshold ) 
        T=imax; 
        voiced = true;
    else 
        T=0; 
        voiced = false;
    end 
    if (T>80) 
        T=round(T/2); 
    end		
    
    % pokaż decyzję o dźwięczności
    if voiced
        f0 = fpr / T;
        disp(['Ramka ' num2str(nr) ': DŹWIĘCZNA, T=' num2str(T) ', f0=' num2str(f0) ' Hz']);
    else
        disp(['Ramka ' num2str(nr) ': BEZDŹWIĘCZNA']);
    end
    
    % macierz autokorelacji i wsp. predykcji
    rr(1:Np,1)=(r(2:Np+1))';
    for m=1:Np
        R(m,1:Np)=[r(m:-1:2) r(1:Np-(m-1))];
    end
    a=-inv(R)*rr;		
    wzm=r(1)+r(2:Np+1)*a;	
    
    % 1b) widmo filtra traktu głosowego
    [H,w] = freqz(1,[1;a], 512, fpr);		
    subplot(4,1,3); plot(w, 20*log10(abs(H))); 
    title('widmo filtra traktu głosowego (dB)'); xlabel('częstotliwość [Hz]');
    
    lpc=[lpc; T; wzm; a; ];
    
    % SYNTEZA ----------------------------------------------------------------------
    T = 0;  % testowo: T = 80, 50, 30, 0
    if (T~=0) gdzie=gdzie-Mstep; end					
    for n=1:Mstep
        if( T==0)
            pob=2*(rand(1,1)-0.5); gdzie=(3/2)*Mstep+1;		
        else
            if (n==gdzie) pob=1; gdzie=gdzie+T;	   
            else pob=0; end
        end
        ss(n)=wzm*pob-bs*a;	
        bs=[ss(n) bs(1:Np-1) ];	
    end
    
    subplot(4,1,4); plot(ss); title('zsyntezowany fragment sygnału mowy');
    pause(0.5)
    
    s = [s ss];		
end

% 1f) porównanie całości
s=filter(1,[1 -0.9735],s); % deemfaza

figure(3); clf;
subplot(2,1,1); plot(x); title('oryginalny sygnał mowy');
subplot(2,1,2); plot(s); title('mowa zsyntezowana');
pause

soundsc(s, fpr)
