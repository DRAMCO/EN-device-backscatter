"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, samp_rate=1E6, sps=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='OOK Demodulator',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )

        # amount of samples per symbol
        self.sps = sps
        self.threshold = samp_rate / sps
        # amount of samples that can be wrong when counting the 1's and 0's
        self.error_threshold = self.threshold // 4

        self.packet = ''
        self.count_1 = 0 # Counts consecutive 1's
        self.count_0 = 0 # Counts consecutive 0's
        self.sample_1_complete = False
        self.sample_0_complete = False
        self.first_trigger = False

    def forecast(self, noutput_items, ninputs):
        # ensure 10 symbols before processing
        return [int(self.sps*10) for ii in range(ninputs)]

    def general_work(self, input_items, output_items):
        samples = input_items[0]

        num_samples = len(samples)

        samples = np.array(samples)

        symbols = []

        sample_idx = 0

        if num_samples == 0:
            return 0

        # wait till first trigger occurs, and start symbol timing from that
        if not self.first_trigger:
            signal_detected = np.sum(np.diff(input_items[0]) == 1) # num positive edge triggers
            if signal_detected:
                sample_idx = np.where(np.diff(input_items[0]) == 1)[0][0]
                if num_samples-sample_idx > self.sps:
                    self.first_trigger = True

        if not self.first_trigger:
            num_remaining_symbols = (num_samples - sample_idx)//self.sps
            print(num_remaining_symbols)
            if num_remaining_symbols > 0:
                # only process the remaining symbols and leave the rest for next block iteration
                num_processed_samples = sample_idx+num_remaining_symbols*self.sps
                # by not processing the last remaing bits, we essentially put the next timing trigger on the first bit in the next block iteration
                samples_to_process = samples[sample_idx:num_remaining_symbols*self.sps]
                bits_per_symbol = np.split(samples_to_process, num_remaining_symbols)
                symbols = [np.median(s) for s in bits_per_symbol]

                self.consume(0, num_processed_samples)
                self.produce(0, len(symbols))
                output_items[0][:len(symbols)] = symbols
            else:
                self.consume(0, 0)
                self.produce(0, 0)

        else:
            self.consume(0, 0)

        return len(symbols)


    def count_samples(self, sample1, sample2):
        if(sample1 == 1):
            self.count_1 += 1
            if(sample2 == 0):
                self.sample_1_complete = True 
        elif(sample1 == 0):
            self.count_0 += 1
            if(sample2 == 1):
                self.sample_0_complete = True 

    
    def process_sample(self, bit, count):
        if(count > self.threshold - self.error_threshold and count < self.threshold + self.error_threshold):
            return [bit], False
        elif count < (self.threshold - self.error_threshold):
            # ignore 
             return None, True
        else:
            num_bits =  int(count//(self.threshold - self.threshold//10))
            return [bit]*num_bits, False

