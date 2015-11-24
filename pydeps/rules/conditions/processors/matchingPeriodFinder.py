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


class MatchingPeriodFinder(object):

    NO_MATCHING_PERIOD = 0

    def __init__(self, data):
        self.data = data
        self.result = None

    def get_largest(self, map_function):
        reduce_fun = ReduceFunctionBuilder().reduce_fun
        if self.data.isEmpty():
            return self.NO_MATCHING_PERIOD

        self.result = self.__map_and_sort(map_function).coalesce(1).reduce(lambda y, z: reduce_fun(y, z))

        if ReduceFunctionBuilder.CURRENT_MATCHING_PERIOD not in self.result:
            return self.NO_MATCHING_PERIOD

        if ReduceFunctionBuilder.is_current_greatest(self.result):
            return self.result[ReduceFunctionBuilder.CURRENT_MATCHING_PERIOD]

        return self.result[ReduceFunctionBuilder.LARGEST_MATCHING_PERIOD]

    def get_largest_start_time(self):
        if self.result is None:
            return self.NO_MATCHING_PERIOD
        if 'period_start' in self.result:
            return self.result['period_start'] / 1000
        return self.result['timestamp'] / 1000

    def __map_and_sort(self, map_function):
        return self.data.map(lambda x: map_function(x)).sortBy(lambda x: x['timestamp']).cache()


class ReduceFunctionBuilder(object):

    LARGEST_MATCHING_PERIOD = 'largest_matching_period'
    CURRENT_MATCHING_PERIOD = 'current_matching_period'
    TIMESTAMP = 'timestamp'

    def reduce_fun(self, x, y):
        if x['passed'] and y['passed']:
            self.__increase_current_matching_period(x, y)
        elif x['passed']:  # matching sequence end
            self.__compare_matching_periods(x, y)
        else:  # no matching data
            self.__reset_matching_period(x, y)

        return y

    def __increase_current_matching_period(self, x, y):
        y[self.CURRENT_MATCHING_PERIOD] = y[self.TIMESTAMP] - x[self.TIMESTAMP]
        y[self.TIMESTAMP] = x[self.TIMESTAMP]
        self.__copy_largest_period(x, y)

    def __compare_matching_periods(self, x, y):
        if self.is_current_greatest(x):
            self.__set_largest_period(x, y)
        else:
            self.__copy_largest_period(x, y)

        y[self.CURRENT_MATCHING_PERIOD] = 0

    def __reset_matching_period(self, x, y):
        y[self.CURRENT_MATCHING_PERIOD] = 0
        if self.__has_largest_period(x):
            self.__copy_largest_period(x, y)

    @staticmethod
    def is_current_greatest(value):
        return not ReduceFunctionBuilder.__has_largest_period(value) \
               or value[ReduceFunctionBuilder.LARGEST_MATCHING_PERIOD] < value[ReduceFunctionBuilder.CURRENT_MATCHING_PERIOD]

    @staticmethod
    def __set_largest_period(x, y):
        y[ReduceFunctionBuilder.LARGEST_MATCHING_PERIOD] = x[ReduceFunctionBuilder.CURRENT_MATCHING_PERIOD]
        y['period_start'] = x[ReduceFunctionBuilder.TIMESTAMP]

    def __copy_largest_period(self, x, y):
        if self.__has_largest_period(x):
            y[self.LARGEST_MATCHING_PERIOD] = x[self.LARGEST_MATCHING_PERIOD]
            y['period_start'] = x[self.TIMESTAMP]

    @staticmethod
    def __has_largest_period(value):
        return ReduceFunctionBuilder.LARGEST_MATCHING_PERIOD in value