cmake_minimum_required(VERSION 3.0.2)

project(SocketW)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  # For some reason Conans libcxx will break the build 
  set(CONAN_LIBCXX "")
  conan_basic_setup(TARGETS)
else()
  find_package(OpenSSL REQUIRED)
endif()

# some versioning things
SET(LIB_MAJOR_VERSION "3")
SET(LIB_MINOR_VERSION "10")
SET(LIB_BUILD_VERSION "26" CACHE STRING "build version")
SET(LIB_VERSION "${LIB_MAJOR_VERSION}.${LIB_MINOR_VERSION}.${LIB_BUILD_VERSION}")
IF (NOT DEFINED LIB_INSTALL_DIR)
    SET(LIB_INSTALL_DIR "lib${LIB_SUFFIX}")
ENDIF (NOT DEFINED LIB_INSTALL_DIR)

file(GLOB sources "src/*.cxx")
file(GLOB headers "src/*.h")

add_library(SocketW ${sources} ${headers})

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
	include_directories(${CONAN_INCLUDE_DIRS_OPENSSL})
	target_link_libraries(SocketW PRIVATE CONAN_PKG::openssl)
else()
	include_directories(${OPENSSL_INCLUDE_DIR})
	target_link_libraries(SocketW PRIVATE OpenSSL::SSL)
endif()

install(TARGETS SocketW DESTINATION lib)
install(DIRECTORY src/ DESTINATION include FILES_MATCHING PATTERN "*.h")

if (UNIX)
    # Detect Linux distribution (if possible)
    execute_process(COMMAND "/usr/bin/lsb_release" "-rs"
            TIMEOUT 4
            OUTPUT_VARIABLE LINUX_VERSION
            ERROR_QUIET
            OUTPUT_STRIP_TRAILING_WHITESPACE)
    message(STATUS "Linux distro is: ${LINUX_VERSION}")
endif ()

# CPack
set(CPACK_PACKAGE_DESCRIPTION "SocketW")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "SocketW is a library which provides cross-platform socket abstraction.")
set(CPACK_PACKAGE_NAME "socketw")
set(CPACK_PACKAGE_CONTACT "Edgar@AnotherFoxGuy.com")
set(CPACK_PACKAGE_VENDOR "Edgar@AnotherFoxGuy.com")
SET(CPACK_PACKAGE_VERSION ${LIB_VERSION})
SET(CPACK_PACKAGE_VERSION_MAJOR ${LIB_MAJOR_VERSION})
SET(CPACK_PACKAGE_VERSION_MINOR ${LIB_MINOR_VERSION})
SET(CPACK_PACKAGE_VERSION_PATCH ${LIB_BUILD_VERSION})
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/README")

SET(CPACK_GENERATOR ZIP)
IF (UNIX)
    SET(CPACK_GENERATOR ${CPACK_GENERATOR};STGZ;TGZ;DEB;RPM)
ENDIF (UNIX)
IF (LINUX)
    SET(CPACK_GENERATOR ${CPACK_GENERATOR};DEB;RPM)
ENDIF (LINUX)
IF (MSVC)
    SET(CPACK_GENERATOR ${CPACK_GENERATOR};NSIS)
ENDIF (MSVC)
IF (APPLE)
    SET(CPACK_GENERATOR ${CPACK_GENERATOR};PackageMaker)
ENDIF (APPLE)
SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${LIB_VERSION}-${CMAKE_SYSTEM_PROCESSOR}")

IF (LINUX_VERSION)
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-${LINUX_VERSION}")
ENDIF ()

include(CPack)
