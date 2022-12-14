#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import Log

from base.Sequence import Sequence
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV


# Testing register data operand request with different precisions and types.
# FP request string format is:
#   'FP{size}(exp={constr})(sign={constr})(frac={constr})
# INT request string format is: 'INT{size}({constr})
# {size} is data size of 16/32/64 and {constr} is the constraint string to be
# applied to the init data


class MainSequence(Sequence):
    VALID_PRECISIONS = ["H", "S", "D"]
    VALID_DATA_TYPES = ["FP", "INT"]
    VALID_DATA_SIZES = [16, 32, 64]
    INSTRUCTIONS = {
        "H": ["FMUL.H##RISCV", "FDIV.H##RISCV"],
        "S": [
            "FMUL.S##RISCV",
            "FDIV.S##RISCV",
        ],
        "D": [
            "FMUL.D##RISCV",
            "FDIV.D##RISCV",
        ],
    }

    def generate(self, **kargs):
        (prec, prec_valid) = self.getOption("precision")
        (data_type, data_type_valid) = self.getOption("data_type")
        (data_size, data_size_valid) = self.getOption("data_size")

        if not prec_valid or prec not in self.VALID_PRECISIONS:
            Log.warn("precision option invalid or missing, using single precision (S) as default")
            prec = "S"

        if not data_type_valid or data_type not in self.VALID_DATA_TYPES:
            Log.warn("data type option invalid or missing, using FP as default")
            data_type = "FP"

        if not data_size_valid or data_size not in self.VALID_DATA_SIZES:
            Log.warn("data size option invalid or missing, using 32 as default")
            data_size = 32

        data_string = "(0x0)"
        if data_type == "FP":
            data_string = "(exp=0x0-0xF)(sign=0x1)(frac=0x0-0xFF)"
        elif data_type == "INT":
            data_string = "(0x0-0xFFFF)"

        for instr in self.INSTRUCTIONS[prec]:
            self.genInstruction(
                instr,
                {
                    "rs1.Data": "{}{}{}".format(data_type, data_size, data_string),
                    "rs2.Data": "{}{}{}".format(data_type, data_size, data_string),
                },
            )


MainSequenceClass = MainSequence
GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV
