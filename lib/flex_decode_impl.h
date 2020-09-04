/* -*- c++ -*- */
/*
 * Copyright 2020 Troy Curtis, Jr..
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

#ifndef INCLUDED_PAGER_FLEX_DECODE_IMPL_H
#define INCLUDED_PAGER_FLEX_DECODE_IMPL_H

#include "flex_frame.h"
#include <pager/flex_decode.h>

namespace gr {
namespace pager {

class flex_decode_impl : public flex_decode
{
private:
    float d_freq;
    flex_frame d_frame;

    std::ostringstream d_payload;
    int d_datawords[88]; // 11 blocks of 8 32-bit words
    int d_count;         // Count of received codewords
    pmt::pmt_t d_outport;

public:
    flex_decode_impl(float freq);
    ~flex_decode_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace pager
} // namespace gr

#endif /* INCLUDED_PAGER_FLEX_DECODE_IMPL_H */
