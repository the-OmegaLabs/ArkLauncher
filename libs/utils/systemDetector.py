# Copyright 2025 Omega Labs, ArkLauncher Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import platform
import re
import subprocess
import sys


def get_linux_version():
    os_version = 0
    verbose_version = "Unknown Linux Distribution"
    version_id = None
    distro_name = "Linux"

    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release", "r") as f:
            os_release = {}
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    os_release[key] = value.strip('"')

        distro_name = os_release.get("NAME", distro_name)
        version_id = os_release.get("VERSION_ID", "")
        verbose_version = os_release.get("PRETTY_NAME", verbose_version)

    if not version_id:
        for release_file in ["/etc/redhat-release", "/etc/centos-release",
                             "/etc/lsb-release", "/etc/debian_version"]:
            if os.path.exists(release_file):
                with open(release_file, "r") as f:
                    content = f.read().strip()
                    match = re.search(r'\d+\.?\d*', content)
                    if match:
                        version_id = match.group(0)
                        verbose_version = f"{distro_name} {content}"
                    break

    if not version_id:
        try:
            output = subprocess.check_output(["lsb_release", "-sr"], stderr=subprocess.DEVNULL)
            version_id = output.decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    if version_id:
        try:
            if version_id.lower() == "rolling":
                return (0, f"{distro_name} (rolling release)")

            main_version = version_id.split('.')[0]
            os_version = int(main_version)
        except ValueError:
            pass

    return (os_version, verbose_version)


def get_windows_version():
    win_version = 0
    verbose = "Unknown Windows Version"

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )

        product_name = winreg.QueryValueEx(key, "ProductName")[0]
        current_build = winreg.QueryValueEx(key, "CurrentBuild")[0]
        release_id = winreg.QueryValueEx(key, "ReleaseId")[0] if "ReleaseId" in \
                                                                 winreg.QueryValueEx(key, "ReleaseId") else ""
        winreg.CloseKey(key)

        if int(current_build) >= 22000:
            win_version = 11
            verbose = product_name.replace("Microsoft ", "")
        else:
            version_map = {
                "10": 10,
                "8.1": 8,
                "8": 8,
                "7": 7,
                "Vista": 6,
                "XP": 5
            }
            for key in version_map:
                if key in product_name:
                    win_version = version_map[key]
                    break
            verbose = product_name.replace("Microsoft ", "")

    except Exception as e:
        win_ver = sys.getwindowsversion()
        build_number = win_ver.build
        if build_number >= 22000:
            win_version = 11
            verbose = f"Windows 11 (Build {build_number})"
        elif win_ver.major == 10:
            win_version = 10
            verbose = f"Windows 10 (Build {build_number})"
        elif win_ver.major == 6:
            win_version = {1: 7, 2: 8, 3: 8}.get(win_ver.minor, 0)

    return (win_version, verbose)


def get_macos_version():
    try:
        sw_vers = subprocess.check_output(["sw_vers", "-productVersion"]).decode().strip()
        os_version = int(sw_vers.split('.')[0])
        build_version = subprocess.check_output(["sw_vers", "-buildVersion"]).decode().strip()
        verbose = f"macOS {sw_vers} ({build_version})"

        version_names = {
            13: "Ventura",
            12: "Monterey",
            11: "Big Sur",
            10: {
                15: "Catalina",
                14: "Mojave",
                13: "High Sierra"
            }
        }

        if os_version >= 11:
            verbose = f"macOS {version_names.get(os_version, '')} {sw_vers}"
        elif os_version == 10:
            minor_version = int(sw_vers.split('.')[1])
            verbose = f"macOS {version_names[10].get(minor_version, '')} {sw_vers}"

    except Exception as e:
        os_version = 0
        verbose = "macOS Unknown Version"

    return (os_version, verbose)


def detect_system():
    system = platform.system()
    result = ["Unknown", 0, "Unknown Operating System"]

    try:
        if system == "Linux":
            os_version, verbose = get_linux_version()
            result = ["Linux", os_version, verbose]

        elif system == "Windows":
            os_version, verbose = get_windows_version()
            result = ["Windows", os_version, verbose]

        elif system == "Darwin":
            os_version, verbose = get_macos_version()
            result = ["macOS", os_version, verbose]

        else:
            result[0] = system
            if system == "FreeBSD":
                version = os.popen("freebsd-version").read().strip()
                try:
                    result[1] = int(version.split('-')[0].split('.')[0])
                    result[2] = f"FreeBSD {version}"
                except:
                    pass
            elif system == "SunOS":
                output = os.popen("uname -v").read().strip()
                result[2] = f"Solaris {output}"
                try:
                    result[1] = int(re.search(r'\d+', output).group())
                except:
                    pass

    except Exception as e:
        pass

    return result


if __name__ == "__main__":
    print(detect_system())
