# Demodulation and Bit Error Rate Testing

## Demodulation process
On-off keying demodulation will be performed by applying a **Xlating FIR filtering** with a 20kHz low-pass filter at the LO frequency. The received complex signal is turned via a **complex to mag^2** block into the power at each spectral point. In the time domain, this is represented by a noisy square wave with a low amplitude (power). To create binary data out of these positive values, a hysteresis based threshold is set to this signal, setting the output to a 1 or a 0 (float). Next clock recovery, and downsampling (decimation) by means of a symbol sync are performed (see below for more info on this). As a final step, efficient data storage is obtained by converting the floats to characters, packing these bytes by selecting the least significant bit of 8 bytes (characters) in a single byte and saving this in a file sink. 

***TO CHECK: adding a Automatic Gain Control (AGC) to prevent necessary changes to the threshold*** 

### Clock recovery and downsampling.

In the backscatter system, there are two main sample/data rates. The first one is the sample rate of the USRP, and heavily depends on the bandwidth needed to receive the frequency shifted OOK signal (determined by the LO). The second one is the data rate of the binary backscatter signal. To perform bit error rate testing, these two rates should be matched in an efficient way. A major problem in downsampling is selecting the correct value for the sample/sample at exactly the right moment in time (often in the middle of the sample). As illustrated in the sketch below, trigger/time based sampling can lead to misfires and erroneous outputs when bit switches occur (e.g. for a noisy signal entering a wrongly set threshold).

Luckily for us there are existing techniques that allow for clock recovery based on the samples per symbol (or both data rates). As aforementioned, this clock recovery is a critical final step in the demodulation process. It synchronizes the output to the symbols in a digital signal, extracting them and reducing them to their individual representations, such as a bit. In Gnuradio, clock recovery is embedded in the **Symbol Sync** block, which performs four main steps:

 1. Estimates and tracks symbol rate (i.e. number of samples per symbol), given an initial estimate of samples per symbol and an allowable deviation from that estimate.
 2. Performs the timing synchronization needed so that the signal is sampled at exactly the right moment in time, which is when each symbol/pulse is at its maximum value.
 3. Decimate the signal so that what comes out of the block is 1 sample per symbol (or multiple if the user would like, but it's usually set to 1 or sometimes 2).
 4. Filter the signal appropriately.

Visually, we want to sample (red) at the maximum (blue), decreasing the estimated symbol clock error.
![Symbol synchronisation](https://wiki.gnuradio.org/images/a/a7/Symbol_sync_1.png)
### Phase Locked Loop (PLL) for Symbol Timing Recovery


A general Phase Locked Loop (PLL) for Symbol Timing Recovery, as used in the symbol sync block, looks like the figure below. The notations for the main parameters are the following:

-   Sample time (inverse of sample rate): $T_S$
-   Matched filter output: $z(n\,T_S)$ where $n$ is an integer
-   Symbol time (inverse of symbol rate): $T_M$
-   Samples per symbol rate: $L$
-   Timing error: $ϵ_Δ$
-   Timing error estimate at Rx: $\hatϵ_Δ$
-   Matched filter output at 1 sample/symbol: $z(m\,T_M+\hatϵΔ)$ where $m$ is an integer
-   Square-root Raised Cosine pulse shape: $p(n\,T_S)$

![SyncPhasedLoop](https://wirelesspi.com/wp-content/uploads/2020/11/figure-timing-sync-phase-locked-loop-pll.png)

At the receiver, the arriving signal $r(t)$ is sampled by a free running clock at a constant rate $1/T_S$ that is asynchronous to the symbol rate $1/T_M$ as shown in the figure above. These samples $r(n\,T_S)$ are matched filtered to produce $z(n\,T_S)$ at $L$ samples/symbol, none of which lies at the symbol boundary, i.e., an integer multiple of $T_M$. Here, the job of the timing synchronization loop is twofold.

1.  Figure out an estimate of the timing offset $\hatϵ_Δ$(or an error signal $e_D[m]$   proportional to it).
2. Then, rather than shifting a physical clock (such as a voltage controlled clock that exhibits excessive phase noise and delay), construct the 'missing samples' at optimal locations $z(m\,T_M+\hatϵ_Δ)$ by an algorithm operating on asynchronous samples $z(n\,T_S)$. This process is called interpolation. 

#### Timing Error Detector (TED)
A timing error detector solves the fundamental problem of synchronization. It generates an error signal $e_D[m]$ during each symbol interval using the matched filter outputs $z(n\,T_S)$ proportional to the timing phase difference $ϵ_Δ$ between the actual and desired sampling instants. The PLL functions properly as long as the mean error has the same sign as the actual error. Most of the timing error detectors operate at 1 or 2 samples/symbol. Some of the examples are [early-late](https://wirelesspi.com/early-late-bit-synchronizer-in-digital-communication/), [zero-crossing](https://wirelesspi.com/gardner-timing-error-detector-a-non-data-aided-version-of-zero-crossing-timing-error-detectors/) and [Mueller and Muller](https://wirelesspi.com/mueller-and-muller-timing-synchronization-algorithm/) timing error detectors.

An important concept in the working of a TED is the eye diagram. Due to its symbol-periodic overlaps, it is an excellent summary of signal behavior in time domain, very similar to a spectrum in frequency domain (they both utilize all the available information). 

Let us define for a pulse shaped and matched filtered Pulse Amplitde Modulated sequence at instants $m\,T_M$:  
-   $z(m\,T_M+ \hatϵ_Δ)$→Matched filtered output at $m\,T_M+\hatϵ_Δ$
-  $\dot z(mT_M+\hatϵΔ)$→Derivative of the matched filter output (i.e., its slope) at  $m\,T_M+\hatϵ_Δ$

The derivative at a point is defined as the slope of the line tangent to the curve at that point. To understand the intuition behind this mechanism, the figure below illustrates from an eye diagram perspective how a valid timing error signal is generated.
Four situations can be considered:

 1. T1: $\hatϵ_Δ < ϵ_Δ$ and $z(m\,T_M+ \hatϵ_Δ) < 0$
 2. T2: $\hatϵ_Δ > ϵ_Δ$ and $z(m\,T_M+ \hatϵ_Δ) > 0$
 3. T3: $\hatϵ_Δ > ϵ_Δ$ and $z(m\,T_M+ \hatϵ_Δ) < 0$
 4. T4: $\hatϵ_Δ < ϵ_Δ$ and $z(m\,T_M+ \hatϵ_Δ) > 0$ 

We conclude that the goal of a timing error detector is to push the sampling instant closer to the center where the eye is maximally open. A timing error detector can thus be formed as: 
$e_D[m] =z(m\,T_M+\hatϵ_Δ)⋅\dot z(m\,T_M+\hatϵ_Δ)$. 

Where the matched filtered output (positive or negative) is multiplied with its derivative (the slope at the sample) to indicate if the error detector should push (positive) or pull (negative) the sampling instant closer to the center of the eye. This is known as a **derivative** or **maximum likelihood Timing Error Detector**.

Naturally, this output is more fine-grained and hence accurate when the number of samples/symbol $L$ is large. Here, $L$ must be several times larger than the minimum limit set by the Nyquist theorem.


![Eye diagram](https://wirelesspi.com/wp-content/uploads/2020/11/figure-timing-sync-timing-matched-filter-intuition.png)
#### Early-Late Bit Synchronizer
In most applications, reducing the complexity of the timing locked loop is far more desirable than achieving the gains from the increased granularity. Instead of having a vastly oversampled Rx signal, a simpler form of a timing error detector is therefore attractive for system design operating at no more than 1 or 2 samples/symbol. Due to this reason, there are many approximations to the maximum likelihood timing error detector that have been derived over the years. Some of those new TEDs were invented in an ad-hoc fashion that turned out to be just another of its approximations. Early-late timing synchronizer is built on one such approximation.

Assume that the Rx signal is sampled at $L$=2 samples/symbol. In this case, the matched filter output, denoted by $z(n\,T_S)$, has every other sample that is a candidate of the symbol decision, i.e., $m=2n$. To keep the indexing in terms of symbols rather than samples, a better notation is to use $m\,T_M$ for the main sample as before and use $±T_M/2$ for the intermediate sample. 

$⋯\; ,\; z((m−1)\,T_M+\hatε_Δ) \; ,\; z(m\,T_M−\frac{T_M}{2}+\hatε_Δ) \; ,\; z(m\,T_M+\hatε_Δ) \; ,\; z(m\,T_M+\frac{T_M}{2}+\hatε_Δ) \; ,\; z((m+1)\,T_M+\hatε_Δ),⋯$

With alternaly a candidate for symbol decision and an intermediate sample. A popular approximation to compute the [derivative of a waveform](https://wirelesspi.com/design-of-a-discrete-time-differentiator/) at a time n is the first central difference filter  
$h[n]=\{+1,0,−1\}$
A reduced complexity solution is to just apply this filter to the matched filter output for finding its approximate slope. For this purpose, concentrate on the matched filter output $z(m\,T_M)$ and the two samples around it, that is to say

$\; z(m\,T_M−\frac{T_M}{2}+\hatε_Δ) \; ,\; z(m\,T_M+\hatε_Δ) \; ,\; z(m\,T_M+\frac{T_M}{2}+\hatε_Δ)$

These samples are drawn in the figure below, where the slope is being computed at time $m\,T_M$. In this scenario,
-   the symbol candidate $z(m\,T_M+\hatε_Δ) $ corresponds to the symbol $a[m]$ (sometimes referred to as ‘prompt’),
-   $z(m\,T_M−\frac{T_M}{2}+\hatε_Δ)$ is an early sample, and
-   $z(m\,T_M+\frac{T_M}{2}+\hatε_Δ)$ is a late sample.


![Early-Late sampling](https://wirelesspi.com/wp-content/uploads/2021/12/figure-timing-sync-early-late-convolution.png)
These early and late samples can be employed for computing the derivative because they overlap with the coefficients −1 and +1 of $h[−n]$ during the convolution process, as shown in the figure above (remember one of the signals, $h[n]$ here, is reversed during convolution). 
Thus, a non-data-aided Early-Late Timing Error Detector (TED) can be constructed by replacing the derivative term   $\dot z(m\,T_M+\hatε_Δ)$ in the maximum likelihood TED as:  

$eD[m]=z(m\,T_M+\hatε_Δ) \left( z(m\,T_M+\frac{T_M}{2}+\hatε_Δ) –z(m\,T_M−\frac{T_M}{2}+\hatε_Δ)\right)$

