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


from comparison.string_functions import StringFunctions
from comparison.float_functions import FloatFunctions
from comparison.boolean_functions import BooleanFunctions
from utils.hbaseDataParser import HbaseDataParser


class FunctionProviderFactory(object):
    def __init__(self, component_type):
        if component_type == "String":
            self.function_provider = StringFunctions()
        elif component_type == "Boolean":
            self.function_provider = BooleanFunctions()
        elif component_type == "Number":
            self.function_provider = FloatFunctions()
        else:
            raise AttributeError("Component Type not supported: " + component_type)

    def get_function_provider(self):
        return self.function_provider


class ConditionSelectorFactory(object):

    @staticmethod
    def get(condition):
        if 'timeLimit' in condition:
            return TimePeriodFunctionSelector(condition['operator'], condition['component']['dataType'])
        return ConditionFunctionSelector(condition['operator'], condition['component']['dataType'])


class ConditionFunctionSelector(object):
    def __init__(self, operator, component_type):
        self.operator = operator
        self.function_selector = FunctionProviderFactory(component_type).get_function_provider()

    def get_function(self):
        try:
            return self.function_selector.functions_map[self.operator]
        except Exception:
            raise AttributeError("Unable to create condition function for operator: " + str(self.operator))


class TimePeriodFunctionSelector(object):
    def __init__(self, operator, component_type):
        self.operator = operator
        self.function_selector = FunctionProviderFactory(component_type).get_function_provider()

    def get_function(self):
        try:
            return self.__map_function
        except Exception:
            raise AttributeError("Unable to create condition function for operator: " + str(self.operator))

    def __map_function(self, val_rdd, values):
        fun = self.function_selector.functions_map[self.operator]
        return {
            'passed': fun(val_rdd, values),
            'timestamp': HbaseDataParser.get_observation_timestamp(val_rdd),
            'value': val_rdd[1]
        }