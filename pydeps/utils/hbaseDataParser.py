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


class HbaseDataParser(object):

    @staticmethod
    def get_observation_timestamp(data):
        return int(data[0].split('\\x00')[2])

    @staticmethod
    def parse_observations(data_series):
        values = []
        for data in data_series:
            values.append({
                'timestamp': HbaseDataParser.get_observation_timestamp(data),
                'value': str(data[1])
            })
        return values
