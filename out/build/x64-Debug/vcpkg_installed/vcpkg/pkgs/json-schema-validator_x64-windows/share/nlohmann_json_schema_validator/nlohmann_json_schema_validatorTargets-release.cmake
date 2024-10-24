#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nlohmann_json_schema_validator" for configuration "Release"
set_property(TARGET nlohmann_json_schema_validator APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nlohmann_json_schema_validator PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/nlohmann_json_schema_validator.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/nlohmann_json_schema_validator.dll"
  )

list(APPEND _cmake_import_check_targets nlohmann_json_schema_validator )
list(APPEND _cmake_import_check_files_for_nlohmann_json_schema_validator "${_IMPORT_PREFIX}/lib/nlohmann_json_schema_validator.lib" "${_IMPORT_PREFIX}/bin/nlohmann_json_schema_validator.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
