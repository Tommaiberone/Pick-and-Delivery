# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "Pick_and_Delivery: 1 messages, 0 services")

set(MSG_I_FLAGS "-IPick_and_Delivery:/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Itf2_msgs:/opt/ros/melodic/share/tf2_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/melodic/share/sensor_msgs/cmake/../msg;-Inav_msgs:/opt/ros/melodic/share/nav_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(Pick_and_Delivery_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_custom_target(_Pick_and_Delivery_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "Pick_and_Delivery" "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(Pick_and_Delivery
  "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Pick_and_Delivery
)

### Generating Services

### Generating Module File
_generate_module_cpp(Pick_and_Delivery
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Pick_and_Delivery
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(Pick_and_Delivery_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(Pick_and_Delivery_generate_messages Pick_and_Delivery_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_dependencies(Pick_and_Delivery_generate_messages_cpp _Pick_and_Delivery_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Pick_and_Delivery_gencpp)
add_dependencies(Pick_and_Delivery_gencpp Pick_and_Delivery_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Pick_and_Delivery_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(Pick_and_Delivery
  "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Pick_and_Delivery
)

### Generating Services

### Generating Module File
_generate_module_eus(Pick_and_Delivery
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Pick_and_Delivery
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(Pick_and_Delivery_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(Pick_and_Delivery_generate_messages Pick_and_Delivery_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_dependencies(Pick_and_Delivery_generate_messages_eus _Pick_and_Delivery_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Pick_and_Delivery_geneus)
add_dependencies(Pick_and_Delivery_geneus Pick_and_Delivery_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Pick_and_Delivery_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(Pick_and_Delivery
  "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Pick_and_Delivery
)

### Generating Services

### Generating Module File
_generate_module_lisp(Pick_and_Delivery
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Pick_and_Delivery
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(Pick_and_Delivery_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(Pick_and_Delivery_generate_messages Pick_and_Delivery_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_dependencies(Pick_and_Delivery_generate_messages_lisp _Pick_and_Delivery_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Pick_and_Delivery_genlisp)
add_dependencies(Pick_and_Delivery_genlisp Pick_and_Delivery_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Pick_and_Delivery_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(Pick_and_Delivery
  "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Pick_and_Delivery
)

### Generating Services

### Generating Module File
_generate_module_nodejs(Pick_and_Delivery
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Pick_and_Delivery
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(Pick_and_Delivery_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(Pick_and_Delivery_generate_messages Pick_and_Delivery_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_dependencies(Pick_and_Delivery_generate_messages_nodejs _Pick_and_Delivery_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Pick_and_Delivery_gennodejs)
add_dependencies(Pick_and_Delivery_gennodejs Pick_and_Delivery_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Pick_and_Delivery_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(Pick_and_Delivery
  "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Pick_and_Delivery
)

### Generating Services

### Generating Module File
_generate_module_py(Pick_and_Delivery
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Pick_and_Delivery
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(Pick_and_Delivery_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(Pick_and_Delivery_generate_messages Pick_and_Delivery_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/me/Desktop/labiagi_2020_21/workspaces/Pick-and-Delivery/src/Pick_and_Delivery/msg/NewGoal.msg" NAME_WE)
add_dependencies(Pick_and_Delivery_generate_messages_py _Pick_and_Delivery_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Pick_and_Delivery_genpy)
add_dependencies(Pick_and_Delivery_genpy Pick_and_Delivery_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Pick_and_Delivery_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Pick_and_Delivery)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Pick_and_Delivery
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(Pick_and_Delivery_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(Pick_and_Delivery_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET tf2_msgs_generate_messages_cpp)
  add_dependencies(Pick_and_Delivery_generate_messages_cpp tf2_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(Pick_and_Delivery_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()
if(TARGET nav_msgs_generate_messages_cpp)
  add_dependencies(Pick_and_Delivery_generate_messages_cpp nav_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Pick_and_Delivery)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Pick_and_Delivery
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(Pick_and_Delivery_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(Pick_and_Delivery_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET tf2_msgs_generate_messages_eus)
  add_dependencies(Pick_and_Delivery_generate_messages_eus tf2_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(Pick_and_Delivery_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()
if(TARGET nav_msgs_generate_messages_eus)
  add_dependencies(Pick_and_Delivery_generate_messages_eus nav_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Pick_and_Delivery)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Pick_and_Delivery
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(Pick_and_Delivery_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(Pick_and_Delivery_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET tf2_msgs_generate_messages_lisp)
  add_dependencies(Pick_and_Delivery_generate_messages_lisp tf2_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(Pick_and_Delivery_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()
if(TARGET nav_msgs_generate_messages_lisp)
  add_dependencies(Pick_and_Delivery_generate_messages_lisp nav_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Pick_and_Delivery)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Pick_and_Delivery
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(Pick_and_Delivery_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(Pick_and_Delivery_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET tf2_msgs_generate_messages_nodejs)
  add_dependencies(Pick_and_Delivery_generate_messages_nodejs tf2_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(Pick_and_Delivery_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()
if(TARGET nav_msgs_generate_messages_nodejs)
  add_dependencies(Pick_and_Delivery_generate_messages_nodejs nav_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Pick_and_Delivery)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Pick_and_Delivery\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Pick_and_Delivery
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(Pick_and_Delivery_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(Pick_and_Delivery_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET tf2_msgs_generate_messages_py)
  add_dependencies(Pick_and_Delivery_generate_messages_py tf2_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(Pick_and_Delivery_generate_messages_py sensor_msgs_generate_messages_py)
endif()
if(TARGET nav_msgs_generate_messages_py)
  add_dependencies(Pick_and_Delivery_generate_messages_py nav_msgs_generate_messages_py)
endif()
