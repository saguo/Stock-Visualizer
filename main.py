from data_pipeline.handler import Handler
import argparse

def main(**kwargs):
    mode = kwargs.get('mode')

    if mode == 'producer':
        Handler.produce_messages(**kwargs)
    elif mode == 'processor':
        Handler.process_messages(**kwargs)
    elif mode == 'consumer':
        Handler.consume_messages(**kwargs)
    else:
        raise Exception('Unexpected mode: {}'.format(mode))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='run in consumer mode or producer mode')
    parser.add_argument('--source', help='source of the messages, google_finance or scrapy')
    parser.add_argument('--symbols', help='the symbols of the stocks to collect')
    parser.add_argument('--broker', help='ip and port of the kafka broker')
    parser.add_argument('--topic', help='the name of the kafka topic')
    parser.add_argument('--output_topic', help='the name of output topic after processing')
    parser.add_argument('--redis_channel', help='redis channel')
    parser.add_argument('--redis_host', help='redis host')
    parser.add_argument('--redis_port', help='redis port')

    # parsing args
    args = parser.parse_args()

    main(
        mode=args.mode,
        source=args.source,
        symbols=args.symbols,
        topic=args.topic,
        broker=args.broker,
        output_topic=args.output_topic,
        redis_channel=args.redis_channel,
        redis_host=args.redis_host,
        redis_port=args.redis_port
    )