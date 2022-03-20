#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio PAGER module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the pager namespace
try:
    # this might fail if the module is python-only
    from .pager_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
#
from .flex_demod import flex_demod
from .pager_utils import *
from .flex_receiver import flex_receiver
from .msg_table import msg_table
