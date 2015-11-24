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
from clients.conditionsParser import ConditionsParser
from utils.timestampFormatter import TimestampFormatter
import json
import time


class AlertApiClient(BaseApiClient):

    def push_alert(self, rule, device_list, conditions):
        request_url = self.dashboard_api_url + 'alerts'

        body = json.dumps(self.__get_alert_body__(rule, device_list, conditions))

        resp, content = None, None
        try:
            resp, content = self.make_request(request_url, 'POST', body)
        except Exception:
            print('Error, unable to push alerts. Response: ' + str(resp) + ', Content: ' + str(content))
            raise

    def __get_alert_body__(self, rule, device_list, list_of_results):
        components_conditions = ConditionsParser(rule=rule, list_of_results=list_of_results).build_conditions()

        device_id = device_list[0]

        return {
            "msgType": "alertsPush",
            "data": [
                {
                    "accountId": str(rule['accountId']),
                    "ruleId": str(rule['externalId']),
                    "deviceId": device_id,
                    "timestamp": int(TimestampFormatter.convert_ts_to_non_scientific_ms(time.time())),
                    'conditions': [
                        {
                            'components': components_conditions
                        }
                    ]
                }
            ]
        }

