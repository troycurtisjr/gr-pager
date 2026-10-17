#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Troy Curtis, Jr.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import math
import sys
import signal

from gnuradio import gr
from gnuradio import analog
from gnuradio import filter

import gnuradio.pager as pager

class flex_receiver(gr.hier_block2):
    """
    Decodes pages from a baseband input.

    The input is expected to be complex data, centered on a FLEX pager transmission. The input
    sample-rate should be at least 16kHz, preferably a bit larger.

    Pages are output as Payload Data Unit (PDU) on the message port called 'pages'. Meta-data such
    as the frequency and capcode are in the "header", and the body is an ascii encoded u8 vector.

    This block is simply a hier block which knits together all the necessary flex_pager blocks,
    plus a resampling and demodulation block, in order to provide a complete pager receiving
    solution.
    """
    def __init__(self, frequency, sample_rate):
        gr.hier_block2.__init__(self,
                                "Flex Pager Receiver",
                                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                                gr.io_signaturev(3, 3, [gr.sizeof_gr_complex*1, gr.sizeof_float*1, gr.sizeof_char*1]),
                                )
        self.message_port_register_hier_out("pages")

        ##################################################
        # Parameters
        ##################################################
        self.frequency = frequency
        self.sample_rate = sample_rate

        ##################################################
        # Variables
        ##################################################
        self.passband = passband = 15e3
        self.deviation = deviation = 4800
        self.decode_samp_rate = decode_samp_rate = 16000
        self.transition_band = transition_band = decode_samp_rate-passband
        self.interp = interp = 32
        self.demod_k = demod_k = 3*decode_samp_rate/(2*math.pi*deviation)
        self.atten = atten = 100

        ##################################################
        # Blocks
        ##################################################
        self.pfb_arb_resampler_xxx_0 = filter.pfb.arb_resampler_ccf(
            decode_samp_rate/sample_rate,
            taps=self.get_filter_taps(),
            flt_size=interp)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.pager_slicer_fb_0 = pager.slicer_fb(5e-6)
        self.pager_flex_sync_0 = pager.flex_sync()
        self.pager_flex_deinterleavers = [pager.flex_deinterleave() for _ in range(4)]
        self.pager_flex_decoders = [pager.flex_decode(frequency) for _ in range(4)]
        self.fm_demod = analog.quadrature_demod_cf(demod_k)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.fm_demod, 0), (self, 1))
        self.connect((self.fm_demod, 0), (self.pager_slicer_fb_0, 0))
        self.connect((self, 0), (self.pfb_arb_resampler_xxx_0, 0))
        for i in range(4):
            self.connect((self.pager_flex_sync_0, i),
                         (self.pager_flex_deinterleavers[i], 0))
            self.connect((self.pager_flex_deinterleavers[i], 0),
                         (self.pager_flex_decoders[i], 0))
            self.msg_connect((self.pager_flex_decoders[i], 'pages'), (self, 'pages'))

        self.connect((self.pager_slicer_fb_0, 0), (self, 2))
        self.connect((self.pager_slicer_fb_0, 0), (self.pager_flex_sync_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.fm_demod, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self, 0))


    def get_filter_taps(self):
        return filter.firdes.low_pass_2(
            self.interp,
            self.interp*self.sample_rate,
            self.passband/2,
            self.transition_band,
            attenuation_dB=self.atten,
            window=filter.window.WIN_BLACKMAN_hARRIS)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        for decoder in self.pager_flex_decoders:
            decoder.set_freq(self.frequency)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.pfb_arb_resampler_xxx_0.set_taps(self.get_filter_taps())
        self.pfb_arb_resampler_xxx_0.set_rate(self.decode_samp_rate/self.sample_rate)

    def get_passband(self):
        return self.passband

    def set_passband(self, passband):
        self.passband = passband
        self.set_transition_band(self.decode_samp_rate-self.passband)
        self.pfb_arb_resampler_xxx_0.set_taps(self.get_filter_taps())

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_demod_k(3*self.decode_samp_rate/(2*math.pi*self.deviation))

    def get_decode_samp_rate(self):
        return self.decode_samp_rate

    def set_decode_samp_rate(self, decode_samp_rate):
        self.decode_samp_rate = decode_samp_rate
        self.set_demod_k(3*self.decode_samp_rate/(2*math.pi*self.deviation))
        self.set_transition_band(self.decode_samp_rate-self.passband)
        self.pfb_arb_resampler_xxx_0.set_rate(self.decode_samp_rate/self.sample_rate)

    def get_transition_band(self):
        return self.transition_band

    def set_transition_band(self, transition_band):
        self.transition_band = transition_band
        self.pfb_arb_resampler_xxx_0.set_taps(self.get_filter_taps())

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.pfb_arb_resampler_xxx_0.set_taps(self.get_filter_taps())

    def get_demod_k(self):
        return self.demod_k

    def set_demod_k(self, demod_k):
        self.demod_k = demod_k
        self.fm_demod.set_gain(self.demod_k)

    def get_atten(self):
        return self.atten

    def set_atten(self, atten):
        self.atten = atten
        self.pfb_arb_resampler_xxx_0.set_taps(self.get_filter_taps())
