#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class NanopbConan(ConanFile):
    name = "nanopb"
    version = "0.3.9.1"
    description = "Protocol Buffers for Embedded Systems"
    url = "https://github.com/k0ekk0ek/conan-nanopb"
    homepage = "https://jpa.kapsi.fi/nanopb/"
    license = "zlib"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "no_debug_postfix.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'enable_malloc': [True, False]
    }
    default_options = (
        'shared=False',
        'fPIC=True',
        'enable_malloc=True'
    )

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    build_requires = 'protobuf/3.5.2@bincrafters/stable'

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/nanopb/nanopb"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        tools.patch(patch_file='no_debug_postfix.patch')
        cmake = CMake(self)
        cmake.definitions['ENABLE_MALLOC'] = self.options.enable_malloc
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="pb.h", dst="include", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="pb_common.h", dst="include", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="pb_encode.h", dst="include", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="pb_decode.h", dst="include", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="*/nanopb_pb2.py", dst="lib/python2.7/site-packages", keep_path=False)
        self.copy(pattern="*/plugin_pb2.py", dst="lib/python2.7/site-packages", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
