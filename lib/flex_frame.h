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

#ifndef INCLUDED_PAGER_FLEX_FRAME_H
#define INCLUDED_PAGER_FLEX_FRAME_H

#include "flex_modes.h"
#include <iosfwd>
#include <vector>

namespace gr {
namespace pager {
/* Simple data container for a single page. */
class flex_page
{
public:
    static const char FIELD_DELIM = 128;

    flex_page();

    float freq;
    page_type_t type;
    int capcode;
    bool laddr;
    int data_len;
    char data[84 * 3]; // Probably overkill, but definitely safe.
};
std::ostream& operator<<(std::ostream& out, const flex_page& page);

class flex_frame
{
private:
    std::vector<flex_page> d_pages;

    int parse_capcode(int* laddr, int32_t aw1, int32_t aw2);
    void
    parse_alphanumeric(flex_page* page, const int32_t* frame, int mw1, int mw2, int j);
    void parse_numeric(flex_page* page, const int32_t* frame, int mw1, int mw2, int j);
    void parse_tone_only();
    void parse_unknown(flex_page* page, const int32_t* frame, int mw1, int mw2);

public:
    static const int FRAME_WORDS = 88;

    flex_frame();
    ~flex_frame();
    /*
     * Handle a frame's worth of data which can produce zero or more pages.
     */
    const std::vector<flex_page>&
    parse(const float freq, const int32_t* frame, const int size);
};

} /* namespace pager */
} /* namespace gr */


#endif /* INCLUDED_PAGER_FLEX_FRAME_IMPL_H */
