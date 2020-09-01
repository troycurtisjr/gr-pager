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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "flex_frame.h"
#include <iostream>
#include <iomanip>

namespace gr {
namespace pager {

flex_page::flex_page():
  freq(0),
  type(),
  capcode(0),
  laddr(false),
  data_len(0),
  data()
{}

flex_frame::flex_frame()
  : d_pages() {}

flex_frame::~flex_frame() {}

/*
  FLEX data frames (that is, 88 data words per phase recovered
  after sync, symbol decoding, dephasing, deinterleaving, error
  correction, and conversion from codewords to data words) start
  with a block information word containing indices of the page
  address field and page vector fields.

  +-------------+---------+--------+---------+--------+
  | Block       | Address | Vector | Message | Idle   |
  | Information | Field   | Field  | Data    | Code   |
  | Word        |         |        | Field   | Words  |
  +-------------+---------+--------+---------+--------+

  BIW: 1 Code word with indices for Address Field & Vector Field
  Address Field: One or more pager addresses
  Vector Field: Message Type & Content Location Description
  Message Data Field: Message data
  Idle CodeWords; Filler for the remainder of frame
*/
int flex_frame::parse_capcode(int *laddr, int aw1, int aw2) {
  *laddr = (aw1 < 0x008001L) || (aw1 > 0x1E0000L) || (aw1 > 0x1E7FFEL);

  if (*laddr)
    return aw1 + ((aw2 ^ 0x001FFFFF) << 15) + 0x1F9000; // Don't ask
  else
    return aw1 - 0x8000;
}

const std::vector<flex_page>& flex_frame::parse(const float freq, const int32_t *frame, const int size) {
  d_pages.clear();

  if (size != FRAME_WORDS)
    return d_pages;
  // Block information word is the first data word in frame
  int biw = frame[0];

  // Nothing to see here, please move along
  if (biw == 0 || biw == 0x001FFFFF)
    return d_pages;

  // Vector start index is bits 15-10
  // Address start address is bits 9-8, plus one for offset
  int voffset = (biw >> 10) & 0x3f;
  int aoffset = ((biw >> 8) & 0x03) + 1;

  // printf("BIW:%08X AW:%02i-%02i\n", biw, aoffset, voffset);

  // Iterate through pages and dispatch to appropriate handler
  for (int i = aoffset; i < voffset; i++) {
    int j = voffset + i - aoffset; // Start of vector field for address @ i

    if (frame[i] == 0x00000000 || frame[i] == 0x001FFFFF)
      continue; // Idle codewords, invalid address

    int laddr;
    const int capcode = parse_capcode(&laddr, frame[i], frame[i + 1]);
    if (laddr)
      i++;

    if (capcode < 0) // Invalid address, skip
      continue;

    // Parse vector information word for address @ offset 'i'
    int viw = frame[j];
    const page_type_t page_type = (page_type_t)((viw >> 4) & 0x00000007);
    int mw1 = (viw >> 7) & 0x00000007F;
    int len = (viw >> 14) & 0x0000007F;

    if (is_numeric_page(page_type))
      len &= 0x07;
    int mw2 = mw1 + len;

    if (mw1 == 0 && mw2 == 0)
      continue; // Invalid VIW

    if (is_tone_page(page_type))
      mw1 = mw2 = 0;

    if (mw1 > 87 || mw2 > 87)
      continue; // Invalid offsets

    d_pages.resize(d_pages.size() + 1);
    flex_page &page = d_pages.back();
    page.freq = freq;
    page.type = page_type;
    page.capcode = capcode;
    page.laddr = laddr;

    if (is_alphanumeric_page(page_type))
      parse_alphanumeric(&page, frame, mw1, mw2 - 1, j);
    else if (is_numeric_page(page_type))
      parse_numeric(&page, frame, mw1, mw2, j);
    else if (is_tone_page(page_type))
      parse_tone_only();
    else
      parse_unknown(&page, frame, mw1, mw2);
  }

  return d_pages;
}

static char *add_alpha(char *data, int dw) {
  *data = dw & 0x7F;
  // 0x03 is a fill character, don't include in the output.
  return *data != 0x03 ? data + 1 : data;
}

void flex_frame::parse_alphanumeric(flex_page *page, const int32_t *frame,
                                    int mw1, int mw2, int j) {
  int frag;
  // bool cont;

  if (!page->laddr) {
    frag = (frame[mw1] >> 11) & 0x03;
    // cont = (frame[mw1] >> 10) & 0x01;
    mw1++;
  } else {
    frag = (frame[j + 1] >> 11) & 0x03;
    // cont = (frame[j+1] >> 10) & 0x01;
    mw2--;
  }

  char *w_ptr = &(page->data[0]);
  for (int i = mw1; i <= mw2; i++) {
    int dw = frame[i];

    if (i > mw1 || frag != 0x03) {
      w_ptr = add_alpha(w_ptr, dw);
    }
    w_ptr = add_alpha(w_ptr, (dw >> 7));
    w_ptr = add_alpha(w_ptr, (dw >> 14));
  }

  page->data_len = w_ptr - &(page->data[0]);
}

void flex_frame::parse_numeric(flex_page *page, const int *frame, int mw1, int mw2, int j) {
  // Get first dataword from message field or from second
  // vector word if long address
  int dw;
  if (!page->laddr) {
    dw = frame[mw1];
    mw1++;
    mw2++;
  } else {
    dw = frame[j + 1];
  }

  char digit = 0;
  int count = 4;
  if (page->type == FLEX_NUMBERED_NUMERIC)
    count += 10; // Skip 10 header bits for numbered numeric pages
  else
    count += 2; // Otherwise skip 2

  char *w_ptr = &(page->data[0]);
  for (int i = mw1; i <= mw2; i++) {
    for (int k = 0; k < 21; k++) {
      // Shift LSB from data word into digit
      digit = (digit >> 1) & 0x0F;
      if (dw & 0x01)
        digit ^= 0x08;
      dw >>= 1;
      if (--count == 0) {
        if (digit != 0x0C) // Fill
          *w_ptr++ = flex_bcd[digit];
        count = 4;
      }
    }

    dw = frame[i];
  }

  page->data_len = w_ptr - &(page->data[0]);
}

void flex_frame::parse_tone_only() {}

void flex_frame::parse_unknown(flex_page *page, const int32_t *frame, int mw1, int mw2) {}

std::ostream &operator<<(std::ostream &out, const flex_page &page)
{
  out << std::showpoint << std::setprecision(6) << std::setw(7)
      << page.freq / 1e6 << flex_page::FIELD_DELIM
      << std::setw(10) << page.capcode << flex_page::FIELD_DELIM
      << flex_page_desc[page.type] << flex_page::FIELD_DELIM
      << std::string(&(page.data[0]), page.data_len);
  return out;
}

} /* namespace pager */
} /* namespace gr */
