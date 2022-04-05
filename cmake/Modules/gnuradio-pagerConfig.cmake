find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_PAGER gnuradio-pager)

FIND_PATH(
    GR_PAGER_INCLUDE_DIRS
    NAMES gnuradio/pager/api.h
    HINTS $ENV{PAGER_DIR}/include
        ${PC_PAGER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_PAGER_LIBRARIES
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

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-pagerTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_PAGER DEFAULT_MSG GR_PAGER_LIBRARIES GR_PAGER_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_PAGER_LIBRARIES GR_PAGER_INCLUDE_DIRS)
