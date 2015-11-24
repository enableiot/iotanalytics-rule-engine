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

from rules.conditions.conditionsBuilder import ConditionsBuilder

class RuleResultChecker(object):

    @staticmethod
    def __join_all_results__(list_of_results):
        return reduce(lambda array_1, array_2: array_1 + array_2, list_of_results)

    def __init__(self, rule):
        self.rule = rule
        if 'operator' in rule['conditions']:
            self.rule_operator = rule['conditions']['operator']
        else:
            self.rule_operator = None
        self.list_of_results = None

    def is_fulfilled(self, list_of_results):
        self.list_of_results = list_of_results

        if self.rule_operator == ConditionsBuilder.OR:
            return reduce(lambda x, y: x or y, self.__get_result_status_list__())

        if self.rule_operator == ConditionsBuilder.AND or self.rule_operator is None:
            return reduce(lambda x, y: x and y, self.__get_result_status_list__())

        raise AttributeError("Unknown rule operator: " + str(self.rule_operator))

    def __get_result_status_list__(self):
        return map(lambda single_result: single_result.is_passed,
                   RuleResultChecker.__join_all_results__(self.list_of_results))
