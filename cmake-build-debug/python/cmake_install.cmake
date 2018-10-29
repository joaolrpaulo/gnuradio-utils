# Install script for directory: /home/joaopaulo/coding/fac/gnuradio-utils/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/pkt" TYPE FILE FILES
    "/home/joaopaulo/coding/fac/gnuradio-utils/python/__init__.py"
    "/home/joaopaulo/coding/fac/gnuradio-utils/python/packet.py"
    "/home/joaopaulo/coding/fac/gnuradio-utils/python/timestamp_generator.py"
    "/home/joaopaulo/coding/fac/gnuradio-utils/python/timestamp_decoder.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/pkt" TYPE FILE FILES
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/__init__.pyc"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/packet.pyc"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/timestamp_generator.pyc"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/timestamp_decoder.pyc"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/__init__.pyo"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/packet.pyo"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/timestamp_generator.pyo"
    "/home/joaopaulo/coding/fac/gnuradio-utils/cmake-build-debug/python/timestamp_decoder.pyo"
    )
endif()

