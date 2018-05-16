function x_t = shipOde(x) 
    x_t = [
        s2s.shipJacobian(x(1:6))*x(7:12)
        x(13:18)
        zeros(6,1)
    ];
end