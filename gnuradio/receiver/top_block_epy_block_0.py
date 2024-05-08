"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import numpy as np


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, sps=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__( 
            self,
            name='OOK threshold',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.uint8, np.float32, np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.avg = -1.0
        self.max = 0.0
        self.min = 1.0
        self.sps = sps

    def forecast(self, noutput_items, ninputs):
        # ensure 100 symbols before processing
        return [int(self.sps*100) for ii in range(ninputs)]


    def work(self, input_items, output_items):
        """example: multiply with constant"""

        if not len(input_items[0]) > 0:
            return 0


        _max = np.max(input_items[0])
        _min = np.min(input_items[0])

        self.max += _max
        self.max /=2

        self.min += _min
        self.min /=2


        threshold = (self.max + self.min) * 0.2

        results = np.ones(len(input_items[0]), dtype=np.uint8)
        results[input_items[0] < threshold] = 0

        output_items[0][:] = results
        output_items[1][:] = self.max
        output_items[2][:] = self.min
        output_items[3][:] = threshold
        return len(output_items[0])
