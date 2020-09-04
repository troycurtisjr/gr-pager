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

#ifndef INCLUDED_PAGER_FLEX_DECODE_H
#define INCLUDED_PAGER_FLEX_DECODE_H

#include <gnuradio/sync_block.h>
#include <pager/api.h>

namespace gr {
namespace pager {

/*!
 * \brief Decodes a stream of codes into messages.
 * \ingroup pager
 *
 */
class PAGER_API flex_decode : virtual public gr::sync_block
{
public:
    // gr::pager::flex_decode::sptr
    typedef boost::shared_ptr<flex_decode> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of pager::flex_decode.
     */
    static sptr make(float freq);
};

} // namespace pager
} // namespace gr

#endif /* INCLUDED_PAGER_FLEX_DECODE_H */
