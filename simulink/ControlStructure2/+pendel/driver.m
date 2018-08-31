function [pt, pt_t, pt_tt] = driver(eta, v, v_t, p, p_t, p_tt, Hbr)
    % Ship/stewart {b} orientation matrix relative to {n}
    Rnb = math3d.Rzyx(eta(4:6));

    % Body fixed velocity and acceleration skew matrices
    W = math3d.skew(v(4:6));
    W_t = math3d.skew(v_t(4:6));

    Rnb_t = Rnb*W;
    Rnb_tt = Rnb*W*W + Rnb*W_t;

    % Constant offsets {b} -> {r}
    r = Hbr(1:3,4);
    Rbr = Hbr(1:3,1:3);

    % Position of {t}/{n} given in {n}
    pt = eta(1:3) + Rnb*(r + Rbr*p);

    % Velocity of {t}/{n} given in {n}
    pt_t = v(1:3) + Rnb_t*(r + Rbr*p) + Rnb*(Rbr*p_t);

    % Acceleration of {t}/{n} given in {n}
    pt_tt = v_t(1:3) + Rnb_tt*(r + Rbr*p) + ...
        2*Rnb_t*(Rbr*p_t) + Rnb*(Rbr*p_tt);
end