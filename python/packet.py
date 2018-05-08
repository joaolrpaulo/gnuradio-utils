from gnuradio import gr, digital
from gnuradio import blocks
from gnuradio.digital import packet_utils
import gnuradio.gr.gr_threading as _threading

# payload length in bytes
DEFAULT_PAYLOAD_LEN = 512

# how many messages in a queue
DEFAULT_MSGQ_LIMIT = 10  # type: int

# threshold for unmaking packets
DEFAULT_THRESHOLD = 12

STATION_CODES = {
    "default": packet_utils.default_access_code,
    "0001": "1010110011011101101001001110001011110010100011000010000011111100"
}


##################################################
# Options Class for OFDM
##################################################
class options(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems(): setattr(self, key, value)


##################################################
# Packet Encoder
##################################################
class _packet_encoder_thread(_threading.Thread):

    def __init__(self, msgq, payload_length, send):
        self._msgq = msgq
        self._payload_length = payload_length
        self._send = send
        _threading.Thread.__init__(self)
        self.setDaemon(True)
        self.keep_running = True
        self.start()

    def run(self):
        while self.keep_running:
            sample = ''  # residual sample
            msg = self._msgq.delete_head()  # blocking read of message queue
            sample = sample + msg.to_string()  # get the body of the msg as a string

            while len(sample) >= self._payload_length:
                payload = sample[:self._payload_length]
                sample = sample[self._payload_length:]

                # check if sample has remaining data to transmit that is shorter than the payload length
                if 0 < len(sample) < self._payload_length:
                    # arbitrary padding to satisfy send on next loop for payload less than _payload_length
                    padding = ('x' * (self._payload_length - len(sample)))
                    sample = sample + padding

                self._send(payload)


class packet_encoder(gr.hier_block2):
    """
    Hierarchical block for wrapping packet-based modulators.
    """

    def __init__(self, station_id=''):
        """
        packet_mod constructor.

        Args:
            station_id: The ID of the station transmitting the data.
        """
        # setup parameters
        self._samples_per_symbol = 1
        self._bits_per_symbol = 1
        self._pad_for_usrp = False

        access_code = STATION_CODES[station_id] if station_id else STATION_CODES["default"]
        preamble = packet_utils.default_preamble

        if not packet_utils.is_1_0_string(preamble):
            raise ValueError, "Invalid preamble %r. Must be string of 1's and 0's" % (preamble,)
        if not packet_utils.is_1_0_string(access_code):
            raise ValueError, "Invalid access_code %r. Must be string of 1's and 0's" % (access_code,)

        self._preamble = preamble
        self._access_code = access_code

        # create blocks
        msg_source = blocks.message_source(gr.sizeof_char, DEFAULT_MSGQ_LIMIT)
        self._msgq_out = msg_source.msgq()
        # initialize hier2
        gr.hier_block2.__init__(
            self,
            "packet_encoder",
            gr.io_signature(0, 0, 0),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_char)  # Output signature
        )
        # connect
        self.connect(msg_source, self)

    def send_pkt(self, payload):
        """
        Wrap the payload in a packet and push onto the message queue.

        Args:
            payload: string, data to send
        """
        packet = packet_utils.make_packet(
            payload,
            self._samples_per_symbol,
            self._bits_per_symbol,
            self._preamble,
            self._access_code,
            self._pad_for_usrp
        )
        msg = gr.message_from_string(packet)
        self._msgq_out.insert_tail(msg)


##################################################
# Packet Decoder
##################################################
class _packet_decoder_thread(_threading.Thread):

    def __init__(self, msgq, callback):
        _threading.Thread.__init__(self)
        self.setDaemon(True)
        self._msgq = msgq
        self.callback = callback
        self.keep_running = True
        self.start()

    def run(self):
        while self.keep_running:
            msg = self._msgq.delete_head()
            ok, payload = packet_utils.unmake_packet(msg.to_string(), int(msg.arg1()))
            if self.callback:
                self.callback(ok, payload)


class packet_decoder(gr.hier_block2):
    """
    Hierarchical block for wrapping packet-based demodulators.
    """

    def __init__(self, station_id='', callback=None):
        """
        packet_demod constructor.

        Args:
            station_id: The ID of the station that we are trying to decode the data from.
        """
        # access code
        self._threshold = DEFAULT_THRESHOLD
        access_code = STATION_CODES[station_id] if station_id else STATION_CODES["default"]

        if not packet_utils.is_1_0_string(access_code):
            raise ValueError, "Invalid access_code %r. Must be string of 1's and 0's" % (access_code,)

        self._access_code = access_code

        # blocks
        msgq = gr.msg_queue(DEFAULT_MSGQ_LIMIT)  # holds packets from the PHY
        correlator = digital.correlate_access_code_bb(self._access_code, self._threshold)
        framer_sink = digital.framer_sink_1(msgq)
        # initialize hier2
        gr.hier_block2.__init__(
            self,
            "packet_decoder",
            gr.io_signature(1, 1, gr.sizeof_char),  # Input signature
            gr.io_signature(0, 0, 0)  # Output signature
        )
        # connect
        self.connect(self, correlator, framer_sink)
        # start thread
        _packet_decoder_thread(msgq, callback)


##################################################
# Packet Mod for OFDM Mod and Packet Encoder
##################################################
class packet_mod_base(gr.hier_block2):
    """
    Hierarchical block for wrapping packet source block.
    """

    def __init__(self, packet_source=None, payload_length=0):

        if not payload_length:  # get payload length
            payload_length = DEFAULT_PAYLOAD_LEN
        if (payload_length % self._item_size_in) != 0:  # verify that packet length is a multiple of the stream size
            raise ValueError, 'The payload length: "%d" is not a multiple of the stream size: "%d".' % (payload_length, self._item_size_in)
        # initialize hier2
        gr.hier_block2.__init__(
            self,
            "ofdm_mod",
            gr.io_signature(1, 1, self._item_size_in),  # Input signature
            gr.io_signature(1, 1, packet_source.output_signature().sizeof_stream_item(0))  # Output signature
        )
        # create blocks
        msgq = gr.msg_queue(DEFAULT_MSGQ_LIMIT)
        msg_sink = blocks.message_sink(self._item_size_in, msgq, False)  # False -> blocking
        # connect
        self.connect(self, msg_sink)
        self.connect(packet_source, self)
        # start thread
        _packet_encoder_thread(msgq, payload_length, packet_source.send_pkt)


class packet_mod_b(packet_mod_base): _item_size_in = gr.sizeof_char


class packet_mod_s(packet_mod_base): _item_size_in = gr.sizeof_short


class packet_mod_i(packet_mod_base): _item_size_in = gr.sizeof_int


class packet_mod_f(packet_mod_base): _item_size_in = gr.sizeof_float


class packet_mod_c(packet_mod_base): _item_size_in = gr.sizeof_gr_complex


##################################################
# Packet Demod for OFDM Demod and Packet Decoder
##################################################
class packet_demod_base(gr.hier_block2):
    """
    Hierarchical block for wrapping packet sink block.
    """

    def __init__(self, packet_sink=None):
        # initialize hier2
        gr.hier_block2.__init__(
            self,
            "ofdm_mod",
            gr.io_signature(1, 1, packet_sink.input_signature().sizeof_stream_item(0)),  # Input signature
            gr.io_signature(1, 1, self._item_size_out)  # Output signature
        )
        # create blocks
        msg_source = blocks.message_source(self._item_size_out, DEFAULT_MSGQ_LIMIT)
        self._msgq_out = msg_source.msgq()
        # connect
        self.connect(self, packet_sink)
        self.connect(msg_source, self)
        if packet_sink.output_signature().sizeof_stream_item(0):
            self.connect(packet_sink,
                         blocks.null_sink(packet_sink.output_signature().sizeof_stream_item(0)))

    def recv_pkt(self, ok, payload):
        msg = gr.message_from_string(payload, 0, self._item_size_out,
                                     len(payload) / self._item_size_out)
        if ok:
            self._msgq_out.insert_tail(msg)


class packet_demod_b(packet_demod_base): _item_size_out = gr.sizeof_char


class packet_demod_s(packet_demod_base): _item_size_out = gr.sizeof_short


class packet_demod_i(packet_demod_base): _item_size_out = gr.sizeof_int


class packet_demod_f(packet_demod_base): _item_size_out = gr.sizeof_float


class packet_demod_c(packet_demod_base): _item_size_out = gr.sizeof_gr_complex
