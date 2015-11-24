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

from timePeriodProcessor import TimePeriodProcessor
from conditionProcessorConfig import FILTERED_DATA_LIMIT
from copy import copy
from data.dataRetriever import DataRetriever
from matchingPeriodFinder import MatchingPeriodFinder


class TimebasedConditionProcessor(TimePeriodProcessor):
    def __init__(self, data_dao, conditions_builder, time_limit):
        super(TimebasedConditionProcessor, self).__init__()
        self.data_dao = data_dao
        self.conditions_builder = conditions_builder
        self.time_limit = time_limit
        self.timestamps = None
        self.data_retriever = None
        self.matching_period = None

    def process(self, data_retrieve_params, timestamps):
        print 'PROCESSING TIME BASED CONDITION'
        self.timestamps = copy(timestamps)
        self.data_retriever = DataRetriever(data_dao=self.data_dao, data_retrieve_params=data_retrieve_params)

        if not self.is_full_period_from_last_trigger_time():
            print ('There was not full period of ' + str(self.time_limit) + ' seconds from last trigger time')
            return []

        self.__find_matching_period()

        if self.__is_condition_fulfilled():
            print ('Matching time period length: ' + str(self.matching_period))
            map_fun = self.conditions_builder.get_condition()

            data = self.data_retriever.get_data(start=self.matching_period_start_time,
                                                end=self.__get_matching_period_end_time())

            filtered_data = data.filter(lambda x: map_fun(x)['passed']).take(FILTERED_DATA_LIMIT)

            self.timestamps['last_obs_trigger_time'] = self.__get_matching_period_end_time()
            return filtered_data

        return []

    def __is_condition_fulfilled(self):
        return self.time_limit * 1000 <= self.matching_period

    def __get_matching_period_end_time(self):
        return self.matching_period_start_time + self.time_limit + 1

    def __find_matching_period(self):
        data = self.data_retriever.get_data(start=self.timestamps['last_obs_trigger_time'],
                                            end=self.timestamps['current_execution_time'])
        matching_period_finder = MatchingPeriodFinder(data)
        self.matching_period = matching_period_finder.get_largest(self.conditions_builder.get_condition())

        self.matching_period_start_time = matching_period_finder.get_largest_start_time()
