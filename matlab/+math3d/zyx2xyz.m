function xyz = zyx2xyz(zyx)

    % Maple optimized code
    t1 = sin(zyx(1));
    t2 = cos(zyx(3));
    t3 = cos(zyx(1));
    t4 = sin(zyx(2));
    t5 = sin(zyx(3));
    t6 = t3 * t5;
    t7 = t1 * t2;
    t8 = cos(zyx(2));
    
    xyz = zeros(3,1);
    xyz(1,1) = atan2((-t6 * t4 + t7),(t3 * t8));
    xyz(2,1) = asin(t3 * t4 * t2 + t1 * t5);
    xyz(3,1) = atan2((-t7 * t4 + t6),( t2 * t8));

end