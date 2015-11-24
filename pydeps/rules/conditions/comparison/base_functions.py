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


class BaseFunctions:
    def __init__(self):
        self.functions_map = {
            '>': self.gt,
            '>=': self.ge,
            '<': self.lt,
            '<=': self.le,
            'Not Equal': self.not_equal,
            'Equal': self.equal,
            'Like': self.like,
            'Between': self.between,
            'Not Between': self.not_between
        }

    def gt(self, val_rdd, values):
        raise NotImplementedError()

    def ge(self, val_rdd, values):
        raise NotImplementedError()

    def lt(self, val_rdd, values):
        raise NotImplementedError()

    def le(self, val_rdd, values):
        raise NotImplementedError()

    def not_equal(val_rdd, values):
        _values = [str(x) for x in values]
        try:
            return not str(val_rdd[1]) in _values
        except:
            return False

    def equal(self, val_rdd, values):
        _values = [str(x) for x in values]
        try:
            return str(val_rdd[1]) in _values
        except:
            return False

    def like(self, val_rdd, values):
        raise NotImplementedError()

    def between(self, val_rdd, values):
        raise NotImplementedError()

    def not_between(self, val_rdd, values):
        raise NotImplementedError()
