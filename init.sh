#!/bin/bash -x
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

export LOGFILE=$HOME/log.txt

# ===========================================================================
#    INITIAL SYSTEM CHECKS
# ===========================================================================
echo -e "DATE:\n`date`\n\nUBUNTU:\n`lsb_release -a`\n\nUNAME:\n`uname -a`\n\nHOME:\n$HOME\n\nGLIBC:\n`ldd --version`\n\nGCC:\n`gcc --version`\n\nPYTHON:\n`python --version 2>&1`\n\nDISK:\n`free -m`\n\nMOUNT:\n`mount`\n\nWHOAMI:\n`whoami`\n\nCPUs:\n`cat /proc/cpuinfo`\n\nENV:\n`env`\n\nLS_HOME:\n`ls -lah $HOME`\n\n" >> machine_info.txt
cat machine_info.txt

# ===========================================================================
#    START HTTP SERVER, SO CF WON'T KILL US
# ===========================================================================
if [ ! -d public_html ]
then
    mkdir public_html
fi
cd public_html
python -m SimpleHTTPServer $PORT &
cd -

# ===========================================================================
#    INSTALL JAVA
# ===========================================================================
if [ ! -d javapkg ]
then
    mkdir -v javapkg | tee -a $LOGFILE
fi
cd javapkg
export JAVA_HOME=`pwd`/usr/lib/jvm/java-7-openjdk/jre
export PATH=$PATH:$JAVA_HOME/bin

wget -q https://launchpad.net/~openjdk/+archive/ubuntu/ppa/+files/openjdk-7-jre-headless_7~b117~pre1-0lucid1_amd64.deb  | tee -a $LOGFILE
ar x openjdk-7-jre-headless_7~b117~pre1-0lucid1_amd64.deb         | tee -a $LOGFILE
tar -xf data.tar.*   | tee -a $LOGFILE
rm -v *.tar.gz *.deb

wget -q https://launchpad.net/~openjdk/+archive/ubuntu/ppa/+files/openjdk-7-jre-lib_7~b117~pre1-0lucid1_all.deb  | tee -a $LOGFILE
ar x openjdk-7-jre-lib_7~b117~pre1-0lucid1_all.deb         | tee -a $LOGFIlLE
tar -xf data.tar.*   | tee -a $LOGFILE
rm -v *.tar.gz *.deb

rm -vrf $JAVA_HOME/lib/security/cacerts | tee -a $LOGFIlLE
cp -v $HOME/cacerts $JAVA_HOME/lib/security/cacerts     | tee -a $LOGFIlLE

KEYSTORE=$JAVA_HOME/lib/security/cacerts

cd -
echo -e "\nENV WITH JAVA:\n`env`\n" >> machine_info.txt
java -version 2>&1 | tee -a $LOGFILE
echo -e "\nJAVA VERSION:\n`java -version 2>&1`\n" >> machine_info.txt


# ===========================================================================
#    FETCH YARN/HDFS CONFIGURATION
# ===========================================================================
export CONF_DIR=$HOME/CONF_DIR
mkdir $CONF_DIR
cd $CONF_DIR
export YARN_CONF_DIR=$CONF_DIR
export HDFS_CONF_DIR=$CONF_DIR
export HADOOP_CONF_DIR=$CONF_DIR

YARN_CONFIG_URL=`echo $VCAP_SERVICES | python -c "import json; import sys; print json.loads(sys.stdin.read())['cdh'][0]['credentials']['yarn_config'].replace('https', 'http');"`
wget -q $YARN_CONFIG_URL
mv clientConfig yarnclientconfig.zip
unzip yarnclientconfig.zip

echo "YARN SITE:" | tee -a $LOGFILE
cat yarn-conf/yarn-site.xml   | tee -a $LOGFILE
echo "HDFS SITE:" | tee -a $LOGFILE
cat yarn-conf/hdfs-site.xml   | tee -a $LOGFILE
echo "CORE SITE:" | tee -a $LOGFILE
cat yarn-conf/core-site.xml   | tee -a $LOGFILE

YARN_WEB_ADDR=`cat yarn-conf/yarn-site.xml | grep -A 1 "yarn.resourcemanager.webapp.address" | tail -1 | python -c "import sys; print sys.stdin.read().split('>')[1].split('<')[0];"`
echo "yarn.resourcemanager.webapp.address ${YARN_WEB_ADDR}"

cp -v yarn-conf/* .   | tee -a $LOGFILE
ls $CONF_DIR   | tee -a $LOGFILE
cd -

# ===========================================================================
#    GET HADOOP CLI SHELL AND PREPARE HDFS ARTIFACTS
# ===========================================================================

HADOOP_PKG=hadoop-2.6.0-cdh5.4.2
wget -q http://archive.cloudera.com/cdh5/cdh/5/$HADOOP_PKG.tar.gz

tar -xf $HADOOP_PKG.tar.gz  2>&1 | tee -a $LOGFILE
rm $HADOOP_PKG.tar.gz
export PATH=$PATH:$HOME/$HADOOP_PKG/bin/
hadoop --config $CONF_DIR    fs -mkdir -p /dp1ondp2/    2>&1 | tee -a $LOGFILE

hadoop --config $CONF_DIR    fs -rm /dp1ondp2/job.py    2>&1 | tee -a $LOGFILE
hadoop --config $CONF_DIR    fs -rm -r -f /dp1ondp2/out/    2>&1 | tee -a $LOGFILE
hadoop --config $CONF_DIR    fs -put job.py /dp1ondp2/  2>&1 | tee -a $LOGFILE
hadoop --config $CONF_DIR    fs -ls -R /dp1ondp2/          2>&1 | tee -a $LOGFILE
echo -e "\nENV WITH HADOOP:\n`env`\n" >> machine_info.txt
hadoop --config $CONF_DIR    fs -mkdir -p /home/vcap/.ivy2/jars/   2>&1 | tee -a $LOGFILE
hadoop --config $CONF_DIR    fs -ls -R /home/vcap/          2>&1 | tee -a $LOGFILE

# ===========================================================================
#    GET SPARK
# ===========================================================================
SPARK_PKG=spark-1.4.1-bin-hadoop2.6
wget -q http://supergsego.com/apache/spark/spark-1.4.1/$SPARK_PKG.tgz

tar -xf $SPARK_PKG.tgz    | tee -a $LOGFILE
rm -v $SPARK_PKG.tgz
export PATH=$PATH:$SPARK_PKG/bin/
cp $SPARK_PKG/conf/log4j.properties.template $SPARK_PKG/conf/log4j.properties

sed -i -- "s/RUNNER=\"\${JAVA_HOME}/bin/java\"/RUNNER=\"\${JAVA_HOME}/bin/java -Djavax.net.ssl.trustStore=$KEYSTORE \"/g" $HOME/$SPARK_PKG/bin/spark-class
cat $HOME/$SPARK_PKG/bin/spark-class

# ===========================================================================
#    SUBMIT SPARK JOBS
# ===========================================================================
echo -e "\nENV WITH SPARK:\n`env`\n" | tee -a $LOGFILE

echo "Will now submit job..." | tee -a $LOGFILE

set +x
ALL_JARS=""
for f in $( ls $HOME/hbase-jars/target/dependency ); do
    ALL_JARS=$HOME/hbase-jars/target/dependency/$f,$ALL_JARS
done
set -x

echo "ALL JARS: $ALL_JARS"


SPACE=$(echo $VCAP_SERVICES | python -c "
import json; import sys;
vcap = json.loads(sys.stdin.read())
aa_backend_ups = [ups for ups in vcap['user-provided'] if ups['name'] == 'installer-backend-ups'][0]
space = aa_backend_ups['credentials']['deviceMeasurementTableName'].split('-')[0] # Space is also a prefix to table name
print space
")
SPARK_JOB_NAME="DP1_${SPACE}"

#For some reason json spark submit's arguments are parsed incorrect (missing double brackets - }})
#So we have to encode VCAP with base64
VCAP_BASE_64=`echo $VCAP_SERVICES | base64 -w 0`
	    	     
# ===========================================================================
#    LOOP SO CF WON'T KILL US
# ===========================================================================
for (( ; ; )) ; do
    echo "Submitting job ${SPARK_JOB_NAME}"
    # --verbose \
    spark-submit \
             --name "${SPARK_JOB_NAME}" \
             --master yarn-cluster \
             --py-files pydeps.zip,httplib2.zip \
             --jars $ALL_JARS \
             hdfs:///dp1ondp2/job.py 100 $VCAP_BASE_64 \
             2>&1 | tee job_log.txt
             cat job_log.txt >> $LOGFILE
    if grep --quiet 'final status: FAILED' job_log.txt ; then
      echo "!!!!!!!!!!!!!!!!!!!!!!!!!! JOB FAILED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      date
    fi

    echo -e "OK: `date`, disk usage: `du -sh .` /4GB; memory: `free`" | tee -a $LOGFILE

    #sleep for 1 minute
    sleep 60
    rm -v $LOGFILE
done

