#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "libnyquist" for configuration "Release"
set_property(TARGET libnyquist APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(libnyquist PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C;CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnyquist.lib"
  )

list(APPEND _cmake_import_check_targets libnyquist )
list(APPEND _cmake_import_check_files_for_libnyquist "${_IMPORT_PREFIX}/lib/libnyquist.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
