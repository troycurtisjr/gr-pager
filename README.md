FLEX Pager Demodulator
=============================

This is an out-of-tree (OOT) module for GNU Radio which can demodulate and decode Motorola FLEX
radiopager signals. In the US, these pager signals typically occur between 929 MHz and 932 MHz at 25
kHz centers. Despite the prevalence of cellphone technology, pagers are still surprisingly
widespread. The protocol is also simple with a robust frequency excursion, which when coupled with
the high power output from the pager towers, makes this signal a very easy one to find and decode.

As with demodulating any over-the-air transmission, you should check your local laws to ensure you
are in full compliance.

Note that this module was extracted from the GNU Radio project after it removed it from the main
upstream.

Getting Started
------------------

* Requirements
    * GNU Radio 3.10/3.11

The high-level steps are to clone this git repo, compile the module, and install.

    $ git clone https://github.com/troycurtisjr/gr-pager.git
    $ mkdir gr-pager/build
    $ cd gr-pager/build
    $ cmake ..
    $ make -j5
    $ make install
      - or -
    $ sudo make install
    
Example GNU Radio Companion flowgraphs for RTLSDR and USRP can be found in the examples directory.
Open one of these files with GRC and run it to get receiving quickly! If you have some other type of
receiver it should be relatively easy to swap out the source block from either graph which your own.

There are also a few included "apps", or standalone scripts, which can be used for command line
demodulation. Supplying the `--help` option to any of the commands will give you specific usage.
Here is the summary:

* flex_band
    * File or RTLSDR receiver with a configurable number of channels to demodulate in parallel
* usrp_flex
    * File or USRP receiver for a single paging channel
* usrp_flex_band
    * File or USRP receiver for a 1 MHz paging band (40 pager channels).
* usrp_flex_all
    * File or USRP receiver for the full 3 MHz paging band (120 pager channels). This may overload
      your CPU and not run in real time (try using a file instead).
      
Acknowledgments
------------------

This module was extracted from the main GNU Radio source code, specifically from commit
f1f49ff9b18d5e4ebbee4ddd279244f562672e0f. I took care to extract the code with history, so that all
the prior work done by many individuals while it was in-tree to GNU Radio is properly preserved. In
particular, Johnathan Corgan was the primary author. I can take almost no credit for the modulation
code in this module, I only ported it over to work with GNU Radio 3.8 and added a few utility
blocks.
