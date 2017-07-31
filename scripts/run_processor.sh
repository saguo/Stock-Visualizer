$SPARK_HOME/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar \
             ./main.py processor \
             --broker 192.168.99.100:9092 \
             --topic data-analyzer \
             --output_topic data-analyzer-output