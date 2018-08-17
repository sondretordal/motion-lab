function H = Hrz(psi)

H = [cos(psi),-sin(psi), 0, 0;
     sin(psi), cos(psi), 0, 0;
     0       , 0       , 1, 0;
     0       , 0       , 0, 1];
 
end