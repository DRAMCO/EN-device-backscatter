## Firmware

The firmware **firmware-vscode-exp-4b-part-2** is used in [experiment 4b](https://github.com/techtile-by-dramco/experiments/tree/main/04_backscatter_communication) part 2.

The firmware [**firmware-vscode-exp-4b-part-2-pseudorandom**](https://github.com/techtile-by-dramco/EN-device-backscatter/tree/main/firmware-vscode-exp-4b-part-2-pseudorandom) transmits 10 bytes preamble + 4096 bytes pseudo random code (baudrate 1000 bps) with a delay of 5 seconds between each transmission cycle.
One cycle requires 8 [bits/byte] * 1 [ms/bit] * (10 + 4096) [bytes] or in total 32.848 seconds.

## GNU Radio

The folder `gnuradio` contains the RX and TX files. The `receiver` folder contains `OOK.grc` to demodulate the modulated backscatter signal. 
