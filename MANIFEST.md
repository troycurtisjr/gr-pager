title: The pager OOT Module
brief: Motorola FLEX protocol decoder
tags:
  - sdr
  - pager
  - flex
author:
  - Troy Curtis <troy@troycurtisjr.com>
  - Johnathan Corgan <johnathan@corganlabs.com>
  - Andrew Jeffery <andrew@aj.id.au>
copyright_owner:
  - Free Software Foundation
dependencies:
  - gnuradio (>= 3.8.0)
gr_supported_version:
  - v3.8
repo: https://github.com/troycurtisjr/gr-pager
website: https://github.com/troycurtisjr/gr-pager
license: GPLv3
---

This OOT module implements the blocks needed to decode the Motorola FLEX pager
protocol. These pagers are still in use and typically transmit between 929 MHz
and 932 MHz.

This module is based on code that was previously in the main GNU Radio
repository, but which was removed for 3.8 since it is really a specific
application and not really a core function.
