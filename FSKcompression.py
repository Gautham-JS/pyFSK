'''
---> Author : Gautham J.S
---> 19-April-2020

The following code shows an application of the generic FSK algorithm(FSK.py) in the working directory. (Not for assignment, just a fun application to test)

Here we try to apply FSk to practically show the data compression using a bitstream. Getting inspiration from FFT data compression used for Image Compression Algorithms,
we apply a similar FFT compression on a 1 dimensional bitstream instead of 2 dimensional Image. 

As a premise, we convert a random distribution of bitstream generated to a frequency distribution in the time domain in FSK generation.

This time domain FSk signal only has 2 quantifiable Frequency Components to it, (fskFreq1 & fskFreq2)...converting it to frequency domain by Fast Fourier Transformation we get frequency domain

This freq domain has numerous minor peaks around the major peaks. The whole data can be transmitted using this Freq domain....for compression , we Truncate all the minor peaks

only Major peaks are transmitted by thresholding FFT peaks.....Inverse FFT of this truncated FFT gives a distorted version of actual FSK with lesser distortion in the frequency component 

Upon applying zero crossing detection to this we obtain the input data with occasional bit errors due to minor frequency distortion whose probablity is directly prop. to Truncation Threshold.
'''



from FSK import FSkgen, FSKdemod

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import style
style.use('ggplot')
from scipy.fftpack import fft,fftfreq, ifft



def FFTcompression(fftsig,threshold):
    compression_mask = np.logical_or(fftsig>threshold , fftsig<-threshold)
    fftcompr = compression_mask * fftsig
    return fftcompr

def MainFun():
    #generating random 16 bit input
    bitlen = 16
    inpSig = [random.randint(0,1) for x in range(0,bitlen)]
    print('\nthe input binary sequence is : {}\n'.format(inpSig))
    
    #compute FSK of input signal with fskFreq1 for bit1 as 2Hz, fskFreq2 for  bit2 as 0.9Hz...frequencies chosen for better visibility in plots
    timepd,mainsig,adjsig = FSkgen(inpSig,2,0.9)

    
    #compute Frequency domain of the FSK signal
    time = np.linspace(0, 16, 1600, endpoint=True)
    fftsig = fft(mainsig, time.size)
    freqarr = np.linspace(0.0, 1.0/(2.0*(16/1600)), time.size//2)

    #COMPRESSING FFT OF FSK SIGNAL BY TRUNCATING ALL AMPLITUDE UNDER 10 TO ZERO.
    fftcompr = FFTcompression(fftsig, 10)


    #Demodulate the FSK signal with the compressed FFT signal.
    det_Bits = FSKdemod(ifft(fftcompr))
    bitPlot = []

    #scale detected bits to the same length as timepd...100 samples/bit...1600 samples for plotting purposes
    for bit in det_Bits:
        for x in range(0,100):
            bitPlot.append(bit)
    
    #Bit Error Detection
    for b in range(0, len(det_Bits)):
        if det_Bits[b]-inpSig[b] == 0:
            pass
        else:
            print("\n\nBit Error detectiod in Decompression at index : {}\n\n".format(b))
    

    amp = (np.abs(fftcompr))
    fftplot = (2/amp.size)*amp[0:amp.size//2]

    fig, axs = plt.subplots(3)
    #axs[0].axis('equal')
    axs[0].plot(timepd ,mainsig, label='FSK Signal')
    axs[0].plot(timepd ,adjsig,label='Input Bits')
    axs[0].set_title('FSK Plot')
    axs[0].legend()
    axs[1].plot(freqarr, fftplot,label='Truncated FFT')
    axs[1].set_title('Compressed Freq Domain')
    
    axs[1].legend()
    axs[2].plot(timepd, bitPlot,label='Decompressed bits')
    axs[2].plot(timepd, ifft(fftcompr),label='IFFT of compressed data')
    axs[2].legend()
    axs[2].set_title('Demodulating IFFT of Truncated signal')
    plt.show()

if __name__ == "__main__":
    try:
        MainFun()
    except Exception as e:
        print("\nError Occured :: \n {}".format(e))