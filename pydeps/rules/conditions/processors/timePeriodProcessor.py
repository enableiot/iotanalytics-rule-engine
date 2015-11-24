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


class TimePeriodProcessor(object):

    def __init__(self):
        self.time_limit = None
        self.timestamps = {
            'current_execution_time': None,
            'last_execution_time': None,
            'last_obs_trigger_time': None
        }

    def is_full_period_from_last_trigger_time(self):
        return not self.timestamps['last_obs_trigger_time'] or \
               self.timestamps['current_execution_time'] - self.timestamps['last_obs_trigger_time'] >= self.time_limit
