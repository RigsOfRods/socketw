
cmake_minimum_required ( VERSION 2.8.12 )

project( SocketW )

set( SOURCES
  src/sw_base.cxx
  src/sw_inet.cxx
  src/sw_ssl.cxx
  src/sw_unix.cxx
)

add_library( SocketW ${SOURCES} )

install( TARGETS SocketW DESTINATION lib )
install(DIRECTORY src/ DESTINATION include FILES_MATCHING PATTERN "*.h")
