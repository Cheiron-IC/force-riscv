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
import traceback


def assert_true(expression, msg=""):
    if not expression:
        err_msg = "%s is false. %s" % (str(expression), msg)
        log_failure(err_msg)


def assert_false(expression, msg=""):
    if expression:
        err_msg = "%s is true. %s" % (str(expression), msg)
        log_failure(err_msg)


def assert_equal(left, right, msg=""):
    if left != right:
        err_msg = "%s != %s. %s" % (str(left), str(right), msg)
        log_failure(err_msg)


def assert_less_equal(left, right, msg=""):
    if left > right:
        err_msg = "%s > %s. %s" % (str(left), str(right), msg)
        log_failure(err_msg)


def assert_greater_equal(left, right, msg=""):
    if left < right:
        err_msg = "%s < %s. %s" % (str(left), str(right), msg)
        log_failure(err_msg)


def assert_not_in(elem, container, msg=""):
    if elem in container:
        err_msg = "%s is in %s. %s" % (str(elem), str(container), msg)
        log_failure(err_msg)


def log_failure(err_msg):
    stack_frame_str = get_stack_frame_string()
    Log.fail("%s\n%s" % (err_msg, stack_frame_str))


def get_stack_frame_string():
    stack_frames = traceback.format_list(traceback.extract_stack())
    stack_frame_str = "".join(stack_frames[:-1])
    return stack_frame_str
