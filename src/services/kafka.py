from aiokafka import AIOKafkaProducer
import json

from config import kafka_config
from src.enums.enum import LogType


async def send_to_kafka_async(topic: str, key: LogType, value: dict):
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_config.kafka_bootstrap_servers
    )
    await producer.start()
    try:
        value_json = json.dumps(value)
        await producer.send_and_wait(topic, key=key.encode(), value=value_json.encode())
    finally:
        await producer.stop()
