import time
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from build import MotionLab
import json

def wavespectrum(Hs=8.0, T1=12.0, spec='JONSWAP', plot=False):
    # Inital frequency range
    N = 100
    w_min = 0.01
    w_max = np.pi/2
    
    w = np.linspace(w_min, w_max, N)
    S = np.zeros(N)            
    # Calculate wavespectrum
    if spec == 'PMS':
        for k in range(0, N):
            # From average wave period to zero crossing period
            Tz = 0.921*T1
            
            # PM constants
            A = 4*np.pi**3*Hs**2/(Tz**4)
            B = 16*np.pi**3/(Tz**4)
            
            # Calculate wave spectrum 
            S[k] = A/(w[k]**5)*np.exp(-B/(w[k]**4))
            
    elif spec == 'JONSWAP':
        for k in range(0, N):
            if w[k] <= 5.24/T1:
                sigma = 0.07
            else:
                sigma = 0.09
                
            Y = np.exp(-((0.191*w[k]*T1-1)/(np.sqrt(2)*sigma))**2)
            
            # Calculate wave spectrum
            S[k] = 155*Hs**2/(T1**4*w[k]**5)*np.exp(-944/(T1**4*w[k]**4))*3.3**Y
    
    # Update frequency range
    w0 = w[np.argmax(S)]

        
    # Approximate linear wave spectrum
    def linear_spectrum(w, p, w0, sigma):
        S = np.zeros(len(w))
        for k in range(0, len(w)):
            S[k] = 4*(p*w0*sigma*w[k])**2/((w0**2-w[k]**2)**2+4*(p*w0*w[k])**2)
            
        return S
    
    sigma = np.sqrt(max(S))
    
    # Find linearized curve parameters
    func = lambda w, p: linear_spectrum(w, p, w0, sigma)
    popt, pcov = curve_fit(func, w, S)
    
    # Ensure popt is positive
    Lambda = abs(popt[0])
    
    # Calculate linear approximated spectrum
    Slin = linear_spectrum(w, Lambda, w0, sigma)
    
    # Plot computes wave spectrum
    if plot:
        plt.figure()
        plt.title(spec)
        plt.plot(w, S, 'b', label='Wave Spectrum')
        plt.plot(w, Slin, 'k--', label='Linear Spectrum')
        plt.xlabel('Wave period - [rad/s]')
        plt.ylabel('Spectrum Energy')
        plt.legend(loc=1)
        plt.grid()
        plt.show()

    # Save linearized wave spectrum parameters
    return w0, Lambda, sigma

s = MotionLab.ShipSimulator(0)


t = []

x = []
y = []
z = []
roll = []
pitch = []
yaw = []

w0, Lambda, sigma = wavespectrum(Hs=8.0, T1=12.0)

print 'w0 = ', w0
print 'Lambda = ', Lambda
print 'sigma = ', sigma

s.w0 = w0
s.Lambda = Lambda
s.sigma = sigma

while s.t <= 10*60.0:
    s.integrate()
    
    t.append(s.t)
    x.append(s.x)
    y.append(s.y)
    z.append(s.z)
    roll.append(s.roll)
    pitch.append(s.pitch)
    yaw.append(s.yaw)


print 'Hs = ', 4*np.std(z)

plt.figure()
plt.subplot(211)
plt.plot(t, x, 'r', label='Surge')
plt.plot(t, y, 'g', label='Sway')
plt.plot(t, z, 'b', label='Heave')
plt.grid()
plt.ylabel('Position - [m]')
plt.legend(loc=1)

plt.subplot(212)
plt.plot(t, np.array(roll)/np.pi*180, 'r', label='Roll')
plt.plot(t, np.array(pitch)/np.pi*180, 'g', label='Pitch')
plt.plot(t, np.array(yaw)/np.pi*180, 'b', label='Yaw')
plt.xlabel('Time - [s]')
plt.ylabel('Angle - [deg]')
plt.grid()
plt.legend(loc=1)

plt.show()







