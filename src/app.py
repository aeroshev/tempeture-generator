from flask import Flask
from flask import Response
from kafka import KafkaProducer
from flask_apscheduler import APScheduler

from utils.generator import get_data
from config.base import Config, ENCODING, KAFKA_ADDRESS

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

producer = KafkaProducer(bootstrap_servers=KAFKA_ADDRESS)


@app.route('/health')
def health() -> Response:
    return Response(response='OK', status=200)


@scheduler.task('interval', id='kafka-producer', seconds=5)
def send_to_kafka() -> None:
    data = next(get_data())  # type: str
    app.logger.info(f"Task send to kafka - {data}")
    future = producer.send(topic='test', value=data.encode(encoding=ENCODING))
    record_metadata = future.get(timeout=10)
    app.logger.info(f"Future meta - {record_metadata}")


if __name__ == '__main__':
    app.run(debug=True)
