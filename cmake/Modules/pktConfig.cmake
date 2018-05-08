INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PKT pkt)

FIND_PATH(
    PKT_INCLUDE_DIRS
    NAMES pkt/api.h
    HINTS $ENV{PKT_DIR}/include
        ${PC_PKT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PKT_LIBRARIES
    NAMES gnuradio-pkt
    HINTS $ENV{PKT_DIR}/lib
        ${PC_PKT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PKT DEFAULT_MSG PKT_LIBRARIES PKT_INCLUDE_DIRS)
MARK_AS_ADVANCED(PKT_LIBRARIES PKT_INCLUDE_DIRS)

