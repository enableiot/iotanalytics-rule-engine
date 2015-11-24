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


class ComponentConditionStatus(object):

    def __init__(self, component):
        self.component = component
        self.is_passed = False
        self.passing_values = None

    def mark_passed(self, passing_values):
        self.is_passed = True
        self.passing_values = passing_values

    def mark_failed(self):
        self.is_passed = False


