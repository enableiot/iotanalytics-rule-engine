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


import sys
import datetime
import traceback
from utils.cloudFoundryEnvReader import CloudFoundryEnvReader
from rulesProcessor import RulesProcessor
from pyspark import SparkContext
from config import Config
from version import VERSION


if __name__ == "__main__":

    print("Rule Engine {0} v. - job is starting ...".format(VERSION))
    sc = SparkContext(appName="RuleEngineSparkContext")
    try:
        cf_reader = CloudFoundryEnvReader((sys.argv[2]))
        config = Config(cf_reader=cf_reader)
        rule_processor = RulesProcessor(config=config, spark_context=sc)
        rule_processor.process_rules()
    except Exception, e:
        print("Spark job failed", e)
        traceback.print_exc()
    finally:
        sc.stop()
        print("Finish time: " + str(datetime.datetime.utcnow().isoformat()))
