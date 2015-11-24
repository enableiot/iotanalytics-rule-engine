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

import traceback

from rules.ruleProcessor import RuleProcessor
from clients.dashboardApiClient import DashboardApiClient
from db.dataDao import DataDao


class RulesProcessor(object):
    def __init__(self, config, spark_context):
        self.config = config
        self.spark_context = spark_context
        self.data_dao = DataDao(spark_context=spark_context, config=self.config)
        self.api_client = DashboardApiClient(config=self.config)

    def process_rules(self):
        active_rules = self.api_client.get_active_rules()
        print("Active rules found: " + str(len(active_rules)))

        for rule in active_rules:
            try:
                meta = self.get_metadata_for_rule(rule)
                rule['meta'] = meta
                rule_processor = RuleProcessor(rule=rule, data_dao=self.data_dao,
                                               api_client=self.api_client)
                rule_processor.process_rule()
            except Exception:
                print ('Error during rule processing')
                traceback.print_exc()

    def get_metadata_for_rule(self, rule):
        rule_metadata = {'devices': {}}

        account_id = rule["accountId"]

        devices_ids = rule["devices"]
        if not devices_ids:
            print("No device list provided. Will fetch all devices for account.")

        devices_with_components = self.api_client.get_devices_with_components(account_id, devices_ids)

        for device_id in devices_with_components:
            component_list = filter(lambda comp: comp['name'] in self.__get_rule_device_components_names__(rule),
                                    devices_with_components[device_id])
            rule_metadata['devices'][str(device_id)] = {"components": component_list}

        return rule_metadata

    def __get_rule_device_components_names__(self, rule):
        return map(lambda condition: condition['component']['name'], rule['conditions']['values'])
