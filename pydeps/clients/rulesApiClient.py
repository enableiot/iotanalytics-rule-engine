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

from baseApiClient import BaseApiClient
import json

class RulesApiClient(BaseApiClient):

    def __init__(self, config):
        super(RulesApiClient, self).__init__(config)
        print("Dashboard API URL - " + str(self.dashboard_api_url))

    def get_active_rules(self):
        request_url = ''.join([self.__get_path(), 'status/Active'])
        resp, content = self.make_request(request_url, "GET")
        return self.__parse_devices_with_components_response(content)

    def add_rule_executions(self, rule, component_ids_with_observation, last_execution):
        request_url = ''.join([self.dashboard_api_url, 'accounts/', rule["accountId"], '/rules/', rule["id"], '/execution'])

        body = json.dumps(self.__get_execution_body(component_ids_with_observation, last_execution))
        self.make_request(request_url, "POST", body)

    def __get_execution_body(self, component_ids_with_observation, last_execution):
        execution_body = []
        for cid, last_observation in component_ids_with_observation.iteritems():
            single_execution = {
                "cid": cid,
                "lastExecution": last_execution,
            }
            if last_observation is not None:
                single_execution["lastObservation"] = last_observation

            execution_body.append(single_execution)
        return execution_body

    def __get_path(self):
        return ''.join([self.dashboard_api_url, 'rules/'])

    def __parse_devices_with_components_response(self, content):
        try:
            return json.loads(content)
        except Exception:
            print ("Unexpected get_active_rules response: " + content)
            raise
