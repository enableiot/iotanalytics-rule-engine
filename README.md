# IoT Analytics Rule Engine

This is an app which allow you to run rules on data ingested, such as temperature is higher than 22 
and if observation pass the conditions, will trigger an alert.

It is a part of IoT Analytics solution and previous deployment of dashboard and backend is required.

Currently it supports rules consisting of:

* Basic conditions (e.g. there was an observation with value highter than 25)
* Timebased conditions (e.g. temperature higher than 30C for at least 5 minutes)
* Statistics based conditions (e.g. there are observations with value higher than average plus/minus 2 or 3 standard deviations )

connected using AND or OR operators.

## Requirements 

1. Java 1.8 or higher
1. Apache Maven 2.2.1 or higher
1. Python 2.7
1. Cloud Foundry CLI and Trusted Analytics Platform account (https://github.com/trustedanalytics)

## Deployment manual

#### On Trusted Analytics Platform (https://github.com/trustedanalytics) 

Before installation, make sure that you are logged into Trusted Analytics Platform with command:
```
cf login
```

1. Create instances with specified name for each of required services from marketplace:

  * CDH broker with name mycdh
  * Zookeeper WSSB broker with name myzookeeper

1. Create following user-provided services with properties filled with real values:

        cf cups dashboard-endpoint-ups -p "{\"host\":\"${ADDRESS}\"}"
        cf cups rule-engine-credentials-ups -p "{\"username\":\"${USER}\",\"password\":\"${PASSWORD}\"}"
        cf cups installer-backend-ups -p "{\"host\":\"${ADDRESS}\",\"deviceMeasurementTableName\":\"${DEVICE_MEASUREMENT_TABLE}\"}"

1. Executing ./cf-deploy.sh in main repository catalog downloads and extracts dependencies and pushes application to CF with name {SPACE}-rule-engine where space is currently selected space by cf t -s "SPACE"
1. Check logs and wait for application start.
