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

import json
import base64


class CloudFoundryEnvReader:

    def __init__(self, vcap_bas64):
        try:
            self.vcap = json.loads(base64.b64decode(vcap_bas64))
        except Exception:
            raise EnvironmentError('Unable to decode/parse VCAP_SERVICES')

    def __get_user_provided_services__(self):
        try:
            return self.vcap['user-provided']
        except Exception:
            raise EnvironmentError('Unable to read settings from cloud foundry env variables.')

    def __get_user_provided_service__(self, name):
        for service in self.__get_user_provided_services__():
            if service['name'] == name:
                return service
        return None

    def get_rule_engine_user_credentials(self):
        try:
            credentials = self.__get_user_provided_service__('rule-engine-credentials-ups')['credentials']
            credentials['username'] = credentials['username']
            credentials['password'] = credentials['password']
            if credentials['username'] is None or credentials['password'] is None:
                raise EnvironmentError('rule-engine-credentials-ups not found')
            return credentials
        except Exception:
            raise EnvironmentError('Unable to read cf user provided services')

    def get_dashboard_endpoint(self):
        try:
            service = self.__get_user_provided_service__('dashboard-endpoint-ups')
            host = service['credentials']['host']
            if host is None:
                raise EnvironmentError('dashboard-endpoint-ups not found')
            return host
        except Exception:
            raise EnvironmentError('Unable to read cf user provided services')

    def get_zookeepers_uri(self):
        try:
            return self.vcap['zookeeper-wssb'][0]['credentials']['uri']
        except Exception:
            raise EnvironmentError('Unable to read cf zookeeper service properties')

    def get_device_measurement_table_name(self):
        try:
            service = self.__get_user_provided_service__('installer-backend-ups')
            host = service['credentials']['deviceMeasurementTableName']
            if host is None:
                raise EnvironmentError('installer-backend-ups not found')
            return host
        except Exception:
            raise EnvironmentError('Unable to read cf user provided services')