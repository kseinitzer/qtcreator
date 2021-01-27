from conans import ConanFile, tools
import os


class QtCreatorConan(ConanFile):
    name = "qtcreator"
    version = "4.12.0"
    license = "GPL"
    author = "Qt"
    description = "IDE"
    settings = "os", "compiler", "build_type", "arch"
    generators = "qmake"
    requires = "qt/5.15.1@bincrafters/stable"
    exports_sources = "creator*"

    scm = {
        "type": "git",
        "subfolder": "creator",
        "url": "https://github.com/qt-creator/qt-creator.git",
        "revision": "v4.14.0"
    }

    def build(self):
        self.run(f"qmake {self.source_folder}/creator", run_environment=True)
        if self.settings.build_os == "Windows":
            with tools.vcvars(self):
                self.run("nmake")
        else:
            self.run("make -j 6")

    def configure(self):
        self.options["qt"].qtdeclarative = True
        self.options["qt"].qttools = True
        self.options["qt"].qtsvg = True

    def package(self):
        self.copy("bin/qtcreator*", keep_path=True)
        self.copy("lib/**", keep_path=True)
        self.copy("libexec/**", keep_path=True)

    def package_info(self):
        self.cpp_info.srcdirs = ["creator"]
        self.env_info.QTC_SOURCE = os.path.join(self.source_folder, "creator")
        print(f"QTC SOURCE: {self.env_info.QTC_SOURCE}")
        self.env_info.IDE_BUILD_TREE = self.package_folder


