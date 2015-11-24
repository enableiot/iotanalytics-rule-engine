#!/bin/bash
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
#

if python -m py_compile job.py ; then
  echo ""
  echo "syntax OK"
else
  echo ""
  echo "!!!!!! job.py - incorrect syntax !!!!!!"
  exit 1
fi

cd hbase-jars
./get.sh
cd -

cd pydeps
zip -r pydeps pydeps.zip ./*
mv pydeps.zip ../
cd -

TARGET=(`cf t | grep "Space"`)
SPACE=${TARGET[1]}

cf push ${SPACE}-rule-engine -c ./init.sh -b https://github.com/cloudfoundry/binary-buildpack.git
