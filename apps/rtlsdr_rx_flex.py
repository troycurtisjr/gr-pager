#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RTLSDR FLEX Pager Receiver (Single Channel)
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import os, math
import osmosdr
import time
import pager
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from gnuradio import qtgui

class rtlsdr_rx_flex(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RTLSDR FLEX Pager Receiver (Single Channel)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RTLSDR FLEX Pager Receiver (Single Channel)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "rtlsdr_rx_flex")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.config_filename = config_filename = os.environ["HOME"]+"/.gnuradio/config.conf"
        self.symbol_rate = symbol_rate = 3200
        self._saved_channel_config = configparser.ConfigParser()
        self._saved_channel_config.read(config_filename)
        try: saved_channel = self._saved_channel_config.getint('gr-pager', 'channel')
        except: saved_channel = 25
        self.saved_channel = saved_channel
        self._saved_band_freq_config = configparser.ConfigParser()
        self._saved_band_freq_config.read(config_filename)
        try: saved_band_freq = self._saved_band_freq_config.getfloat('gr-pager', 'band_center')
        except: saved_band_freq = 930.5125e6
        self.saved_band_freq = saved_band_freq
        self.deviation = deviation = 4800
        self.decim = decim = 1
        self.adc_rate = adc_rate = 2048000
        self.sample_rate = sample_rate = adc_rate/decim
        self.passband = passband = 2*(deviation+symbol_rate)
        self.channel_rate = channel_rate = 8*3200
        self.channel = channel = saved_channel
        self.band_freq = band_freq = saved_band_freq
        self._saved_rx_gain_config = configparser.ConfigParser()
        self._saved_rx_gain_config.read(config_filename)
        try: saved_rx_gain = self._saved_rx_gain_config.getint('gr-pager', 'rx_gain')
        except: saved_rx_gain = 40
        self.saved_rx_gain = saved_rx_gain
        self._saved_offset_config = configparser.ConfigParser()
        self._saved_offset_config.read(config_filename)
        try: saved_offset = self._saved_offset_config.getfloat('gr-pager', 'freq_offset')
        except: saved_offset = 0
        self.saved_offset = saved_offset
        self.freq = freq = band_freq+(channel-61)*25e3
        self.channel_taps = channel_taps = firdes.low_pass(10, sample_rate, passband/2.0, (channel_rate-passband)/2.0)
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = freq
        self.rx_gain = rx_gain = saved_rx_gain
        self.offset = offset = saved_offset
        self.nchan_taps = nchan_taps = len(channel_taps)
        self.ma_ntaps = ma_ntaps = int(channel_rate/symbol_rate)
        self.demod_k = demod_k = 3*channel_rate/(2*math.pi*deviation)
        self.channel_decim = channel_decim = int(sample_rate/channel_rate)
        self.bb_interp = bb_interp = 5
        self.bb_decim = bb_decim = 8
        self.baseband_rate = baseband_rate = 16000

        ##################################################
        # Blocks
        ##################################################
        self.tabwidget = Qt.QTabWidget()
        self.tabwidget_widget_0 = Qt.QWidget()
        self.tabwidget_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabwidget_widget_0)
        self.tabwidget_grid_layout_0 = Qt.QGridLayout()
        self.tabwidget_layout_0.addLayout(self.tabwidget_grid_layout_0)
        self.tabwidget.addTab(self.tabwidget_widget_0, 'RX Spectrum')
        self.tabwidget_widget_1 = Qt.QWidget()
        self.tabwidget_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabwidget_widget_1)
        self.tabwidget_grid_layout_1 = Qt.QGridLayout()
        self.tabwidget_layout_1.addLayout(self.tabwidget_grid_layout_1)
        self.tabwidget.addTab(self.tabwidget_widget_1, 'Baseband')
        self.top_grid_layout.addWidget(self.tabwidget)
        self._rx_gain_range = Range(0, 100, 1, saved_rx_gain, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'Analog RX Gain', "counter_slider", int)
        self.tabwidget_grid_layout_0.addWidget(self._rx_gain_win, 0, 4, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 5):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self._offset_range = Range(-12.5e3, 12.5e3, 25e3/200, saved_offset, 200)
        self._offset_win = RangeWidget(self._offset_range, self.set_offset, 'Freq Offset', "counter_slider", float)
        self.tabwidget_grid_layout_0.addWidget(self._offset_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self._band_freq_tool_bar = Qt.QToolBar(self)
        self._band_freq_tool_bar.addWidget(Qt.QLabel('Band Freq.' + ": "))
        self._band_freq_line_edit = Qt.QLineEdit(str(self.band_freq))
        self._band_freq_tool_bar.addWidget(self._band_freq_line_edit)
        self._band_freq_line_edit.returnPressed.connect(
            lambda: self.set_band_freq(eng_notation.str_to_num(str(self._band_freq_line_edit.text()))))
        self.tabwidget_grid_layout_0.addWidget(self._band_freq_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Channel Freq' + ": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.tabwidget_grid_layout_0.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(sample_rate)
        self.rtlsdr_source_0.set_center_freq(band_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(rx_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=bb_decim,
                decimation=bb_interp,
                taps=[1.0/ma_ntaps,]*ma_ntaps*bb_interp,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            band_freq, #fc
            sample_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tabwidget_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 0, 4, 5)
        for r in range(3, 7):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 5):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            baseband_rate, #samp_rate
            "Slicer Output", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.tabwidget_grid_layout_1.addWidget(self._qtgui_time_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tabwidget_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabwidget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            baseband_rate, #samp_rate
            "FM Demod", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tabwidget_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabwidget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            channel_rate, #bw
            "Baseband", #name
            1
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(0.2)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.tabwidget_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabwidget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            band_freq, #fc
            sample_rate, #bw
            "Full Band Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tabwidget_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 2, 5)
        for r in range(1, 3):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 5):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self.pager_slicer_fb_0 = pager.slicer_fb(1e-6)
        self.pager_flex_sync_0 = pager.flex_sync()
        self.pager_flex_deinterleave_0_1_0 = pager.flex_deinterleave()
        self.pager_flex_deinterleave_0_1 = pager.flex_deinterleave()
        self.pager_flex_deinterleave_0_0 = pager.flex_deinterleave()
        self.pager_flex_deinterleave_0 = pager.flex_deinterleave()
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(channel_decim, channel_taps, (freq-band_freq)+offset, sample_rate)
        self.fm_demod = analog.quadrature_demod_cf(demod_k)
        self._channel_range = Range(1, 120, 1, saved_channel, 200)
        self._channel_win = RangeWidget(self._channel_range, self.set_channel, 'Channel', "counter_slider", int)
        self.tabwidget_grid_layout_0.addWidget(self._channel_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tabwidget_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabwidget_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.fm_demod, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fm_demod, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.pager_flex_deinterleave_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.pager_flex_deinterleave_0_0, 0), (self.blocks_null_sink_0_2, 0))
        self.connect((self.pager_flex_deinterleave_0_1, 0), (self.blocks_null_sink_0_1, 0))
        self.connect((self.pager_flex_deinterleave_0_1_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.pager_flex_sync_0, 0), (self.pager_flex_deinterleave_0, 0))
        self.connect((self.pager_flex_sync_0, 3), (self.pager_flex_deinterleave_0_0, 0))
        self.connect((self.pager_flex_sync_0, 2), (self.pager_flex_deinterleave_0_1, 0))
        self.connect((self.pager_flex_sync_0, 1), (self.pager_flex_deinterleave_0_1_0, 0))
        self.connect((self.pager_slicer_fb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.pager_slicer_fb_0, 0), (self.pager_flex_sync_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.pager_slicer_fb_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rtlsdr_rx_flex")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_config_filename(self):
        return self.config_filename

    def set_config_filename(self, config_filename):
        self.config_filename = config_filename
        self._saved_band_freq_config = configparser.ConfigParser()
        self._saved_band_freq_config.read(self.config_filename)
        if not self._saved_band_freq_config.has_section('gr-pager'):
        	self._saved_band_freq_config.add_section('gr-pager')
        self._saved_band_freq_config.set('gr-pager', 'band_center', str(self.band_freq))
        self._saved_band_freq_config.write(open(self.config_filename, 'w'))
        self._saved_channel_config = configparser.ConfigParser()
        self._saved_channel_config.read(self.config_filename)
        if not self._saved_channel_config.has_section('gr-pager'):
        	self._saved_channel_config.add_section('gr-pager')
        self._saved_channel_config.set('gr-pager', 'channel', str(self.channel))
        self._saved_channel_config.write(open(self.config_filename, 'w'))
        self._saved_offset_config = configparser.ConfigParser()
        self._saved_offset_config.read(self.config_filename)
        if not self._saved_offset_config.has_section('gr-pager'):
        	self._saved_offset_config.add_section('gr-pager')
        self._saved_offset_config.set('gr-pager', 'freq_offset', str(self.offset))
        self._saved_offset_config.write(open(self.config_filename, 'w'))
        self._saved_rx_gain_config = configparser.ConfigParser()
        self._saved_rx_gain_config.read(self.config_filename)
        if not self._saved_rx_gain_config.has_section('gr-pager'):
        	self._saved_rx_gain_config.add_section('gr-pager')
        self._saved_rx_gain_config.set('gr-pager', 'rx_gain', str(self.rx_gain))
        self._saved_rx_gain_config.write(open(self.config_filename, 'w'))

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_ma_ntaps(int(self.channel_rate/self.symbol_rate))
        self.set_passband(2*(self.deviation+self.symbol_rate))

    def get_saved_channel(self):
        return self.saved_channel

    def set_saved_channel(self, saved_channel):
        self.saved_channel = saved_channel
        self.set_channel(self.saved_channel)

    def get_saved_band_freq(self):
        return self.saved_band_freq

    def set_saved_band_freq(self, saved_band_freq):
        self.saved_band_freq = saved_band_freq
        self.set_band_freq(self.saved_band_freq)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_demod_k(3*self.channel_rate/(2*math.pi*self.deviation))
        self.set_passband(2*(self.deviation+self.symbol_rate))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_sample_rate(self.adc_rate/self.decim)

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.set_sample_rate(self.adc_rate/self.decim)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.set_channel_decim(int(self.sample_rate/self.channel_rate))
        self.set_channel_taps(firdes.low_pass(10, self.sample_rate, self.passband/2.0, (self.channel_rate-self.passband)/2.0))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.band_freq, self.sample_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.band_freq, self.sample_rate)
        self.rtlsdr_source_0.set_sample_rate(self.sample_rate)

    def get_passband(self):
        return self.passband

    def set_passband(self, passband):
        self.passband = passband
        self.set_channel_taps(firdes.low_pass(10, self.sample_rate, self.passband/2.0, (self.channel_rate-self.passband)/2.0))

    def get_channel_rate(self):
        return self.channel_rate

    def set_channel_rate(self, channel_rate):
        self.channel_rate = channel_rate
        self.set_channel_decim(int(self.sample_rate/self.channel_rate))
        self.set_channel_taps(firdes.low_pass(10, self.sample_rate, self.passband/2.0, (self.channel_rate-self.passband)/2.0))
        self.set_demod_k(3*self.channel_rate/(2*math.pi*self.deviation))
        self.set_ma_ntaps(int(self.channel_rate/self.symbol_rate))
        self.qtgui_freq_sink_x_1.set_frequency_range(self.freq, self.channel_rate)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq(self.band_freq+(self.channel-61)*25e3)
        self._saved_channel_config = configparser.ConfigParser()
        self._saved_channel_config.read(self.config_filename)
        if not self._saved_channel_config.has_section('gr-pager'):
        	self._saved_channel_config.add_section('gr-pager')
        self._saved_channel_config.set('gr-pager', 'channel', str(self.channel))
        self._saved_channel_config.write(open(self.config_filename, 'w'))

    def get_band_freq(self):
        return self.band_freq

    def set_band_freq(self, band_freq):
        self.band_freq = band_freq
        Qt.QMetaObject.invokeMethod(self._band_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.band_freq)))
        self.set_freq(self.band_freq+(self.channel-61)*25e3)
        self._saved_band_freq_config = configparser.ConfigParser()
        self._saved_band_freq_config.read(self.config_filename)
        if not self._saved_band_freq_config.has_section('gr-pager'):
        	self._saved_band_freq_config.add_section('gr-pager')
        self._saved_band_freq_config.set('gr-pager', 'band_center', str(self.band_freq))
        self._saved_band_freq_config.write(open(self.config_filename, 'w'))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.freq-self.band_freq)+self.offset)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.band_freq, self.sample_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.band_freq, self.sample_rate)
        self.rtlsdr_source_0.set_center_freq(self.band_freq, 0)

    def get_saved_rx_gain(self):
        return self.saved_rx_gain

    def set_saved_rx_gain(self, saved_rx_gain):
        self.saved_rx_gain = saved_rx_gain
        self.set_rx_gain(self.saved_rx_gain)

    def get_saved_offset(self):
        return self.saved_offset

    def set_saved_offset(self, saved_offset):
        self.saved_offset = saved_offset
        self.set_offset(self.saved_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.freq))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.freq-self.band_freq)+self.offset)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.freq, self.channel_rate)

    def get_channel_taps(self):
        return self.channel_taps

    def set_channel_taps(self, channel_taps):
        self.channel_taps = channel_taps
        self.set_nchan_taps(len(self.channel_taps))
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.channel_taps)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self._saved_rx_gain_config = configparser.ConfigParser()
        self._saved_rx_gain_config.read(self.config_filename)
        if not self._saved_rx_gain_config.has_section('gr-pager'):
        	self._saved_rx_gain_config.add_section('gr-pager')
        self._saved_rx_gain_config.set('gr-pager', 'rx_gain', str(self.rx_gain))
        self._saved_rx_gain_config.write(open(self.config_filename, 'w'))
        self.rtlsdr_source_0.set_gain(self.rx_gain, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self._saved_offset_config = configparser.ConfigParser()
        self._saved_offset_config.read(self.config_filename)
        if not self._saved_offset_config.has_section('gr-pager'):
        	self._saved_offset_config.add_section('gr-pager')
        self._saved_offset_config.set('gr-pager', 'freq_offset', str(self.offset))
        self._saved_offset_config.write(open(self.config_filename, 'w'))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.freq-self.band_freq)+self.offset)

    def get_nchan_taps(self):
        return self.nchan_taps

    def set_nchan_taps(self, nchan_taps):
        self.nchan_taps = nchan_taps

    def get_ma_ntaps(self):
        return self.ma_ntaps

    def set_ma_ntaps(self, ma_ntaps):
        self.ma_ntaps = ma_ntaps
        self.rational_resampler_xxx_0.set_taps([1.0/self.ma_ntaps,]*self.ma_ntaps*self.bb_interp)

    def get_demod_k(self):
        return self.demod_k

    def set_demod_k(self, demod_k):
        self.demod_k = demod_k
        self.fm_demod.set_gain(self.demod_k)

    def get_channel_decim(self):
        return self.channel_decim

    def set_channel_decim(self, channel_decim):
        self.channel_decim = channel_decim

    def get_bb_interp(self):
        return self.bb_interp

    def set_bb_interp(self, bb_interp):
        self.bb_interp = bb_interp
        self.rational_resampler_xxx_0.set_taps([1.0/self.ma_ntaps,]*self.ma_ntaps*self.bb_interp)

    def get_bb_decim(self):
        return self.bb_decim

    def set_bb_decim(self, bb_decim):
        self.bb_decim = bb_decim

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.baseband_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.baseband_rate)





def main(top_block_cls=rtlsdr_rx_flex, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
