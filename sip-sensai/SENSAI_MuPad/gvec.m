function [g] = gvec(t,x,p) 

g1 = -(x(1)-4.0e1)*p(1)*x(2)^3*x(3)-(x(1)+8.7e1)*p(2)*x(4)^4-(x(1)+6.4387e1)*p(3)+2.0e1;
g2 = ((x(2)-1.0)*(1.0e-1*x(1)+5.0))/(exp(-x(1)*(1.0/1.0e1)-5.0)-1.0)+-4.0*exp(-x(1)*(1.0/1.8e1)-2.5e1/6.0)*x(2);
g3 = -7.0e-2*exp(-x(1)*(1.0/2.0e1)-1.5e1/4.0)*(x(3)-1.0)-x(3)/(exp(-x(1)*(1.0/1.0e1)-9.0/2.0)+1.0);
g4 = ((x(4)-1.0)*(1.0e-2*x(1)+6.5e-1))/(exp(-x(1)*(1.0/1.0e1)-1.3e1/2.0)-1.0)+-1.25e-1*exp(-x(1)*(1.0/8.0e1)-1.5e1/1.6e1)*x(4);

g(1) = g1;
g(2) = g2;
g(3) = g3;
g(4) = g4;

end