# pyFSK
This code is part of the assignment given for the course Digital Communication.
We use a standard binary data as an input signal, (randomly generated 16bit array in code).

The dependencies required for the compilation in python3 are:
1. Numpy 
2. Scipy
3. Matplotlib

These can be installed using the command line / Terminal commands as :
```
pip install numpy
pip install scipy
pip install matplotlib
```
After installing the dependencies, you can download this repository and continue to execute FSK.py using python3.

## Explanation of FSK.py :
FSK.py is the core file for Frequency Shift Keying of a digital input datastream. It consists of namely 2 trivial functions`FSKgen(inpSig, fskFreq1, fskFreq2)` and `FSKdemod(FSKsig)`which are used to modulate a FSK waveform and demodulate a digital bitstream from the generated FSK respectively.  

The input arguments to the modulator are `inpSig` which is the 16bit input data to be modulated with 2 frequencies `fskFreq1`,`fskFreq2` that becomes the carrier frequencies for bits 1&0 respectively.
Since the output signal is a **continous time signal**, we sample the signals at a sampling rate for each symbol or bit, I have used a sampling rate of **100samples/bit**. Thus for a 16bit sequence we obtain total of 1600samples.

We use 100samples of a standard sinewave of frequency `fskFreq1` for bit1 and 100samples of standard sinewave of frequency `fskFreq2` for bit0.

After iterating for every bit in the 16bit sequence, we obtain the FSK signal which has Frequency `fskFreq1` if bit is 1 and `fskFreq2` if bit is zero.

**The output FSK is :**

![FSK](/FSK_screencaps/FSK_updated.png)


Upon doing Fourier transform of the FSK signal, we obtain 2 significant peaks at the 2 FSK frequencies used. 
