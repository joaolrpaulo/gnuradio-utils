#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import struct
import numpy as np
from gnuradio import gr
from datetime import datetime
import zmq


class messageEncoder(gr.sync_block):

    def __init__(self, stationid="1"):
        gr.sync_block.__init__(
            self,
            name='Message Encoder',
            in_sig=None,
            out_sig=[np.int8]
        )

        self.stationid = stationid
        self.first_time = True

    def work(self, input_items, output_items):
        # Sleep for a while to send and receive information
        if not self.first_time:
            time.sleep(5)
        else:
            self.first_time = False

        output_items[0] = self.stationid

        return len(output_items[0])

        # timestamp_info = bytearray(struct.pack("I", int(self.id)))
        #
        # timestamp_info_len = len(timestamp_info)
        # output_0_len = len(output_items[0])
        #
        # timestamp_info.extend(output_items[0][ timestamp_info_len : output_0_len ])
        #
        # output_items[0][:] = timestamp_info
        #
        # return len(output_items[0][ : timestamp_info_len ])

