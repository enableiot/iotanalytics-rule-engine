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


class DataDao(object):
    def __init__(self, spark_context, config):
        self.spark_context = spark_context
        self.zookeepers_uri = config.ZOOKEEPERS
        self.device_measurement_table_name = config.DEVICE_MEASUREMENT_TABLE_NAME

    def get_data_from_hbase(self, account_id, component_id, start_ts, stop_ts):
        print("get_data_for_device", account_id, component_id, start_ts, stop_ts)

        start = account_id + '\0' + component_id + '\0' + start_ts
        stop = account_id + '\0' + component_id + '\0' + stop_ts
        print("START: ", start.replace('\0', '\\0'))
        print("STOP: ", stop.replace('\0', '\\0'))

        # see https://hbase.apache.org/0.94/xref/org/apache/hadoop/hbase/mapreduce/TableInputFormat.html
        conf = {
            "hbase.zookeeper.quorum": self.zookeepers_uri,
            "hbase.mapreduce.inputtable": self.device_measurement_table_name,
            "hbase.mapreduce.scan.row.start": str(start),
            "hbase.mapreduce.scan.row.stop": str(stop),
            "hbase.mapreduce.scan.columns": "data:measure_val"
        }

        key_conv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
        value_conv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

        rdd = self.spark_context.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                                                 "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                                                 "org.apache.hadoop.hbase.client.Result",
                                                 conf=conf, keyConverter=key_conv, valueConverter=value_conv)
        return rdd
