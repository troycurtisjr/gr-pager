/* -*- c++ -*- */

#define PAGER_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "pager_swig_doc.i"

%{
#include "pager/flex_frame.h"
#include "pager/slicer_fb.h"
#include "pager/flex_sync.h"
#include "pager/flex_deinterleave.h"
#include "pager/flex_parse.h"
%}

%include "pager/flex_frame.h"
%include "pager/slicer_fb.h"
%include "pager/flex_sync.h"
%include "pager/flex_deinterleave.h"
%include "pager/flex_parse.h"

GR_SWIG_BLOCK_MAGIC2(pager, flex_frame);
GR_SWIG_BLOCK_MAGIC2(pager, slicer_fb);
GR_SWIG_BLOCK_MAGIC2(pager, flex_sync);
GR_SWIG_BLOCK_MAGIC2(pager, flex_deinterleave);
GR_SWIG_BLOCK_MAGIC2(pager, flex_parse);
