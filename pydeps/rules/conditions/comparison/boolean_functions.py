# Copyright (c) 2015 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from base_functions import BaseFunctions


class BooleanFunctions(BaseFunctions):

    def not_equal(self, val_rdd, values):
        _values = [bool(x) for x in values]
        try:
            return not bool(val_rdd[1]) in _values
        except:
            return False

    def equal(self, val_rdd, values):
        _values = [bool(x) for x in values]
        try:
            return bool(val_rdd[1]) in _values
        except:
            return False
