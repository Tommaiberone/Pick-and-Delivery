# Install script for directory: /home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/Pick_and_Delivery/msg" TYPE FILE FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/Pick_and_Delivery/cmake" TYPE FILE FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/Pick_and_Delivery-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/include/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/share/roseus/ros/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/share/common-lisp/ros/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/share/gennodejs/ros/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/lib/python2.7/dist-packages/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/devel/lib/python2.7/dist-packages/Pick_and_Delivery")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/Pick_and_Delivery.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/Pick_and_Delivery/cmake" TYPE FILE FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/Pick_and_Delivery-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/Pick_and_Delivery/cmake" TYPE FILE FILES
    "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/Pick_and_DeliveryConfig.cmake"
    "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/Pick_and_DeliveryConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/Pick_and_Delivery" TYPE FILE FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/Pick_and_Delivery" TYPE PROGRAM FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/server_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/Pick_and_Delivery" TYPE PROGRAM FILES "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/build/Pick_and_Delivery/catkin_generated/installspace/set_goal.py")
endif()

