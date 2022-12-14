#!/usr/bin/env python3
#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the
# 'License'.)  You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN \'AS IS\' BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Usage:
    patcher.py (generate | patch) [--clean | --verbose]

Arguments:
    generate    Generate patch files
    patch       Apply patch files

Options:
    --clean     Remove folders & contents
    --verbose

"""
import os
import pathlib
import shutil
import subprocess

from docopt.docopt import docopt

copyright_text = """#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
# FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
verbose = None
patch_cmd = "/usr/bin/patch"
diff_cmd = "/usr/bin/diff"
args = None

STANDALONE = "standalone"
SA_RISCV = "%s/riscv" % STANDALONE
SA_INSNS = "%s/insns" % SA_RISCV

ADD_A_PATH = "%s/%s"
ORIGINALS_PATH = "./originals" + ADD_A_PATH

folder_list = [
    "originals",
    "modified",
    "patched",
]

to_originals = {
    "config.h": {"origin": STANDALONE, "staged_path": "../build/config.h"},
    "csrs.cc": {"origin": SA_RISCV},
    "csrs.h": {"origin": SA_RISCV},
    "decode.h": {"origin": SA_RISCV},
    "disasm.cc": {
        "origin": "standalone/disasm",
        "staged_path": "../build/disasm/disasm.cc",
    },
    "disasm.h": {"origin": SA_RISCV},
    "execute.cc": {"origin": SA_RISCV},
    "mmu.cc": {"origin": SA_RISCV},
    "mmu.h": {"origin": SA_RISCV},
    "primitives.h": {
        "origin": "standalone/softfloat",
        "staged_path": "../build/softfloat/primitives.h",
    },
    "processor.cc": {"origin": SA_RISCV},
    "processor.h": {"origin": SA_RISCV},
    "regnames.cc": {"origin": "standalone/disasm", "staged_path": "../build/disasm/regnames.cc"},
    "sim.cc": {"origin": SA_RISCV},
    "sim.h": {"origin": SA_RISCV},
    "simif.h": {"origin": SA_RISCV},
    "specialize.h": {
        "origin": "standalone/softfloat",
        "staged_path": "../build/softfloat/specialize.h",
    },
    "spike.cc": {
        "origin": "standalone/spike_main",
        "staged_path": "../build/spike_main/spike.cc",
    },
}

to_originals_insns = {
    "mret.h": {"origin": SA_INSNS},
    "sret.h": {"origin": SA_INSNS},
    "vadc_vim.h": {"origin": SA_INSNS},
    "vadc_vvm.h": {"origin": SA_INSNS},
    "vadc_vxm.h": {"origin": SA_INSNS},
    "vcompress_vm.h": {"origin": SA_INSNS},
    "vcpop_m.h": {"origin": SA_INSNS},
    "vfcvt_f_x_v.h": {"origin": SA_INSNS},
    "vfcvt_f_xu_v.h": {"origin": SA_INSNS},
    "vfcvt_rtz_x_f_v.h": {"origin": SA_INSNS},
    "vfcvt_rtz_xu_f_v.h": {"origin": SA_INSNS},
    "vfcvt_x_f_v.h": {"origin": SA_INSNS},
    "vfcvt_xu_f_v.h": {"origin": SA_INSNS},
    "vfirst_m.h": {"origin": SA_INSNS},
    "vfmerge_vfm.h": {"origin": SA_INSNS},
    "vfmv_f_s.h": {"origin": SA_INSNS},
    "vfmv_s_f.h": {"origin": SA_INSNS},
    "vfmv_v_f.h": {"origin": SA_INSNS},
    "vfncvt_f_f_w.h": {"origin": SA_INSNS},
    "vfncvt_f_x_w.h": {"origin": SA_INSNS},
    "vfncvt_f_xu_w.h": {"origin": SA_INSNS},
    "vfncvt_rod_f_f_w.h": {"origin": SA_INSNS},
    "vfncvt_rtz_x_f_w.h": {"origin": SA_INSNS},
    "vfncvt_rtz_xu_f_w.h": {"origin": SA_INSNS},
    "vfncvt_x_f_w.h": {"origin": SA_INSNS},
    "vfncvt_xu_f_w.h": {"origin": SA_INSNS},
    "vfslide1down_vf.h": {"origin": SA_INSNS},
    "vfslide1up_vf.h": {"origin": SA_INSNS},
    "vfwcvt_f_f_v.h": {"origin": SA_INSNS},
    "vfwcvt_f_x_v.h": {"origin": SA_INSNS},
    "vfwcvt_f_xu_v.h": {"origin": SA_INSNS},
    "vfwcvt_rtz_x_f_v.h": {"origin": SA_INSNS},
    "vfwcvt_rtz_xu_f_v.h": {"origin": SA_INSNS},
    "vfwcvt_x_f_v.h": {"origin": SA_INSNS},
    "vfwcvt_xu_f_v.h": {"origin": SA_INSNS},
    "vid_v.h": {"origin": SA_INSNS},
    "viota_m.h": {"origin": SA_INSNS},
    "vmadc_vim.h": {"origin": SA_INSNS},
    "vmadc_vvm.h": {"origin": SA_INSNS},
    "vmadc_vxm.h": {"origin": SA_INSNS},
    "vmerge_vim.h": {"origin": SA_INSNS},
    "vmerge_vvm.h": {"origin": SA_INSNS},
    "vmerge_vxm.h": {"origin": SA_INSNS},
    "vmsbc_vvm.h": {"origin": SA_INSNS},
    "vmsbc_vxm.h": {"origin": SA_INSNS},
    "vmsbf_m.h": {"origin": SA_INSNS},
    "vmsif_m.h": {"origin": SA_INSNS},
    "vmsof_m.h": {"origin": SA_INSNS},
    "vmulhsu_vv.h": {"origin": SA_INSNS},
    "vmulhsu_vx.h": {"origin": SA_INSNS},
    "vmv_s_x.h": {"origin": SA_INSNS},
    "vmv_x_s.h": {"origin": SA_INSNS},
    "vmvnfr_v.h": {"origin": SA_INSNS},
    "vrgather_vi.h": {"origin": SA_INSNS},
    "vrgather_vv.h": {"origin": SA_INSNS},
    "vrgather_vx.h": {"origin": SA_INSNS},
    "vrgatherei16_vv.h": {"origin": SA_INSNS},
    "vsbc_vvm.h": {"origin": SA_INSNS},
    "vsbc_vxm.h": {"origin": SA_INSNS},
    "vslide1down_vx.h": {"origin": SA_INSNS},
    "vslide1up_vx.h": {"origin": SA_INSNS},
    "vwmulsu_vv.h": {"origin": SA_INSNS},
    "vwmulsu_vx.h": {"origin": SA_INSNS},
}

# Contains a list of tuples of the additional path string, and the associated
# collection of file names that go there.
file_folders = [("", to_originals), ("/insns", to_originals_insns)]


def printout(string):
    if verbose:
        print(string)


def first_file_is_newer(file1, file2):
    """If file2 is older than file1, or does not exist, return True"""
    try:
        file1_ts = os.stat(file1).st_mtime
    except FileNotFoundError as exc:
        print("source file1, %s, not found" % file1)
        raise exc
    try:
        file2_ts = os.stat(file2).st_mtime
    except FileNotFoundError:
        print("target file2, %s, not found" % file2)
        return True
    if file1_ts > file2_ts:
        return True
    return False


def should_do_patch(src, patch, tgt):
    """If either the src or patch is newer than the tgt, return True"""
    if first_file_is_newer(src, tgt) or first_file_is_newer(patch, tgt):
        retval = True
        print("Doing %s" % src)
    else:
        retval = False
        print("Skipping %s" % src)
    return retval


def patch_file(src, patch, tgt):
    cmd = [patch_cmd, src, "-i", patch, "-o", tgt]
    printout("Calling %s" % cmd)
    returncode = subprocess.call(cmd)
    if returncode:
        print("error encountered running %r" % cmd)


def make_folders():
    for item in folder_list:
        if args["--clean"]:
            shutil.rmtree(item, ignore_errors=True)
        pathlib.Path("%s/insns" % item).mkdir(parents=True, exist_ok=True)


def create_originals():
    for extra_path, dic in file_folders:
        for item in dic.keys():
            path = dic[item]["origin"]
            src = "../" + ADD_A_PATH % (path, item)
            tgt = ORIGINALS_PATH % (extra_path, item)
            if first_file_is_newer(src, tgt):
                printout("copying %s to %s" % (src, tgt))
                shutil.copy(src, tgt, follow_symlinks=False)


def apply_patches():
    make_folders()
    create_originals()
    for extra_path, dic in file_folders:
        for item in dic.keys():
            src = ORIGINALS_PATH % (extra_path, item)
            patch = ("./patches" + ADD_A_PATH + ".patch") % (extra_path, item)

            # allow for specified target filename
            tgt = "./patched" + ADD_A_PATH % (extra_path, item)

            if should_do_patch(src, patch, tgt):
                patch_file(src, patch, tgt)


def stage_patched_files():
    for extra_path, dic in file_folders:
        for item in dic.keys():
            src = "./patched" + ADD_A_PATH % (extra_path, item)
            tgt = dic[item].get(
                "staged_path",
                "../build/riscv" + ADD_A_PATH % (extra_path, item),
            )
            if first_file_is_newer(src, tgt):
                shutil.copy(src, tgt, follow_symlinks=False)


def generate_patches():
    make_folders()
    create_originals()
    for extra_path, dic in file_folders:
        for item in dic.keys():
            # copy into
            # patch_tgt = './modified%s/%s.patch' % (extra_path, item)
            src = dic[item].get(
                "staged_path",
                "../build/riscv" + ADD_A_PATH % (extra_path, item),
            )
            tgt = "./modified" + ADD_A_PATH % (extra_path, item)
            if first_file_is_newer(src, tgt):
                shutil.copy(src, tgt, follow_symlinks=False)

            src = ORIGINALS_PATH % (extra_path, item)
            tgt = "./modified" + ADD_A_PATH % (extra_path, item)
            patch = "./patches" + ADD_A_PATH % (extra_path, item + ".patch")

            # see if patch needs to be recreated
            if should_do_patch(src, tgt, patch):
                with open(patch, "w") as fh:
                    fh.write(copyright_text)

                with open(patch, "a") as fh:
                    cmd = [diff_cmd, src, tgt]
                    subprocess.call(cmd, stdout=fh)


def main():
    global args, verbose
    args = docopt(__doc__)
    print(args)

    if args["--verbose"]:
        verbose = 1
    else:
        verbose = 0

    if args["patch"]:
        apply_patches()
        stage_patched_files()
    elif args["generate"]:
        folder_list.append("patches")
        generate_patches()


if __name__ == "__main__":
    main()
