#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Derived from the "table.py" module from https://github.com/osh/gr-pyqt
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

from gnuradio import gr, eng_notation
from PyQt5 import QtCore, QtWidgets
import pmt


class msg_table(gr.sync_block, QtWidgets.QTableWidget):
    """
    This is a PyQT-Table. It will be populated by PDU messages. For every new message, it will
    insert a new row. The list of columns are the values to extract and display from the meta-data
    header.
    """
    updateTrigger = QtCore.pyqtSignal()

    def __init__(self, *args, blkname="table", columns=tuple(), ascii_body=True):
        gr.sync_block.__init__(self, name="blkname", in_sig=[], out_sig=[])
        QtWidgets.QTableWidget.__init__(self, *args)
        self.message_port_register_in(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_input)
        self.scroll_to_bottom = True
        self.updateTrigger.connect(self.updatePosted)

        if not columns and not ascii_body:
            raise ValueError("At least one column or ascii_body must be specified.")

        ## table setup
        self.column_dict = {}  # mapping aid for column indices
        if ascii_body:
            self.body_label = "Message Body"

        self.columns = columns + [self.body_label]
        # set column headers
        for idx, column in enumerate(self.columns):
            item = QtWidgets.QTableWidgetItem(column)
            self.insertColumn(idx)
            self.setHorizontalHeaderItem(idx, item)
            self.column_dict[column] = idx
        self.setColumnCount(len(self.columns))

        self.horizontalHeader().setStretchLastSection(True)
        # make table non-writable
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)
        self.rowcount = 0

    @QtCore.pyqtSlot()
    def updatePosted(self):
        self.scrollToBottom()

    def handle_input(self, pdu):
        # Expect a pdu
        if not pmt.is_pair(pdu):
            print("Message is not a PDU")
            return
        meta = pmt.car(pdu)
        if not pmt.is_dict(meta):
            print("No meta field present")
            return

        meta_dict = pmt.to_python(meta)
        if not isinstance(meta_dict, dict):
            return

        self.setRowCount(self.rowcount + 1)
        # get the current row identifier
        for col, idx in self.column_dict.items():
            if col == self.body_label:
                msg_pmt = pmt.cdr(pdu)
                msg_bytes = bytes(pmt.u8vector_elements(msg_pmt))
                value = msg_bytes.decode("utf8", errors="replace")
                display = str(value)
            elif col == "frequency":
                value = meta_dict.get(col)
                display = eng_notation.num_to_str(value) + "Hz"
            else:
                value = meta_dict.get(col)
                display = str(value)

            tab_item = QtWidgets.QTableWidgetItem(display)
            self.setItem(self.rowcount, idx, tab_item)

        self.rowcount += 1
        if self.scroll_to_bottom:
            self.updateTrigger.emit()

    def work(self, input_items, output_items):
        pass
