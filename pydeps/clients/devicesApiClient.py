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


class DeviceApiClient(BaseApiClient):

    def get_devices_with_components(self, account_id, device_ids=None):
        request_url = ''.join([self.__get_path(account_id), 'search/'])

        body = self.__get_devices_search_body(device_ids)

        resp, content = self.make_request(request_url, "POST", body)
        return self.__parse_devices_with_components_response(content)

    @staticmethod
    def __get_devices_search_body(device_list):
        return json.dumps({
            'deviceId':
                {
                    'operator': 'in',
                    'value': device_list
                },
            'status':
                {
                    'operator': 'eq',
                    'value': 'active'
                }
        })

    def __get_path(self, account_id):
        return ''.join([self.dashboard_api_url, 'accounts/', account_id, '/devices/'])

    def __parse_devices_with_components_response(self, content):
        response = {}

        try:
            parsed_content = json.loads(content)
            for device in parsed_content:
                response[device['deviceId']] = self.__parse_device_component(device['components'])
        except Exception:
            raise Exception('Unexpected get_devices_with_components response - ' + str(content))
        return response

    def __parse_device_component(self, components):
        response = []
        for device_component in components:
            response.append({
                'name': device_component['name'],
                'id': device_component['cid'],
                'component_type_id': device_component["componentTypeId"]
            })

        return response