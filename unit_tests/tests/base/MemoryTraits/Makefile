#
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
FORCE_DIR = ../../../..
INC_PATHS = -I$(FORCE_DIR)/riscv/inc -I$(FORCE_DIR)/base/inc -I$(FORCE_DIR)/3rd_party/inc -I../../../utils/inc

ARCH_ENUM=RISCV

include Makefile.target
include $(FORCE_DIR)/utils/make/Makefile.common
include ../../Makefile_unit_tests.common

CFLAGS := $(CFLAGS) -DUNIT_TEST
NODEPS:=clean

vpath %.cc $(FORCE_DIR)/riscv/src $(FORCE_DIR)/3rd_party/src $(FORCE_DIR)/base/src
vpath %.d $(DEP_DIR)

all:
	@$(MAKE) make_dir
	@$(MAKE) bin/$(TARGET_NAME)

ifeq (0, $(words $(findstring $(MAKECMDGOALS), $(NODEPS))))
-include $(ALL_DEPS)
endif

$(DEP_DIR)/%.d: %.cc
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INC_PATHS) -MM -MT '$(patsubst $(DEP_DIR)/%.d,$(OBJ_DIR)/%.o,$@)' $< -MF $@

$(OBJ_DIR)/%.o: %.cc %.d
	$(CC) -c $(CFLAGS) $(INC_PATHS) -o $@ $<

bin/$(TARGET_NAME): $(ALL_OBJS)
	$(CC) -o $@ $^ $(LFLAGS)

.PHONY: make_dir
make_dir:
	@mkdir -p bin make_area make_area/obj make_area/dep

.PHONY: clean
clean:
	rm -rf make_area bin
