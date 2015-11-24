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

from rules.ruleResultChecker import RuleResultChecker
from utils.hbaseDataParser import HbaseDataParser


class ConditionsParser(object):
    def __init__(self, rule, list_of_results):
        self.list_of_results = list_of_results
        self.rule = rule
        self.conditions = []

    def build_conditions(self):
        components_result = RuleResultChecker.__join_all_results__(self.list_of_results)

        for result in components_result:
            if self.__has_condition_passed__(result):
                single_condition_parser = SingleConditionParser(result.component, result.passing_values, self.rule)
                self.conditions.append(single_condition_parser.parse_component())

        return self.conditions

    @staticmethod
    def __has_condition_passed__(result):
        return result.passing_values is not None


class SingleConditionParser(object):

    def __init__(self, component, component_passing_data, rule):
        self.component = component
        self.component_passing_data = component_passing_data
        self.rule = rule

    def parse_component(self):
        parsed_component = {
            'componentId': str(self.component['id']),
            'componentName': str(self.component['name']),
            'dataType': self.rule['conditions']['values'][0]['component']['dataType']
        }
        parsed_component['valuePoints'] = self.__parse_component_values__()
        return parsed_component

    def __parse_component_values__(self):
        return HbaseDataParser.parse_observations(self.component_passing_data)
