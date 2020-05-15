from conans import ConanFile, CMake, tools


class SocketwConan(ConanFile):
    name = "SocketW"
    version = "3.10.36"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/socketw/issues"
    description = "SocketW is a library which provides cross-platform socket abstraction"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "LICENSE", "README"


    def requirements(self):
        self.requires.add('openssl/1.1.1g')

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
