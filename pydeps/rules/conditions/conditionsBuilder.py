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

from conditionFunctionSelector import ConditionSelectorFactory


class SingleConditionBuilder(object):
    def __init__(self, condition):

        self.function_selector = ConditionSelectorFactory.get(condition)

        self.values = condition['values']
        if 'baselineMinimalInstances' in condition or 'baselineSecondsBack' in condition:
            self.baseline = {}
        if 'baselineMinimalInstances' in condition:
            self.baseline['baselineMinimalInstances'] = condition['baselineMinimalInstances']
        if 'baselineSecondsBack' in condition:
            self.baseline['baselineSecondsBack'] = condition['baselineSecondsBack']

    def convert_to_statistics(self, avg, stdev):
        for i in range(len(self.values)):
            try:
                multiplier = float(self.values[i])
                self.values[i] = avg + multiplier * stdev
            except:
                print "Cannot convert condition to statistic using values: ", self.values

    def get(self, hbase_value):
        return self.function_selector.get_function()(hbase_value, self.values)

    def get_condition(self):
        return self.get


class ConditionsBuilder(object):

    AND = 'AND'
    OR = 'OR'

    def __init__(self, condition, component_name):
        self.conditions = condition['values']
        self.component_name = component_name
        self.conditions = self.get_conditions_for_component()

        if 'operator' in condition and len(self.conditions) > 1:
            self.conditions_complex_operator = condition['operator']
        else:
            self.conditions_complex_operator = None

        self.condition_functions = self.__get_functions__()

    def get_conditions_for_component(self):
        components_conditions = []

        for condition in self.conditions:
            if condition['component']['name'] == self.component_name:
                components_conditions.append(condition)
        return components_conditions

    def __get_functions__(self):
        condition_functions = []
        for condition in self.conditions:
            single_condition = SingleConditionBuilder(condition)
            condition_functions.append(single_condition.get_condition())

        return condition_functions

    def __and_function__(self, hbase_value):
        return reduce(lambda x, y: x(hbase_value) and y(hbase_value), self.condition_functions)

    def __or_function__(self, hbase_value):
        return reduce(lambda x, y: x(hbase_value) or y(hbase_value), self.condition_functions)

    def get_complex_condition(self):
        if self.conditions_complex_operator is None:
            return self.condition_functions[0]
        if self.conditions_complex_operator == self.AND:
            return self.__and_function__
        if self.conditions_complex_operator == self.OR:
            return self.__or_function__
        raise AttributeError(
            "Unable to create condition function for complex operator: " + str(self.conditions_complex_operator))
