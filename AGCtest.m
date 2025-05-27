A=[ones(400,1);ones(400,1)*0.2;ones(400,1);5*ones(400,1);ones(400,1)];
Xin=A.*exp(1i*(pi/20)*(1:2000)');
figure;
grid on;
subplot(3,1,1);
plot(real(Xin));
title('signal at receiver input')
grid on;
[Yo,g]=agc(Xin,0.05);
subplot(3,1,2);
plot(real(Yo));
title('Output of the AGC loop')
grid on;
subplot(3,1,3);
plot(g);
title('AGC loop gain');
grid on;
