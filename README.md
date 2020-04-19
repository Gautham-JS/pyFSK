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

**The output FSK for sequence [1101100011001000] with `fskFreq1=2`, `fskFreq2=0.9` is :**

![FSK](/FSK_screencaps/FSK_updated.png)


**Upon doing Fourier transform of the FSK signal, we obtain frequency spectrum with 2 significant peaks at the 2 FSK frequencies used :**

![FFT of FSK](/FSK_screencaps/FSKfft.png)

**Passing the FSK signal to the function `FSKdemod()` gives the demodulated bit sequence by using a frequency detection technique(zero crossing) :**

![Demodulated output](/FSK_screencaps/FSKdemod.png)

## Explanation of FSK_compression.py :
This code uses the functions defined in FSK.py for modulation and demodulation and uses it for a practical application of FSK in digital Data Compression using concepts from FFT Image Compression techniques. 
The inspiration for this section comes from a brilliant explanation of FFT Image Compression by University of Washington : https://cosmolearning.org/video-lectures/fft-image-compression/

Similar to Image Compression, we use a 1 Dimentional bit stream instead of 2 Dimentional images. As the video above explains, if we create random numbers for each pixel of an image, we obtain white noise. That image will look like TV static and the FFT of such an image gives no significant peaks and thus cannot be compressed. Most natural images have an order in the pixels  while going sequentially and rarely have abrupt value changes. These images FFT gives few significant Peaks. Truncating all minor values and transmitting only the Peak Values is sufficient to reconstruct the image at the receiver using IFFT thus significantly saving bandwidth. An image is more compressible if the pixels are more ordered rather than random, a detailed picture of a rainforest is less compressible than a picture of the night sky.

In our case we are using a random 16bit sequence, this randomness and lack of order prevents the use of direct FFT compression of digital datastreams as there would be a lot of peaks. Horrible for compression. This is where FSK comes in.

FSK converts the Bit Sequence to 2 quantifiable frequencies , `fskFreq1` and `fskFreq2`, the frequency spectrum of FSK only contains 2 peaks making it highly compressible.compression contains the function `FFTcompression(fftsig,threshold)` This function takes 2 arguments FFT of FSK signal(Frequency spectrum) and threshold. It truncates all values below Threshold in amplitude to zero thus truncating all the minor peaks in the spectrum it returns this truncated Frequency Spectrum.

This truncated FFT spectrm if transmitted can save significant bandwidth in comparison to complete FSK sequence. 

When we compute IFFT of this truncated FFT Spectrum, we obtain a distorted version of the input FSK sequence. This distortion arises due to discontinuities in the FSK spectrum at the input generally when bit changes. 

This distorted FSK is distorted more in the amplitude and waveshape and the frequency domain is rather unaffected due to existence of major peaks in FFT spectrum.

Thus using a standard demodulation of FSK (Zero Crossing Detectior) gives the input waveform.


