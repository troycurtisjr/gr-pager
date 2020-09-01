/* -*- c++ -*- */
/*
 * Copyright 2006,2012 Free Software Foundation, Inc.
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

#ifndef INCLUDED_PAGER_FLEX_PARSE_IMPL_H
#define INCLUDED_PAGER_FLEX_PARSE_IMPL_H

#include <pager/flex_parse.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/msg_queue.h>
#include "flex_modes.h"
#include "flex_frame.h"
#include <sstream>

namespace gr {
  namespace pager {

    class flex_parse_impl : public flex_parse
    {
    private:
      float d_freq;
      flex_frame d_frame;
      msg_queue::sptr d_queue;		  // Destination for decoded pages

      std::ostringstream d_payload;
      int d_datawords[88];                // 11 blocks of 8 32-bit words
      int d_count;                        // Count of received codewords

    public:
      flex_parse_impl(msg_queue::sptr queue, float freq);
      ~flex_parse_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } /* namespace pager */
} /* namespace gr */

#endif /* INCLUDED_PAGER_FLEX_PARSE_IMPL_H */
