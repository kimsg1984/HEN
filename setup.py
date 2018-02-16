#!/usr/bin/env python

import os
import sys
from distutils.core import setup

sys.path.append(os.path.realpath("src"))

setup(name = "hen",
        version = "0.1",
        description = "PyQt Wiki-Wiki Text Editor",
        long_description = "Python port of Wiki-Wiki texteditor.",
        author = "SunGyo Kim",
        author_email = "kimsg1984@gmail.com",
        license = "GNU GPLv3",
        url = "",
        packages = ["hen "],
        package_dir = {"": "src"},
        scripts = ["hen "],
        requires = ["PyQt4"],
        platforms = ["Linux", "Windows", "OSX"]
        )