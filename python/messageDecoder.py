#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import numpy as np
from gnuradio import gr
import zmq


class messageDecoder(gr.sync_block):

    def __init__(self, stationid="1"):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Message Decoder',
            in_sig=[np.int8],
            out_sig=None
        )

        self.context = zmq.Context()

        #  Socket to talk to server
        self.socket = self.context.socket(zmq.DEALER)

        self.socket.setsockopt(zmq.IDENTITY, b"%s" % stationid)
        self.socket.connect("tcp://localhost:10001")

    def work(self, input_items, output_items):
        now = datetime.now()

        self.socket.send("%s" % np.datetime64(now).view('<i8'))

        return len(input_items[0])

    def stop(self):
        self.socket.close()


