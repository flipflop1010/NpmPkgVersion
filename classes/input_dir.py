import os
import json
from .flip_sqlite import *


class InputDir:
    def print_input_file(self):
        path = "inputs"
        dir_lists = os.listdir(path)
        sql_obj = FlipSqlite.get_instance()
        # print("Files and directories in '", path, "' :")

        # prints all files
        for dir_list in dir_lists:
            fp = "inputs/" + dir_list
            # print(fp)
            f = open(fp, "r")
            data = json.load(f)
            devDependencies = data["devDependencies"]
            for key in devDependencies:
                ver = devDependencies[key]
                if ver.startswith("^"):
                    ver = ver[1:]
                # print(key,ver)
                sql_obj.update_npm_package(key, ver, "devDependencies")
            # for dependencies
            dependencies = data["dependencies"]
            for key in dependencies:
                ver = dependencies[key]
                if ver.startswith("^"):
                    ver = ver[1:]
                # print(key,ver)
                sql_obj.update_npm_package(key, ver, "dependencies")


# a = InputDir()

# a.print_input_file()
