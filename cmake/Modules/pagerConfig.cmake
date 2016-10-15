INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PAGER pager)

FIND_PATH(
    PAGER_INCLUDE_DIRS
    NAMES pager/api.h
    HINTS $ENV{PAGER_DIR}/include
        ${PC_PAGER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PAGER_LIBRARIES
    NAMES gnuradio-pager
    HINTS $ENV{PAGER_DIR}/lib
        ${PC_PAGER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PAGER DEFAULT_MSG PAGER_LIBRARIES PAGER_INCLUDE_DIRS)
MARK_AS_ADVANCED(PAGER_LIBRARIES PAGER_INCLUDE_DIRS)

