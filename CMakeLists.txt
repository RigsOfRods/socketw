cmake_minimum_required(VERSION 3.0.2)

# Required for conan
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_BINARY_DIR})

project(
        SocketW
        HOMEPAGE_URL http://rigsofrods.github.io/socketw/
        DESCRIPTION "SocketW is a library which provides cross-platform socket abstraction "
        VERSION 3.10.27
)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

SET(CMAKEFILES_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/SocketW")

find_package(OpenSSL)

set(_HAVE_SSL ${OpenSSL_FOUND})
configure_file("${CMAKE_SOURCE_DIR}/src/sw_config.h.in" "${CMAKE_SOURCE_DIR}/src/sw_config.h")

file(GLOB sources "src/*.cxx")
file(GLOB headers "src/*.h")

add_library(${CMAKE_PROJECT_NAME} ${sources} ${headers})

if (OpenSSL_FOUND)
    include_directories(${OPENSSL_INCLUDE_DIR})
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE OpenSSL::SSL)
endif ()

target_include_directories(
        ${CMAKE_PROJECT_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/src>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

# install the library
install(
        TARGETS ${CMAKE_PROJECT_NAME}
        EXPORT SocketWTargets
        RUNTIME LIBRARY ARCHIVE
)

install(
        EXPORT SocketWTargets
        FILE SocketWTargets.cmake
        NAMESPACE SocketW::
        DESTINATION ${CMAKEFILES_INSTALL_DIR}
)

install(DIRECTORY src/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR} FILES_MATCHING PATTERN "*.h")

if (UNIX)
    # Detect Linux distribution (if possible)
    execute_process(COMMAND "/usr/bin/lsb_release" "-rs"
            TIMEOUT 4
            OUTPUT_VARIABLE LINUX_VERSION
            ERROR_QUIET
            OUTPUT_STRIP_TRAILING_WHITESPACE)
    message(STATUS "Linux distro is: ${LINUX_VERSION}")
endif ()

# install the PkgConfig file
configure_file("${CMAKE_SOURCE_DIR}/SocketW.pc.in" "${CMAKE_BINARY_DIR}/SocketW.pc" @ONLY)
install(FILES "${CMAKE_BINARY_DIR}/SocketW.pc" DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig")

configure_package_config_file(
        SocketWConfig.cmake.in
        ${CMAKE_BINARY_DIR}/SocketWConfig.cmake
        INSTALL_DESTINATION ${CMAKEFILES_INSTALL_DIR}
)

write_basic_package_version_file(
        ${CMAKE_BINARY_DIR}/SocketWConfigVersion.cmake
        VERSION "${CMAKE_PROJECT_VERSION}"
        COMPATIBILITY SameMajorVersion
)

install(
        FILES ${CMAKE_BINARY_DIR}/SocketWConfig.cmake
        ${CMAKE_BINARY_DIR}/SocketWConfigVersion.cmake
        DESTINATION ${CMAKEFILES_INSTALL_DIR}
)