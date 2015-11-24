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

import sys
sys.path.insert(0, 'httplib2.zip')
try:
    import httplib2
except Exception, ex:
    print(ex)
    exit(1)
import json


class BaseApiClient(object):
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'cache-control': 'no-cache'}
    api_path = "/v1/api/"

    def __init__(self, config):
        self.http_client = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        self.config = config
        self.dashboard_api_url = self.config.DASHBOARD_URL + self.api_path
        self.api_token = None

    def get_token(self):
        if self.api_token:  # One token per ruleprocessor execution, no need to make request each time
            return self.api_token
        request_url = self.dashboard_api_url + 'auth/token'
        body = json.dumps(self.config.USER_CREDENTIALS)
        resp, content = self.http_client.request(request_url, "POST", headers=self.headers, body=body)

        if resp["status"] == '200':
            self.api_token = json.loads(content)["token"]
            return self.api_token
        else:
            raise Exception('Unable to get token for - ' + self.config.USER_CREDENTIALS['username'] + ', response status: ' + resp['status'])

    def __generate_auth_headers(self):
        self.headers['Authorization'] = 'Bearer ' + str(self.get_token())

    def make_request(self, url, method, body=None):
        self.__generate_auth_headers()
        resp, content = self.http_client.request(url, method=method, headers=self.headers, body=body)
        self.verify_response(resp)
        return resp, content

    @staticmethod
    def verify_response(resp):
        if resp["status"] not in ['200', '304', '201']:
            raise Exception('Unexpected response status - ' + resp["status"])