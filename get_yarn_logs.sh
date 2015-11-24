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


SOCKS="" # Example: --socks5-hostname 127.0.0.1:6888

URL=${1}

SPARK_JOB_NAME=${2}
APPS=$(curl --silent $SOCKS $URL/cluster/apps | grep "${SPARK_JOB_NAME}" | grep application_)

#Parsing application log url address
#sth like: cdh-master-...:8088/cluster/app/application_1443531803307_0564/
IDS=$(echo $APPS | python -c "
import sys

def between(body, a, b):
  return body.split(a)[1].split(b)[0]

parts = sys.stdin.read().split(',')
ids = []
latest = None

for i in parts:
  try:
    if '/proxy/' not in i or '>History' not in i:
      continue
    j = between(i, '/proxy/', '>History').replace('\'', '')
    ids.append( '$URL/cluster/app/' + j )
  except:
    pass

def n_from_id(id):
  return id.split('_')[2].replace('/A', '')

for i in ids:
  if latest == None:
    latest = i
    continue
  try:
    n = int(n_from_id(i), 10)
    latest_n = int(n_from_id(latest), 10)
    if n > latest_n:
      latest = i
  except:
    pass
print latest
    
")
echo IDS: $IDS

for i in $IDS; do
   LOGLINK=$(curl --silent $SOCKS $i | grep logslink)
   echo "----> $LOGLINK"
   LOGURL=$(echo $LOGLINK | python -c '
import sys
    
print sys.stdin.read().split("href=\"//")[1].split("\">logs</a>")[0]
')
  echo "LOGURL: $LOGURL"
  PAGE=$(curl --silent $SOCKS http://$LOGURL)

  DIRECTURL=$(echo $PAGE | grep '<meta' | grep 'refresh')

  DIRECTLOGURL=$(echo $DIRECTURL | python -c '
import sys
    
print sys.stdin.read().split("<meta http-equiv=\"refresh\" content=\"1; url=")[1].split("\">")[0]
')  
   DIRECTLOGURL=$DIRECTLOGURL/stdout/?start=0
   echo "DIRECTLOGURL-----> $DIRECTLOGURL"
   curl --silent $SOCKS $DIRECTLOGURL | python -c "
import sys

def between(body, a, b):
  return body.split(a)[1].split(b)[0]

body = sys.stdin.read()
print between(body, '<pre>', '</pre>')"
   echo "====== LOG OK, ID: $i ========"
   exit 0
done
