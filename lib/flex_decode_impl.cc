/* -*- c++ -*- */
/*
 * Copyright 2020 Troy Curtis, Jr.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "flex_decode_impl.h"
#include "flex_modes.h"
#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>
#include <time.h>
#include <iostream>

namespace gr {
namespace pager {

flex_decode::sptr flex_decode::make(float freq)
{
    return gnuradio::get_initial_sptr(new flex_decode_impl(freq));
}


/*
 * The private constructor
 */
flex_decode_impl::flex_decode_impl(float freq)
    : gr::sync_block("flex_decode",
                     gr::io_signature::make(1, 1, sizeof(int32_t)),
                     gr::io_signature::make(0, 0, 0)),
      d_freq(freq),
      d_frame(),
      d_payload(),
      d_datawords(),
      d_count(0),
      d_outport(pmt::intern("pages"))
{
    message_port_register_out(d_outport);
}

/*
 * Our virtual destructor.
 */
flex_decode_impl::~flex_decode_impl() {}

int flex_decode_impl::work(int noutput_items,
                           gr_vector_const_void_star& input_items,
                           gr_vector_void_star& output_items)
{
    const int32_t* in = reinterpret_cast<const int32_t*>(input_items[0]);

    pmt::pmt_t key_freq = pmt::intern("freq");
    pmt::pmt_t key_type = pmt::intern("type");
    pmt::pmt_t key_capcode = pmt::intern("capcode");
    pmt::pmt_t key_rx_time = pmt::intern("rx_time");
    const uint64_t curTime = static_cast<uint64_t>(time(nullptr));
    pmt::pmt_t timeval = pmt::make_tuple(pmt::from_uint64(curTime), pmt::from_double(0));

    int i = 0;
    while (i < noutput_items) {
        // Accumulate one whole frame's worth of data words (88 of them)
        d_datawords[d_count] = *in++;
        i++;
        if (++d_count == flex_frame::FRAME_WORDS) {
            const std::vector<flex_page>& pages =
                d_frame.parse(d_freq, &d_datawords[0], d_count);
            for (auto&& page : pages) {
                // Construct the PMT message
                pmt::pmt_t hdr = pmt::make_dict();
                hdr = pmt::dict_add(hdr, key_freq, pmt::from_double(page.freq));
                hdr =
                    pmt::dict_add(hdr, key_type, pmt::intern(flex_page_desc[page.type]));
                hdr = pmt::dict_add(hdr, key_capcode, pmt::from_long(page.capcode));
                hdr = pmt::dict_add(hdr, key_rx_time, timeval);
                pmt::pmt_t body = pmt::init_u8vector(
                    page.data_len, reinterpret_cast<const uint8_t*>(&page.data[0]));
                pmt::pmt_t msg = pmt::cons(hdr, body);

                message_port_pub(d_outport, msg);
            }
            d_count = 0;
        }
    }

    return i;
}

void flex_decode_impl::set_freq(float freq) { d_freq = freq; }

float flex_decode_impl::get_freq() const { return d_freq; }

} /* namespace pager */
} /* namespace gr */
