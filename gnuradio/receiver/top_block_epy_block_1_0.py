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

    def __init__(self, sps=10, frame_size=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Gate till edge',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.sps = sps
        self.record_ongoing = False
        self.remainig_samples = 0
        self.trigger_detected = False

    def forecast(self, noutput_items, ninputs):
        # ensure 5 symbols before processing
        return [int(self.sps*5) for ii in range(ninputs)]

    def find_first(item, vec):
        for i in range(len(vec)):
            if item == vec[i]:
                return i
        return -1 

    def general_work(self, input_items, output_items):
        samples = input_items[0]

        output_samples = []

        # if 0->1 detected start new recording if not already done so, and output frame_size*self.sps
        if self.record_ongoing and self.remainig_samples > 0: #todo ensure the remaing samples ar larger then input_items
            output_samples = samples[:self.remainig_samples]
            self.remainig_samples = 0
            self.record_ongoing = False

        if not self.record_ongoing:
            # check if new positive edge is found
            edge_idx = find_first(1, np.diff(samples)) + 1 # first where diff is 0->1, ie is 1 is positive edge and +1 bcs 1 starts at edge+1

            if edge_idx > 0: # found an edge
                self.record_ongoing = True

                num_remaining_samples = len(samples) - edge_idx

                if num_remaining_samples < frame_size*self.sps:
                    self.remainig_samples = frame_size*self.sps-num_remaining_samples
                    num_samples_to_process = frame_size*self.sps - self.remainig_samples
                else:
                    num_samples_to_process = frame_size*self.sps
                    self.record_ongoing = False

                output_samples = samples[edge_idx:edge_idx+num_samples_to_process]


        if len(output_items[0]) < len(output_samples): 
            output_samples = output_samples[:len(output_items[0])]

        self.consume(0, len(samples))

        return len(output_samples)
