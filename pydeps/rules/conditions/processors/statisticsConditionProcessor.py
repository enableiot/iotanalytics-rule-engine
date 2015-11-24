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


class StatisticsConditionProcessor(TimePeriodProcessor):
    def __init__(self, data_dao, conditions_builder):
        super(StatisticsConditionProcessor, self).__init__()
        self.data_dao = data_dao
        self.conditions_builder = conditions_builder
        self.timestamps = None
        self.baseline = {
            'baselineMinimalInstances': None,
            'baselineSecondsBack': None,
        }
        self.time_limit = None

    def process(self, data_retrieve_params, timestamps):
        print 'PROCESSING STATISTICS CONDITION'

        self.timestamps = copy(timestamps)
        self.baseline.update(self.conditions_builder.baseline)
        self.time_limit = self.baseline['baselineSecondsBack']

        if not self.is_full_period_from_last_trigger_time():
            print ('There was not full period of ' + str(self.baseline['baselineSecondsBack']) + ' seconds from last trigger time')
            return []

        data_retriever = DataRetriever(data_dao=self.data_dao, data_retrieve_params=data_retrieve_params)

        data = data_retriever.get_data(start=self.timestamps['last_obs_trigger_time'],
                                       end=self.timestamps['current_execution_time'])
        count = data.count()

        if self.baseline['baselineMinimalInstances'] == 0 or count < self.baseline['baselineMinimalInstances']:
            print "Number or observations in lower than baselineMinimalInstances."
            return []
        sum = data.reduce(lambda x, y: reduce_func(x, y))

        avg = sum / count

        stdev = data.map(lambda x: float(x[1])).stdev()

        self.conditions_builder.convert_to_statistics(avg, stdev)
        fun = self.conditions_builder.get_condition()
        filtered_data = data.filter(lambda x: fun(x)).take(FILTERED_DATA_LIMIT)
        if len(filtered_data) > 0:
            self.timestamps['last_obs_trigger_time'] = self.timestamps['current_execution_time']

        return filtered_data


def reduce_func(x, y):
    try:
        if type(x) == tuple:
            x = float(x[1])
        return x + float(y[1])
    except:
        return x