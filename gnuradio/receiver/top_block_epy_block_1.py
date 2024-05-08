"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Symbol detector',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.set_history(2) # The comand set_history(x) appends the previous x-1 items to the input buffer (input_items), while the x'th item is the current value.

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        edges = np.diff(input_items[0])**2
        output_items[0][:] = edges

        return len(output_items[0])
