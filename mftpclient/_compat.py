#!/usr/bin/env python3
"""
Compatibility module 
"""
from codecs import ignore_errors
import sys
import platform
import subprocess

IS_PY3 = sys.version_info[0] == 3
SUPPORTED_SYSTEMS = ["Linux"]

def _get_linux_kernel_version():
    cmd_result, _ = subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE).communicate()
    return str(cmd_result).replace("'", "").replace("b", "")

def _compare_kernel_version(this_version, other_version):
    this_to_array, other_to_array = this_version.split('.')[:2], other_version.split('.')[:2]
    min_length = min(len(this_to_array), len(other_to_array))
    for idx in range(min_length):
        this_to_number = int(this_to_array[idx])
        other_to_number = int(other_to_array[idx])
        if  this_to_number < other_to_number:
            return -1
        elif this_to_number > other_to_number:
            return 1
    return 0

def is_mptcp_supported_on_sytem():
    if platform.system() != "Linux":
        return False
    kernel_version = _get_linux_kernel_version()
    if _compare_kernel_version(kernel_version, "5.6") < 0:
        return False
    return True
