#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Troy Curtis, Jr..
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

from gnuradio import gr, gr_unittest, blocks, analog
from flex_receiver import flex_receiver

class qa_flex_receiver(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_with_noise(self):
        # set up fg
        noise = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 1, 0, 8192)
        head = blocks.head(gr.sizeof_gr_complex*1, 2048)
        rcvr = flex_receiver(0, 50e3)
        msgsink = blocks.message_debug()
        self.tb.connect((noise, 0), (head, 0))
        self.tb.connect((head, 0), (rcvr, 0))
        self.tb.msg_connect((rcvr, 'pages'), (msgsink, 'store'))
        self.tb.run()
        # No data is expected to be output, this merely tests that a noise source won't crash any
        # of the pieces which are knit together with the flex_receiver heir block.
        self.assertEqual(0, msgsink.num_messages())


if __name__ == '__main__':
    gr_unittest.run(qa_flex_receiver)
