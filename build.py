from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.build_policy = "missing"
    builder.add_common_builds()
    builder.run()
