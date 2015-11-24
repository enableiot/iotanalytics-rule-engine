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

from conditionProcessorConfig import FILTERED_DATA_LIMIT
from data.dataRetriever import DataRetriever
from copy import copy

class BasicConditionProcessor(object):
    def __init__(self, data_dao, conditions_builder):
        self.data_dao = data_dao
        self.conditions_builder = conditions_builder
        self.timestamps = None

    def process(self, data_retrieve_params, timestamps):
        print 'PROCESSING BASIC CONDITION'
        print 'Timestamps:', timestamps
        self.timestamps = copy(timestamps)
        data_retriever = DataRetriever(data_dao=self.data_dao, data_retrieve_params=data_retrieve_params)
        data = data_retriever.get_data(end=timestamps['current_execution_time'], start=timestamps['last_execution_time'])
        return self.__get_rule_matching_data__(data=data)

    def __get_rule_matching_data__(self, data):
        fun = self.conditions_builder.get_condition()

        filtered_data = data.filter(lambda x: fun(x)).take(FILTERED_DATA_LIMIT)

        return filtered_data
