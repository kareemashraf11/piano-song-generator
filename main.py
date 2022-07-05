import math
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

𝑡 = np.linspace(0,3,12*1024)                  # set the playing time of the song from 0 to 3 seconds with 12*1024 samples
fLeft = [196,130.81,164.81,220,246.93,146.83]   # list containing left hand frequencies
fRight = [392,261.63,329.63,440,493.88,293.66]   # list containing right hand frequencies
ti = [0,0.4,1.1,1.5,2.2,3]                  # list containing starting time for each frquency
Ti = [0.3,0.6,0.2,0.5,0.8,0.7]               # list containing duration of each frequency
x = 0                                       # initialize x 

n = len(fLeft)      # length of the list containing the frequencies

for i in range(n):
    x+= (np.sin(2*np.pi*fLeft[i]*t) + np.sin(2*np.pi*fRight[i]*t)) * (np.where(np.logical_and(t>=ti[i],t<ti[i]+Ti[i]),1,0))
# for loop to iterate over the lists and generate the song without noise

plt.subplot(3,2,1)
plt.plot(t,x)         # plot the song x without noise composed of multiple signals on the axis t
plt.title("Time domain without noise")
sd.play(x, 3*1024)    # play the song without noise


𝑁= 3*1024            # set number of samples to duration * 1024
freq = np.linspace(0,512,int(𝑁/2))   # set frequency axis range from 0 to 512 with N/2 samples

x_f = fft(x)          # convert the time signal x(t) without noise to frequency signal x(f)
y = 2/N * np.abs(x_f[0:np.int(N/2)])

plt.subplot(3,2,2)
plt.plot(freq, y)    # plot the frequency signal x(f) without noise
plt.title("Frequency domain without noise")


# get the maximum value in the frequency signal x(f) and round it to the next integer
max = 0
for i in range (1536):
    if y[i] > max:
        max = y[i]
max = math.ceil(max)

fn1 = np.random.randint(0,512)      # get two random frequencies to generate noise signal
fn2 = np.random.randint(0,512)
noise = (np.sin(2*np.pi*fn1*t) + np.sin(2*np.pi*fn2*t)) * (np.where(np.logical_and(t>=0,t<3),1,0))
                            # generate noise signal
                            
xn = x + noise      # add the noise signal to the original signal to produce the signal xn(t)
plt.subplot(3,2,3)
plt.plot(t,xn)     # plot the signal xn(t) with noise
plt.title("Time domain with noise")
#sd.play(xn,3*1024)  # play the song with noise

xn_f = fft(xn)      # convert the time signal xn(t) with noise to frequency signal xn(f)
y2 = 2/N * np.abs(xn_f[0:np.int(N/2)])

plt.subplot(3,2,4)
plt.plot(freq, y2)   # plot the frequency signal xn(f) with noise
plt.title("Frequency domain with noise")


    # get the maximum two random values in xn(f) greater than the max peak in the signal x(f)
index1 = 0
index2 = 0
for i in range(1536):
    if y2[i]>max:
        if index1 == 0:
            index1 = i
        else:
            index2 = i


        # generate xfiltered(t) signal by subtracting the two noise tones 
x_filtered = xn - (np.sin(2*np.pi*(index1/3)*t) + np.sin(2*np.pi*(index2/3)*t))
plt.subplot(3,2,5)
plt.plot(t,x_filtered)         # plot the filtered signal
plt.title("Time domain after\n noise cancellation")

sd.play(x_filtered, 3*1024)    # play the filtered song


x_filtered_f= fft(x_filtered)      # convert the time signal xn(t) with noise to frequency signal xn(f)
y3= 2/N * np.abs(x_filtered_f[0:np.int(N/2)])
plt.subplot(3,2,6)
plt.plot(freq, y3)   # plot the frequency signal x_filtered(f) after noise cancellation
plt.title("Frequency domain after\n noise cancellation")


plt.tight_layout()
