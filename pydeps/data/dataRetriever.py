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

from utils.timestampFormatter import TimestampFormatter


def format_start_date(db_timestamp):
    if db_timestamp is None:
        return '0'
    return TimestampFormatter.convert_ts_to_non_scientific_ms(db_timestamp)


def format_end_date(db_timestamp):
    if db_timestamp is None:
        return 'z'
    return TimestampFormatter.convert_ts_to_non_scientific_ms(db_timestamp)


class DataRetrieveParams(object):
    def __init__(self, component_id, rule):
        self.component_id = component_id
        self.rule = rule


class DataRetriever(object):
    def __init__(self, data_dao, data_retrieve_params):
        self.data_dao = data_dao
        self.data_retrieve_params = data_retrieve_params

    def get_data(self, end, start=None):
        start_date = format_start_date(start)
        end_date = format_end_date(end)
        return self.data_dao.get_data_from_hbase(self.__get_account_id(),
                                                 self.__get_component_id(), start_date,
                                                 end_date)

    def __get_component_last_execution_timestamp(self):
        rule = self.data_retrieve_params.rule
        if self.__get_component_id() in rule["executions"]:
            return rule["executions"][self.__get_component_id()]['last_execution_time']
        return None

    def __get_account_id(self):
        return str(self.data_retrieve_params.rule["accountId"])

    def __get_component_id(self):
        return self.data_retrieve_params.component_id