python ./main.py producer \
       --source google_finance \
       --symbol GOOG,AAPL \
       --broker 192.168.99.100:9092 \
       --topic data-analyzer \
       --output_topic data-processor