% ----------------------------------------------------------
% Eksperymenty pobudzenia w dekoderze LPC
% ----------------------------------------------------------

clear all; clf;

[x,fpr]=audioread('mowa.wav');	      
plot(x); title('sygnał mowy'); 	
soundsc(x,fpr); pause

N=length(x);
Mlen=240; Mstep=180; Np=10;
gdzie=Mstep+1;

lpc=[]; s=[]; ss=[]; bs=zeros(1,Np);
Nramek=floor((N-Mlen)/Mstep+1);

x=filter([1 -0.9735], 1, x);  % preemfaza

tryb = 'E2';  % A, B, C, D, E1, E2

% Jeśli tryb D: wczytaj coldvox.wav
if strcmp(tryb,'E1')
    [coldvox,~]=audioread('coldvox.wav');
    coldvox_idx = 1;
end

% Jeśli tryb E: przygotuj sygnał resztkowy
if strcmp(tryb,'E1') || strcmp(tryb,'E2')
    % wybierz ręcznie stały dźwięczny fragment (np. próbki 10000-10500)
    frag = x(10000:10500);
    frag = frag - mean(frag);
    for k = 0:Mlen-1
        r(k+1) = sum(frag(1:Mlen-k) .* frag(1+k:Mlen));
    end
    rr=(r(2:Np+1))';
    for m=1:Np
        R(m,:)=[r(m:-1:2) r(1:Np-(m-1))];
    end
    a=-inv(R)*rr;
    resztka = filter([1; a], 1, frag);
    T_resztka = 80;  % przyjmij okres
    if strcmp(tryb,'E1')
        pobudzenie = resztka(1:T_resztka);
    else
        num_okresy = 5;
        reshaped = reshape(resztka(1:num_okresy*T_resztka), T_resztka, num_okresy);
        pobudzenie = mean(reshaped,2);
    end
    res_idx = 1;
end

for  nr = 1:Nramek
    n = 1+(nr-1)*Mstep : Mlen + (nr-1)*Mstep;
    bx = x(n);
    bx = bx - mean(bx);
    for k = 0:Mlen-1
        r(k+1) = sum(bx(1:Mlen-k) .* bx(1+k:Mlen));
    end
    
    offset=20; rmax=max(r(offset:Mlen));
    imax=find(r==rmax);
    if (rmax > 0.35*r(1)) T=imax; else T=0; end
    if (T>80) T=round(T/2); end
    
    rr=(r(2:Np+1))';
    for m=1:Np
        R(m,:)=[r(m:-1:2) r(1:Np-(m-1))];
    end
    a=-inv(R)*rr;
    wzm=r(1)+r(2:Np+1)*a;
    
    lpc=[lpc; T; wzm; a;];
    
    % --- SYNTEZA ---
    if strcmp(tryb,'A')
        T = 0;
    elseif strcmp(tryb,'B')
        if T ~= 0, T = T * 2; end
    elseif strcmp(tryb,'C')
        if T ~= 0, T = 80; end
    elseif strcmp(tryb,'D')
        T = 0;
    elseif strcmp(tryb,'E1') || strcmp(tryb,'E2')
        % T jak wyliczone, ale pobudzenie zastąpione
    end
    
    if (T~=0) gdzie=gdzie-Mstep; end
    
    for ni=1:Mstep
        if strcmp(tryb,'D')
            if coldvox_idx > length(coldvox)
                coldvox_idx = 1;
            end
            pob = coldvox(coldvox_idx);
            coldvox_idx = coldvox_idx +1;
        elseif strcmp(tryb,'E1') || strcmp(tryb,'E2')
            pob = pobudzenie(res_idx);
            res_idx = mod(res_idx, length(pobudzenie)) +1;
        else
            if T==0
                pob=2*(rand(1,1)-0.5);
                gdzie=(3/2)*Mstep+1;
            else
                if (ni==gdzie)
                    pob=1; gdzie=gdzie+T;
                else
                    pob=0;
                end
            end
        end
        
        ss(ni)=wzm*pob-bs*a;
        bs=[ss(ni) bs(1:Np-1)];
    end
    
    s = [s ss];
end

s=filter(1,[1 -0.9735],s);

plot(s); title(['Zsyntezowana mowa, tryb: ' tryb]);
soundsc(s, fpr);
