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

from datetime import datetime
import math
import time
from rules.conditions.results.componentConditionStatus import ComponentConditionStatus
from rules.ruleResultChecker import RuleResultChecker
from data import dataRetriever
from rules.conditions.conditionsBuilder import ConditionsBuilder
from rules.conditions.processors.conditionProcessorFactory import ConditionProcessorFactory

class RuleProcessor(object):
    def __init__(self, rule, data_dao, api_client):
        self.api_client = api_client
        self.data_dao = data_dao
        self.rule = rule
        self.rule_processing_start_date = int(math.floor(time.time()))
        self.timestamps = None
        self.list_of_results = {}

    def process_rule(self):

        print("Rule [META] = ", self.rule['meta'])
        component_ids_with_observation = {}
        for device_id, device_details in self.rule['meta']['devices'].items():
            self.list_of_results[device_id] = []
            for component in device_details['components']:
                component_id = str(component['id'])
                component_name = str(component['name'])
                data_retrieve_params = dataRetriever.DataRetrieveParams(rule=self.rule, component_id=component_id)

                conditions_builder = ConditionsBuilder(self.rule['conditions'], component_name)
                self.__init_execution_timestamps__()
                self.__add_previous_rule_executions_timestamps__(component_id)

                for condition in conditions_builder.get_conditions_for_component():
                    condition_processor = ConditionProcessorFactory.get_condition_processor(self.data_dao, condition)
                    matching_data = condition_processor.process(data_retrieve_params, self.timestamps)
                    self.timestamps = condition_processor.timestamps
                    self.__check_component_condition_status(matching_data, component, device_id)

                component_ids_with_observation[component_id] = self.__format_timestamp_for_processing(
                    'last_obs_trigger_time')

        if self.is_rule_fulfilled():
            print "Rule triggered, id - ", self.rule['id']
            self.api_client.push_alert(self.rule, self.list_of_results.keys(), self.list_of_results.values())
        else:
            print'Rule not triggered - ', self.rule['id']

        # lets update execution time if no exception from push_alert
        if len(component_ids_with_observation) > 0:
            self.__save_last_processing_batch_dates(component_ids_with_observation)

    def __init_execution_timestamps__(self):
        self.timestamps = {
            'current_execution_time': self.rule_processing_start_date,
            'last_execution_time': None,
            'last_obs_trigger_time': None
        }

    def __add_previous_rule_executions_timestamps__(self, component_id):
        if component_id in self.rule["executions"]:
            for key in self.rule["executions"][component_id]:
                self.timestamps[key] = self.rule["executions"][component_id][key]

    def __check_component_condition_status(self, matching_data, component, device_id):
        component_condition_status = ComponentConditionStatus(component)

        if len(matching_data) > 0:
            component_condition_status.mark_passed(matching_data)
        else:
            component_condition_status.mark_failed()

        self.list_of_results[device_id].append(component_condition_status)

    def is_rule_fulfilled(self):
        return RuleResultChecker(self.rule).is_fulfilled(self.list_of_results.values())

    def __save_last_processing_batch_dates(self, component_ids_with_observation):
        current_execution_time = self.__format_timestamp_for_processing('current_execution_time')

        self.api_client.add_rule_executions(rule=self.rule,
                                                    component_ids_with_observation=component_ids_with_observation,
                                                    last_execution=current_execution_time)

    def __format_timestamp_for_processing(self, key):
        if self.timestamps[key]:
            print ('Saving ' + key + ' - ' + str(
                datetime.fromtimestamp(self.timestamps[key]).strftime('%Y-%m-%d %H:%M:%S')))
            return self.timestamps[key]
