
import zmq
import array
from queue import Queue
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy as numpy
import scipy.signal
import sys

tau = numpy.pi * 2
max_samples = 1000000
minpktlen = 15 * 8   # Minimum number of bits in a packet
minsamples = 10000   # Minumum number of samples expected
invalid_packets = 0
packet_count = 0
debug = False
graph = False


SYNC_WORD = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1]
SYNC_WORD_LEN = len(SYNC_WORD)
PACKAGE_LEN = 6*8

# Whole packet clock recovery adapted from Michael Ossman's wcpr.py
# To learn more, see the following:
# https://www.youtube.com/watch?v=rQkBDMeODHc
# https://github.com/mossmann/clock-recovery/blob/master/wpcr.py

# determine the clock frequency
# input: magnitude spectrum of clock signal (numpy array)
# output: FFT bin number of clock frequency
def find_clock_frequency(spectrum):
    maxima = scipy.signal.argrelextrema(spectrum, numpy.greater_equal)[0]
    while maxima[0] < 2:
        maxima = maxima[1:]
    if maxima.any():
        threshold = max(spectrum[2:-1])*0.8
        indices_above_threshold = numpy.argwhere(spectrum[maxima] > threshold)
        return maxima[indices_above_threshold[0]]
    else:
        return 0

def midpoint(a):
    mean_a = numpy.mean(a)
    mean_a_greater = numpy.ma.masked_greater(a, mean_a)
    high = numpy.ma.median(mean_a_greater)
    mean_a_less_or_equal = numpy.ma.masked_array(a, ~mean_a_greater.mask)
    low = numpy.ma.median(mean_a_less_or_equal)
    return (high + low) / 2

# convert soft symbols into bits (assuming binary symbols)
def slice_bits(symbols):
    symbols_average = numpy.average(symbols)
    if debug:
        print("average amplitude: %s" % symbols_average)
    bits = (symbols >= symbols_average)
    return numpy.array(bits, dtype=numpy.uint8)

# Adapted from: https://stackoverflow.com/questions/28370991/converting-bits-to-bytes-in-python#28371638
def getbytes(bits):
    done = False
    while not done:
        byte = 0
        for _ in range(0, 8):
            try:
                bit = next(bits)
            except StopIteration:
                bit = 0
                done = True
            byte = (byte << 1) | bit
        yield byte

def getHex(bits):
    num_bytes = len(bits)//8

    # bits_lsb = []
    # for byte_idx in range(num_bytes):
    #     bits_lsb.extend(bits[byte_idx*num_bytes:(byte_idx+1)*num_bytes][::-1]) # select byte and inverse MSB-> LSB

    bits_str = "".join([str(b) for b in bits[:num_bytes*8]])
    print(bits_str)
    return hex(int(bits_str, 2))

def parsepacket(bits):  
    bytes_str = ''
    # packet structure
    # 1 0xAA 0x08 0x01 0x01 0x08 0x01 0x00 0x08 0x01 0xAB 1
    bits = bits[1:] # remove first bit
    print(getHex(bits))
    


def decode(values = []):
    global invalid_packets
    samples = np.array(values)

    # Graph packet
    if graph:
        plt.ion()
        plt.clf()
        plt.show()
        plt.plot(samples)
        plt.draw()
        plt.pause(0.000001)
    
    # Clock Recovery
    b = samples > midpoint(samples)
    d = numpy.diff(b)**2
    f = scipy.fft.fft(d, len(samples))
    p = find_clock_frequency(abs(f))
    p = int(p)
    
    # Symbol extraction
    cycles_per_sample = (p*1.0)/len(f)
    clock_phase = 0.5 + numpy.angle(f[p])/(tau)
    if clock_phase <= 0.5:
        clock_phase += 1
    symbols = []
    for sample in samples:
        if clock_phase >= 1:
            clock_phase -= 1
            symbols.append(sample)
        clock_phase += cycles_per_sample
    if debug:
        print("peak frequency index: %d / %d" % (p, len(f)))
        print("samples per symbol: %f" % (1.0/cycles_per_sample))
        print("clock cycles per sample: %f" % (cycles_per_sample))
        print("clock phase in cycles between 1st and 2nd samples: %f" % (clock_phase))
        print("clock phase in cycles at 1st sample: %f" % (clock_phase - cycles_per_sample/2))
        print("symbol count: %d" % (len(symbols)))
        print("invalid packet count: %d / %d" % (invalid_packets,packet_count))

    # Extract bits
    bits=slice_bits(symbols)
    # if debug:
    #     print(list(bits))

    def cmp(l1,l2):
        if len(l1) != len(l2):
            return False
        return all(x == y for x, y in zip(l1, l2))

    sync_found = False
    
    # Align to sync word for beginning of packet
    for i in range(1,len(bits)-SYNC_WORD_LEN):
        tmpbits = bits[i:i+SYNC_WORD_LEN]
        if cmp(SYNC_WORD, tmpbits):
            print("SYNC FOUND")
            # sync_found = True
            # bits = bits[i:i+6*8]
            parsepacket(list(bits[i:i+6*8]))
            # break
    

    # Parse and print packet bytes
    # if sync_found:
    #     parsepacket(list(bits))
    
def zmq_consumer():
    packet_finished = False     # Whether or not we have the last sample of the current packet
    packet_samples = 0          # Number of samples in the current packet (once we have them all)
    sps = 4                     # samples per symbol
    below_thresh = 0            # Number of samples since we've been below the threshold

    context = zmq.Context()
    results_amplitude = context.socket(zmq.PULL)
    results_amplitude.connect("tcp://127.0.0.1:5558")

    amplitude_ring = Queue(maxsize=80000)  # Buffer that contains the amplitude samples
    
    while True:
        # Read in the amplitude samples
        raw_amplitude = results_amplitude.recv()
        if not packet_finished:
            print('.', end="", flush=True)
        amp_list = array.array('f', raw_amplitude) # struct.unpack will be faster
        if len(amp_list) >= 0:
            for f in amp_list:
                if amplitude_ring.full():
                    packet_finished = True
                else:
                    amplitude_ring.put(f)
        
        # Send to demodulator when ready
        if packet_finished:
            packet = list(amplitude_ring.queue)
            decode(packet)
            _ = [amplitude_ring.get() for _ in range(amplitude_ring.qsize())]
            packet_finished = False
            below_thresh = 0
            

     
def main():

    zmq_consumer()

if __name__ == '__main__':
    main()
