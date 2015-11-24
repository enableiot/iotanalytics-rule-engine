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


class FloatFunctions(BaseFunctions):

    def gt(self, val_rdd, values):
        try:
            return float(val_rdd[1]) > float(values[0])
        except:
            return False

    def ge(self, val_rdd, values):
        try:
            return float(val_rdd[1]) >= float(values[0])
        except:
            return False

    def lt(self, val_rdd, values):
        try:
            return float(val_rdd[1]) < float(values[0])
        except:
            return False

    def le(self, val_rdd, values):
        try:
            return float(val_rdd[1]) <= float(values[0])
        except:
            return False

    def not_equal(self, val_rdd, values):
        float_values = [ float(x) for x in values ]
        try:
            return not float(val_rdd[1]) in float_values
        except:
            return False

    def equal(self, val_rdd, values):
        float_values = [ float(x) for x in values ]
        try:
            return float(val_rdd[1]) in float_values
        except:
            return False

    def like(self, val_rdd, values):
        try:
            return val_rdd[1] in values[0]
        except:
            return False

    def between(self, val_rdd, values):
        try:
            float_val_rdd = float(val_rdd[1])
            return float(values[0]) <= float_val_rdd <= float(values[1])
        except:
            return False

    def not_between(self, val_rdd, values):
        try:
            float_val_rdd = float(val_rdd[1])
            return float_val_rdd < float(values[0]) or float_val_rdd > float(values[1])
        except:
            return False