cmake_minimum_required(VERSION 3.22.0)

project(samplemodule)
set(compiled_module_name _${PROJECT_NAME})

include(FindPackageHandleStandardArgs)

# Libraries and options set by the module builder
set(OPTIMIZE "4")
find_package(PythonExtensions REQUIRED)

# Locate the Panda3D headers
find_path(Panda_INCLUDE_DIR dtoolbase.h PATH_SUFFIXES panda3d)

# Locate the Panda3D libraries
list(APPEND Panda_LIBRARIES)
foreach (lib panda pandaexpress p3dtool p3dtoolconfig p3interrogatedb)
  find_library(Panda_LIBRARY_${lib} ${lib} PATH_SUFFIXES panda3d)
  list(APPEND Panda_LIBRARIES ${Panda_LIBRARY_${lib}})
endforeach()

find_package_handle_standard_args(Panda DEFAULT_MSG Panda_LIBRARIES Panda_INCLUDE_DIR)

# Link panda includes / libraries
include_directories("${Panda_INCLUDE_DIR}")

# Collect sources for compiling
file(GLOB_RECURSE module_sources
  ${PROJECT_NAME}/*.cpp
  ${PROJECT_NAME}/*.cxx
  ${PROJECT_NAME}/*.I
  ${PROJECT_NAME}/*.hpp
  ${PROJECT_NAME}/*.h
  ${PROJECT_NAME}/*.cc
  ${PROJECT_NAME}/*.c
)

set(interrogate_root ${CMAKE_CURRENT_BINARY_DIR}/interrogate)
make_directory(${interrogate_root})

set(interrogate_module_file ${interrogate_root}/interrogate_module.cpp)
set(interrogate_wrapper_file ${interrogate_root}/interrogate_wrapper.cpp)
set(interrogate_interface_file ${interrogate_root}/interrogate.in)

list(APPEND interrogate_sources ${interrogate_module_file} ${interrogate_wrapper_file})

add_custom_command(
  OUTPUT ${interrogate_sources}
  COMMAND interrogate
    ARGS -srcdir ${CMAKE_CURRENT_LIST_DIR}
      -I${Panda_INCLUDE_DIR} -S${Panda_INCLUDE_DIR}/parser-inc
      -python-native -fnames -string -refcount -assert -nomangle
      -module ${compiled_module_name} -library ${compiled_module_name}
      -DINTERROGATE -DCPPPARSER -D__STDC__=1 -D__cplusplus=201103L
      -oc ${interrogate_wrapper_file} -od ${interrogate_interface_file}
      ${module_sources}
  COMMAND interrogate_module
    ARGS
      -python-native
      -import panda3d.core
      -module ${compiled_module_name} -library ${compiled_module_name}
      -oc ${interrogate_module_file}
      ${interrogate_interface_file}
  DEPENDS ${module_sources}
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
)

# Differnt optimization settings
if (OPTIMIZE STREQUAL "1")
  add_definitions("-ggdb -D_DEBUG")
elseif(OPTIMIZE STREQUAL "2")
  add_definitions("-O1 -D_DEBUG")
elseif(OPTIMIZE STREQUAL "3")
  add_definitions("-O2")
  add_definitions("-fno-finite-math-only -ffast-math")
elseif(OPTIMIZE STREQUAL "4")
  add_definitions("-O3 -DNDEBUG -ffast-math -fno-rtti")
else()
  message(FATAL_ERROR "Invalid optimize value! Was: '${OPTIMIZE}'")
endif()

# Define the module name
add_definitions("/DPB_MODULE=${compiled_module_name}")
add_definitions("/DPB_CFG_MODULE=${compiled_module_name}")

add_library(${compiled_module_name} MODULE ${module_sources} ${interrogate_sources})
python_extension_module(${compiled_module_name})

# Add the required libraries
target_link_libraries(${compiled_module_name} ${Panda_LIBRARIES})

# [LIB] Eigen 3
find_package (Eigen3 3.3 REQUIRED)
target_link_libraries(${compiled_module_name} Eigen3::Eigen)
# Eigen build flags (sync with Panda)
add_definitions("/DEIGEN_MPL2_ONLY=")
if ((OPTIMIZE STREQUAL "3") OR (OPTIMIZE STREQUAL "4"))
  add_definitions("/DEIGEN_NO_DEBUG=")
endif()

install(TARGETS ${compiled_module_name} LIBRARY DESTINATION ${PROJECT_NAME})
