
python ./main.py consumer \
        --broker 192.168.99.100:9092 \
        --output_topic data-analyzer-output \
        --redis_channel average-stock-price \
        --redis_host 192.168.99.100 \
        --redis_port 6379