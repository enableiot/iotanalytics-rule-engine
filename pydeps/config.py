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


class Config(object):

    def __init__(self, cf_reader):
        self.cf_reader = cf_reader
        self.__prepare_config__()

    def __prepare_config__(self):
        self.ZOOKEEPERS = self.cf_reader.get_zookeepers_uri()
        self.DEVICE_MEASUREMENT_TABLE_NAME = self.cf_reader.get_device_measurement_table_name()
        self.DASHBOARD_URL = self.cf_reader.get_dashboard_endpoint()
        self.USER_CREDENTIALS = self.cf_reader.get_rule_engine_user_credentials()

