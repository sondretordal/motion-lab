function [lambda, w0, sigma] = LinearWaveSpec(S, w, plotResult)

    % Fomr objective funciton
    waveSpec = @(x) linearWaveSpec(x(1), x(2), x(3), w);
    objFun = @(x) (waveSpec(x) - S)'*(waveSpec(x) - S);

    % Solve optimization problem
    x0 = ones(3,1);
    x = fminsearch(objFun, x0);
    
    lambda = x(1);
    w0 = x(2);
    sigma = x(3);

    % Calculate resulting linearized wave spectrum
    Slin = waveSpec(x);
    
    if strcmp(plotResult, 'true')
        figure;
        plot(w/(2*pi), S, 'r'), hold on
        plot(w/(2*pi), Slin, 'b')
        pbaspect([16 9 1])
        legend('S(\omega)', '|h(j\omega)|^2')
        xlabel('Frequency - [Hz]')
        ylabel('Spectrum Density - [$m^2$/Hz]')
        xlim([min(w/(2*pi)), max(w/(2*pi))])
    end

end

function S = linearWaveSpec(lambda, w0, sigma, w)

    S = zeros(length(w),1);
    for i = 1:length(w)
        num = 4*(lambda*w0*sigma*w(i)^2); 
        den = (w0^2 - w(i)^2)^2 + 4*(lambda*w0*w(i))^2;
        
        
        S(i) = num/den;
    end

end