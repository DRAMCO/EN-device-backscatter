"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.decim_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, decim_rate=10, sps=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.decim_block.__init__(
            self,
            name='Median',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8],
            decim = decim_rate)
        self.sps = sps
        self.set_relative_rate(1.0/decim_rate)
        self.decimation = decim_rate

    # def forecast(self, noutput_items, ninputs):
    #     # ensure 1 symbols before processing
    #     return [int(self.sps) for ii in range(ninputs)]

    def work(self, input_items, output_items):
        samples = input_items[0]

        N = len(samples)

        num_symbols = N//self.sps
        
        samples_consumed = samples[:num_symbols*self.sps]

        bits_per_symbol = np.split(samples_consumed, num_symbols)

        symbols = [np.median(bits_per_symb) for bits_per_symb in bits_per_symbol]

        output_items[0][:] = symbols

        # self.consume(0, len(samples_consumed))

        return len(output_items[0])
