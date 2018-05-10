function f = f(in1,l_ref,Ts,omega,zeta,Kdc)
%F
%    F = F(IN1,L_REF,TS,OMEGA,ZETA,KDC)

%    This function was generated by the Symbolic Math Toolbox version 8.0.
%    09-May-2018 15:17:39

c1 = in1(34,:);
eta1 = in1(1,:);
eta2 = in1(2,:);
eta3 = in1(3,:);
eta4 = in1(4,:);
eta5 = in1(5,:);
eta6 = in1(6,:);
l = in1(28,:);
l_t = in1(29,:);
p1 = in1(19,:);
p2 = in1(20,:);
p3 = in1(21,:);
p_t1 = in1(22,:);
p_t2 = in1(23,:);
p_t3 = in1(24,:);
p_tt1 = in1(25,:);
p_tt2 = in1(26,:);
p_tt3 = in1(27,:);
phi1 = in1(30,:);
phi2 = in1(31,:);
phi_t1 = in1(32,:);
phi_t2 = in1(33,:);
v1 = in1(7,:);
v2 = in1(8,:);
v3 = in1(9,:);
v4 = in1(10,:);
v5 = in1(11,:);
v6 = in1(12,:);
v_t1 = in1(13,:);
v_t2 = in1(14,:);
v_t3 = in1(15,:);
v_t4 = in1(16,:);
v_t5 = in1(17,:);
v_t6 = in1(18,:);
t2 = cos(eta5);
t3 = 1.0./t2;
t4 = sin(eta5);
t5 = cos(eta4);
t6 = sin(eta4);
t7 = omega.^2;
t8 = cos(eta6);
t9 = sin(eta6);
t10 = t6.*t9;
t11 = t4.*t5.*t8;
t12 = t10+t11;
t13 = t5.*t9;
t15 = t4.*t6.*t8;
t14 = t13-t15;
t16 = t12.*v5;
t17 = t14.*v6;
t18 = t16+t17;
t19 = t14.*v4;
t20 = t2.*t8.*v5;
t21 = t19+t20;
t22 = t12.*v4;
t23 = t22-t2.*t8.*v6;
t24 = p1.*4.971672424300975e-1;
t25 = p3.*4.967117124448933e-3;
t75 = p2.*8.676405135780166e-1;
t26 = t24+t25-t75+1.082024099747949;
t27 = t5.*t8;
t28 = t4.*t6.*t9;
t29 = t27+t28;
t30 = t6.*t8;
t35 = t4.*t5.*t9;
t31 = t30-t35;
t32 = p_t2.*3.690033198352161e-3;
t33 = p_t3.*9.99986887020921e-1;
t71 = p_t1.*3.550977499600688e-3;
t34 = t32+t33-t71;
t36 = p_t1.*8.676474650532034e-1;
t37 = p_t2.*4.971783612075956e-1;
t38 = p_t3.*1.246408311757266e-3;
t39 = t36+t37+t38;
t40 = p_t1.*4.971672424300975e-1;
t41 = p_t3.*4.967117124448933e-3;
t69 = p_t2.*8.676405135780166e-1;
t42 = t40+t41-t69;
t43 = p_tt2.*3.690033198352161e-3;
t44 = p_tt3.*9.99986887020921e-1;
t82 = p_tt1.*3.550977499600688e-3;
t45 = t43+t44-t82;
t46 = p1.*8.676474650532034e-1;
t47 = p2.*4.971783612075956e-1;
t48 = p3.*1.246408311757266e-3;
t49 = t46+t47+t48+1.536041691521612;
t50 = t29.*v4;
t88 = t2.*t9.*v5;
t51 = t50-t88;
t52 = p_tt1.*8.676474650532034e-1;
t53 = p_tt2.*4.971783612075956e-1;
t54 = p_tt3.*1.246408311757266e-3;
t55 = t52+t53+t54;
t56 = p2.*3.690033198352161e-3;
t57 = p3.*9.99986887020921e-1;
t72 = p1.*3.550977499600688e-3;
t58 = t56+t57-t72+1.024461448780775;
t59 = t31.*v5;
t60 = t29.*v6;
t61 = t59+t60;
t62 = t31.*v4;
t63 = t2.*t9.*v6;
t64 = t62+t63;
t65 = p_tt1.*4.971672424300975e-1;
t66 = p_tt3.*4.967117124448933e-3;
t70 = p_tt2.*8.676405135780166e-1;
t67 = t65+t66-t70;
t68 = sin(phi1);
t73 = t2.*t5.*v5;
t123 = t2.*t6.*v6;
t74 = t73-t123;
t76 = t4.*v6;
t77 = t2.*t5.*v4;
t78 = t76+t77;
t79 = t4.*v5;
t80 = t2.*t6.*v4;
t81 = t79+t80;
t83 = cos(phi2);
t84 = cos(phi1);
t85 = 1.0./l;
t86 = t31.*v_t5;
t87 = t29.*v_t6;
t89 = t51.*v5;
t90 = t86+t87+t89-t64.*v6;
t91 = t26.*t90;
t92 = t29.*v4.*2.0;
t93 = t92-t2.*t9.*v5.*2.0;
t94 = t31.*v4.*2.0;
t95 = t2.*t9.*v6.*2.0;
t96 = t94+t95;
t97 = t39.*t96;
t98 = t31.*v5.*2.0;
t99 = t29.*v6.*2.0;
t100 = t98+t99;
t101 = t42.*t100;
t102 = t31.*v_t4;
t103 = t61.*v6;
t104 = t51.*v4;
t105 = t2.*t9.*v_t6;
t106 = t102+t103+t104+t105;
t107 = t49.*t106;
t108 = t61.*v5;
t109 = t64.*v4;
t110 = t2.*t9.*v_t5;
t111 = t108+t109+t110-t29.*v_t4;
t112 = t58.*t111;
t113 = t2.*t9.*t67;
t114 = t91+t97+t101+t107+t112+t113-v_t2-t31.*t45-t29.*t55-t34.*t93;
t115 = sin(phi2);
t116 = t4.*v6.*2.0;
t117 = t2.*t5.*v4.*2.0;
t118 = t116+t117;
t119 = t39.*t118;
t120 = t2.*t5.*v5.*2.0;
t121 = t120-t2.*t6.*v6.*2.0;
t122 = t42.*t121;
t124 = t74.*v6;
t125 = t4.*v_t6;
t126 = t2.*t5.*v_t4;
t127 = t124+t125+t126-t81.*v4;
t128 = t49.*t127;
t129 = t4.*t67;
t130 = t4.*v5.*2.0;
t131 = t2.*t6.*v4.*2.0;
t132 = t130+t131;
t133 = t34.*t132;
t134 = t74.*v5;
t135 = t78.*v4;
t136 = t4.*v_t5;
t137 = t2.*t6.*v_t4;
t138 = t134+t135+t136+t137;
t139 = t58.*t138;
t140 = t78.*v6;
t141 = t81.*v5;
t142 = t2.*t6.*v_t6;
t143 = t140+t141+t142-t2.*t5.*v_t5;
t144 = t2.*t6.*t55;
t145 = t119+t122+t128+t129+t133+t139+t144+v_t3-t26.*t143-t2.*t5.*t45;
f = [eta1+Ts.*v1;eta2+Ts.*v2;eta3+Ts.*v3;eta4+Ts.*(v4+t3.*t4.*t5.*v6+t3.*t4.*t6.*v5);eta5+Ts.*(t5.*v5-t6.*v6);t3.*(eta6.*t2+Ts.*t5.*v6+Ts.*t6.*v5);v1+Ts.*v_t1;v2+Ts.*v_t2;v3+Ts.*v_t3;v4+Ts.*v_t4;v5+Ts.*v_t5;v6+Ts.*v_t6;v_t1;v_t2;v_t3;v_t4;v_t5;v_t6;p1+Ts.*p_t1;p2+Ts.*p_t2;p3+Ts.*p_t3;p_t1+Ts.*p_tt1;p_t2+Ts.*p_tt2;p_t3+Ts.*p_tt3;p_tt1;p_tt2;p_tt3;l+Ts.*l_t;l_t-Ts.*(l.*t7-Kdc.*l_ref.*t7+l_t.*omega.*zeta.*2.0);phi1+Ts.*phi_t1;phi2+Ts.*phi_t2;phi_t1-Ts.*t85.*(-t84.*(v_t1-t34.*(t14.*v4.*2.0+t2.*t8.*v5.*2.0)+t39.*(t12.*v4.*2.0-t2.*t8.*v6.*2.0)-t12.*t45-t14.*t55+t26.*(t21.*v5-t23.*v6+t12.*v_t5+t14.*v_t6)+t42.*(t12.*v5.*2.0+t14.*v6.*2.0)+t49.*(t18.*v6+t21.*v4+t12.*v_t4-t2.*t8.*v_t6)+t58.*(t18.*v5+t23.*v4-t14.*v_t4-t2.*t8.*v_t5)-t2.*t8.*t67)+l_t.*phi_t1.*2.0+c1.*t68.*t83-t68.*t83.*t145+t68.*t114.*t115+l.*phi_t2.^2.*t68.*t84);phi_t2+(Ts.*t85.*(-c1.*t115+t83.*t114+t115.*t145-l_t.*phi_t2.*t84.*2.0+l.*phi_t1.*phi_t2.*t68.*2.0))./t84;c1];
