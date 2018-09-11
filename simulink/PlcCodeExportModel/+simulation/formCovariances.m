function sim = formCovariances(data, compare)

    % Convert stewarts
    em8000 = convertStewart(data.feedback.em8000);
    em1500 = convertStewart(data.feedback.em1500);

    mru1 = data.feedback.mru1;
    mru2 = data.feedback.mru2;

    t = data.feedback.t - data.feedback.t(1);

    % Mru covariances
    mru1 = removeAngleBias(mru1, em8000);
    mru2 = removeAngleBias(mru2, em1500);
    
    sim.mru1.e_phi = mru1.e_phi;
    sim.mru1.e_theta = mru1.e_theta;
    
    sim.mru2.e_phi = mru2.e_phi;
    sim.mru2.e_theta = mru2.e_theta;
    
    sim.mru1.var = formMruCovarince(mru1, em8000);
    sim.mru2.var = formMruCovarince(mru2, em1500);

    if ~strcmp(compare, 'none')
        compareData(t, mru1, em8000, compare, 'EM8000');
        compareData(t, mru2, em1500, compare, 'EM1500');
    end

end

function mru = removeAngleBias(mru, stewart)
    mru.e_phi = mean(mru.phi - stewart.phi);
    mru.e_theta = mean(mru.theta - stewart.theta);
    
    mru.phi = mru.phi - mru.e_phi;
    mru.theta = mru.theta - mru.e_theta;
end

function compareData(t, mru, stewart, type, name)
    figure('Name', name);
    if strcmp(type, 'pos')
        subplot(3,2,1)
        plot(t, stewart.surge, 'b'), hold on
        plot(t, mru.surge, 'k--')
        
        subplot(3,2,3)
        plot(t, stewart.sway, 'b'), hold on
        plot(t, mru.sway, 'k--')
        
        subplot(3,2,5)
        plot(t, stewart.heave, 'b'), hold on
        plot(t, mru.heave, 'k--')
        
        subplot(3,2,2)
        plot(t, stewart.phi/pi*180, 'b'), hold on
        plot(t, mru.phi/pi*180, 'k--')
        
        subplot(3,2,4)
        plot(t, stewart.theta/pi*180, 'b'), hold on
        plot(t, mru.theta/pi*180, 'k--')
        
        subplot(3,2,6)
        plot(t, stewart.psi/pi*180, 'b'), hold on
        plot(t, mru.psi/pi*180, 'k--')
    end
    
    if strcmp(type, 'vel')
        subplot(3,2,1)
        plot(t, stewart.surge_t, 'b'), hold on
        plot(t, mru.surge_t, 'k--')
        
        subplot(3,2,3)
        plot(t, stewart.sway_t, 'b'), hold on
        plot(t, mru.sway_t, 'k--')
        
        subplot(3,2,5)
        plot(t, stewart.heave_t, 'b'), hold on
        plot(t, mru.heave_t, 'k--')
        
        subplot(3,2,2)
        plot(t, stewart.wx, 'b'), hold on
        plot(t, mru.wx, 'k--')
        
        subplot(3,2,4)
        plot(t, stewart.wy, 'b'), hold on
        plot(t, mru.wy, 'k--')
        
        subplot(3,2,6)
        plot(t, stewart.wz, 'b'), hold on
        plot(t, mru.wz, 'k--')
    end
end

function variance = formMruCovarince(mru, stewart)
    variance.eta = [
        (cov(mru.surge - stewart.surge))
        (cov(mru.sway - stewart.sway))
        (cov(mru.heave - stewart.heave))
        (cov(mru.phi - stewart.phi))
        (cov(mru.theta - stewart.theta))
        (cov(mru.psi - stewart.psi))
    ];

    variance.v = [
        (cov(mru.surge_t - stewart.surge_t))
        (cov(mru.sway_t - stewart.sway_t))
        (cov(mru.heave_t - stewart.heave_t))
        (cov(mru.wx - stewart.wx))
        (cov(mru.wy - stewart.wy))
        (cov(mru.wz - stewart.wz))
    ];

    variance.v_t = [
        (cov(mru.surge_tt - stewart.surge_tt))
        (cov(mru.sway_tt - stewart.sway_tt))
        (cov(mru.heave_tt - stewart.heave_tt))
        0.001^2
        0.001^2
        0.001^2
    ];
end

function stewart = convertStewart(stewart)

    for i = 1:length(stewart.surge)
        eta = [
            stewart.surge(i)
            stewart.sway(i)
            stewart.heave(i)
            stewart.phi(i)
            stewart.theta(i)
            stewart.psi(i)
        ];

        eta_t = [
            stewart.surge_t(i)
            stewart.sway_t(i)
            stewart.heave_t(i)
            stewart.phi_t(i)
            stewart.theta_t(i)
            stewart.psi_t(i)
        ];

        eta_tt = [
            stewart.surge_tt(i)
            stewart.sway_tt(i)
            stewart.heave_tt(i)
            stewart.phi_tt(i)
            stewart.theta_tt(i)
            stewart.psi_tt(i)
        ];

        % Get body velocities and accelearytions
        [v, v_t] = math3d.eulerToBody(eta, eta_t, eta_tt, 'xyz');

        stewart.phi(i,1) = eta(4);
        stewart.theta(i,1) = eta(5);
        stewart.psi(i,1) = eta(6);

        stewart.wx(i,1) = v(4);
        stewart.wy(i,1) = v(5);
        stewart.wz(i,1) = v(6);

        stewart.wx_t(i,1) = v_t(4);
        stewart.wy_t(i,1) = v_t(5);
        stewart.wz_t(i,1) = v_t(6);

    end


end