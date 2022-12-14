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
from VectorTestSequence import VectorLoadStoreTestSequence
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV


# This test verifies that indexed load and store instructions can be generated and executed
# successfully.
class MainSequence(VectorLoadStoreTestSequence):
    def __init__(self, aGenThread, aName=None):
        super().__init__(aGenThread, aName)

        self._mInstrList = (
            "VLOXEI16.V##RISCV",
            "VLOXEI32.V##RISCV",
            "VLOXEI64.V##RISCV",
            "VLOXEI8.V##RISCV",
            "VLUXEI16.V##RISCV",
            "VLUXEI32.V##RISCV",
            "VLUXEI64.V##RISCV",
            "VLUXEI8.V##RISCV",
            "VSOXEI16.V##RISCV",
            "VSOXEI32.V##RISCV",
            "VSOXEI64.V##RISCV",
            "VSOXEI8.V##RISCV",
            "VSUXEI16.V##RISCV",
            "VSUXEI32.V##RISCV",
            "VSUXEI64.V##RISCV",
            "VSUXEI8.V##RISCV",
        )

    # Return a list of test instructions to randomly choose from.
    def _getInstructionList(self):
        return self._mInstrList


MainSequenceClass = MainSequence
GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV
