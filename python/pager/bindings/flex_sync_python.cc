/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(flex_sync.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(8d372c017e326895af66f348e98507da)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/pager/flex_sync.h>
// pydoc.h is automatically generated in the build directory
#include <flex_sync_pydoc.h>

void bind_flex_sync(py::module& m)
{

    using flex_sync    = ::gr::pager::flex_sync;


    py::class_<flex_sync, gr::block, gr::basic_block,
        std::shared_ptr<flex_sync>>(m, "flex_sync", D(flex_sync))

        .def(py::init(&flex_sync::make),
           D(flex_sync,make)
        )
        



        ;




}








