'''
---> Author : Gautham J.S
---> 18-April-2020
---> FSK Modulation and demodulation - Assignment 4, Digital Communiction

Hello Sir, The Following code shows FSK modulation and demodulation process with an arbitary 16 bit digital Input and 2 more inputs : frequency correesponding to bit 1 and another for bit 0
The Stepwise explanation is given before significant lines in code.

This code is not plagerized and was written purely logically by Myself with the best of my knowledge.
'''

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import style
style.use('ggplot')
from scipy.fftpack import fft,fftfreq, ifft



def FSkgen(inpSig, fskFreq1, fskFreq2):
    #create a time domain from 0 to length of input(bit length) in intervals of 0.01....thus total of 100 samples per bit...hence 1600 samples for 16 bit data.
    timepd = np.arange(0 ,len(inpSig) ,0.01)

    #init arrays mainsig to store output FSK and adjsig array which stores same data as input signal but sampled at 100 samples/bit to plot with timepd
    #lval is just a constant used to iteratively jump 100 samples to next bit at every next iteration, thus looping 16 times for 16 bits.
    mainsig = []
    lval = 0
    adjsig = []


    for i in range(0 ,len(inpSig)):
        #this loop iterates 16 times for each bit
        for j in range(lval,lval+100):
            #this loop iterates 100 times for each bit (once for each sample)
            if inpSig[i]==1:
                #append sinewave with frequency fskFreq1 for bit 1 --- 100 samples 
                mainsig.append( np.sin(2*np.pi*fskFreq1*timepd[j]) )
            else:
                #append sinewave with frequence fskFreq2 for bit 0 --- 100 samples
                mainsig.append( np.sin(2*np.pi*fskFreq2*timepd[j]) )
            adjsig.append(inpSig[i])
            lval+=1
    return timepd,mainsig,adjsig




def FSKdemod(FSKsig):
    sample_duration = len(FSKsig)/16
    i = 0
    #initializing crosscount array to count the number of zero crossings per bit duration(100 samples) and bitstream array to store output demodulated 16 bits
    cross_count = []
    bitstream =[]

    while i<len(FSKsig):
        zero_cross = []

        #reference frame is a frame of continous sampled FSK data representing one bit of 16 bit representation---frames of 100 samples each 
        ref_frame = FSKsig[int(i):int(i+sample_duration)]

        #iterating through the frame , note that we exclude last and first indices...i'll get back to that
        for x in range(1, len(ref_frame)-1 ):
            
            #checking prev and next element to detect zero crossing... this is where the excluded last and first indices are taken in, iteratively going thru [i-1] & [i+1] each step
            if np.logical_and(ref_frame[x-1]<0 , ref_frame[x+1]>0) or np.logical_and(ref_frame[x-1]>0, ref_frame[x+1]<0):
                zero_cross.append(round(ref_frame[x],2))
            else:
                pass
        cross_count.append(len(zero_cross))
        i+=sample_duration
    
    #through trial and error its estimated that there will be more than 5 zero crossings for bit 1, Thersholding crosscount and setting bit values of bitstream accordingly
    #The threshold can be determined more accurately using statistical methods but i decided to omit this step and hardcode instead
    for k in range(0, len(cross_count)):
        if cross_count[k]<5:
            bitstream.append(0)
        else:
            bitstream.append(1)
    
    return bitstream


def main():    

    #generating random 16 bit input
    bitlen = 16
    inpSig = [random.randint(0,1) for x in range(0,bitlen)]
    print('\nthe input binary sequence is : {}\n'.format(inpSig))
    
    #compute FSK of input signal with fskFreq1 for bit1 as 2Hz, fskFreq2 for  bit2 as 0.9Hz...frequencies chosen for better visibility in plots
    timepd,mainsig,adjsig = FSkgen(inpSig,2,0.9)

    time = np.linspace(0, 16, 1600, endpoint=True)
    #compute Frequency domain of the FSK signal
    fftsig = fft(mainsig, time.size)
    fft_dB = 20*np.log(fftsig)
    time_step = 1/len(fftsig)
    freqarr = np.linspace(0.0, 1.0/(2.0*(16/1600)), time.size//2)

    #Demodulate the FSK signal
    det_Bits = FSKdemod(mainsig)
    bitPlot = []

    #scale detected bits to the same length as timepd...100 samples/bit...1600 samples
    for bit in det_Bits:
        for x in range(0,100):
            bitPlot.append(bit)


    

    amp = np.abs(fftsig)
    fftplot = (2/amp.size)*amp[0:amp.size//2]
    #Plotting the signals
    fig, axs = plt.subplots(3)

    axs[0].plot(timepd ,mainsig,label='FSK')
    axs[0].plot(timepd ,adjsig,label='Binary Input')
    axs[0].set_title('FSK Plot')
    axs[1].plot(freqarr, fftplot,label='Frequency spectrum of FSK')
    axs[1].set_title('FFT of FSK Signal')
    ind = np.argpartition(fftplot,-2)[-2:]
    style = dict(size=10, color='gray')
    for i in list(ind):
        axs[1].text(freqarr[i],fftplot[i],'Freq :: {}'.format(freqarr[i]),**style)
    
    axs[2].plot(timepd, bitPlot,label='Demodulated Binary Signal')
    axs[2].set_title('Demodulated Signal')
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    plt.show()

if __name__ == "__main__":
    main()