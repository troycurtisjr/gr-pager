/* -*- c++ -*- */
/*
 * Copyright 2004,2006,2007,2010,2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "bch3221.h"
#include "flex_parse_impl.h"
#include <gnuradio/io_signature.h>
#include <ctype.h>

namespace gr {
namespace pager {

flex_parse::sptr flex_parse::make(msg_queue::sptr queue, float freq)
{
    return gnuradio::get_initial_sptr(new flex_parse_impl(queue, freq));
}

flex_parse_impl::flex_parse_impl(msg_queue::sptr queue, float freq)
    : sync_block("flex_parse",
                 io_signature::make(1, 1, sizeof(int32_t)),
                 io_signature::make(0, 0, 0)),
      d_freq(freq),
      d_frame(),
      d_queue(queue),
      d_payload(),
      d_datawords(),
      d_count(0)
{
}

flex_parse_impl::~flex_parse_impl() {}

int flex_parse_impl::work(int noutput_items,
                          gr_vector_const_void_star& input_items,
                          gr_vector_void_star& output_items)
{
    const int32_t* in = reinterpret_cast<const int32_t*>(input_items[0]);

    int i = 0;
    while (i < noutput_items) {
        // Accumulate one whole frame's worth of data words (88 of them)
        d_datawords[d_count] = *in++;
        i++;
        if (++d_count == flex_frame::FRAME_WORDS) {
            const std::vector<flex_page>& pages =
                d_frame.parse(d_freq, &d_datawords[0], d_count);
            for (auto&& page : pages) {
                d_payload.str("");
                d_payload << page;
                message::sptr msg =
                    message::make_from_string(std::string(d_payload.str()));
                d_queue->handle(msg);
            }
            d_count = 0;
        }
    }

    return i;
}
} /* namespace pager */
} /* namespace gr */
