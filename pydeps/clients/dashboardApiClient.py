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

from devicesApiClient import DeviceApiClient
from alertsApiClient import AlertApiClient
from rulesApiClient import RulesApiClient


class DashboardApiClient(object):

    def __init__(self, config):
        self.device_api_client = DeviceApiClient(config)
        self.alert_api_client = AlertApiClient(config)
        self.rules_api_client = RulesApiClient(config)

    def push_alert(self, rule, device_list, conditions):
        self.alert_api_client.push_alert(rule, device_list, conditions)

    def get_devices_with_components(self, account_id, devices_ids=None):
        return self.device_api_client.get_devices_with_components(account_id, devices_ids)

    def get_active_rules(self):
        return self.rules_api_client.get_active_rules()

    def add_rule_executions(self, rule, component_ids_with_observation, last_execution):
        return self.rules_api_client.add_rule_executions(rule, component_ids_with_observation, last_execution)