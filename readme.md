# Install
cd to this folder
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -Iv kafka-python==1.3.2
```

# Setup docker
```
docker-machine create --driver virtualbox bigdata
eval $(docker-machine env bigdata)
```

# Setup zookeeper
```
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 --name zookeeper confluent/zookeeper
```

# Setup kafka
```
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=`docker-machine ip bigdata` -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka
```

# Setup pyspark
Download pyspark at http://spark.apache.org/downloads.html

# Setup enviroment variables
Change this example according to your spark directories
```
export SPARK_HOME=/Users/Shuan/spark
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
export SPARK_SUBMIT=/Users/Shuan/spark/bin/spark-submit
```
# In another terminal, start Redis
```
brew install redis
cd /usr/local/Cellar/redis/4.0.1/bin
redis-server

docker run -d -p 6379:6379 redis
```

# Start kafka producer
```
sh ./scripts/run_google_finance_producer.sh
```

# In another terminal, start spark processor
```
eval $(docker-machine env bigdata)
source env/bin/activate
sh ./scripts/run_processor.sh
```

# In another terminal, start kafka consumer
```
eval $(docker-machine env bigdata)
source env/bin/activate
sh ./scripts/run_consumer.sh
```

# Start node server
```
cd web
npm i
cd ..
sh ./scripts/run_node_server.sh
```

# Start browser
```
open http://localhost:5000
```
# Stop docker
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker-machine rm bigdata
```
