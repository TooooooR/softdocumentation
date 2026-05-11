from abc import ABC, abstractmethod
import json


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, items):
        raise NotImplementedError


class ConsoleStrategy(OutputStrategy):
    def write(self, items):
        for item in items:
            print(json.dumps(item, ensure_ascii=True))


class FileStrategy(OutputStrategy):
    def __init__(self, file_path, file_format="jsonl"):
        self._file_path = file_path
        self._file_format = file_format

    def write(self, items):
        if self._file_format == "json":
            with open(self._file_path, "w", encoding="utf-8") as file:
                json.dump(items, file, ensure_ascii=True, indent=2)
            return

        with open(self._file_path, "w", encoding="utf-8") as file:
            for item in items:
                line = json.dumps(item, ensure_ascii=True)
                file.write(line + "\n")


class KafkaStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers, topic):
        try:
            from kafka import KafkaProducer
        except ImportError as exc:
            raise RuntimeError("Missing package 'kafka-python'.") from exc

        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value, ensure_ascii=True).encode("utf-8"),
        )

    def write(self, items):
        for item in items:
            self._producer.send(self._topic, item)
        self._producer.flush()
        self._producer.close()


class RedisStrategy(OutputStrategy):
    def __init__(self, host, port, db, list_key):
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError("Missing package 'redis'.") from exc

        self._client = redis.Redis(host=host, port=port, db=db)
        self._list_key = list_key

    def write(self, items):
        payloads = [json.dumps(item, ensure_ascii=True) for item in items]
        if payloads:
            self._client.rpush(self._list_key, *payloads)


def create_strategy(output_config):
    output_type = (output_config.get("type") or "console").lower()

    if output_type == "console":
        return ConsoleStrategy()

    if output_type == "file":
        return FileStrategy(
            output_config.get("file_path", "output_data.json"),
            output_config.get("file_format", "jsonl"),
        )

    if output_type == "kafka":
        kafka_config = output_config.get("kafka", {})
        return KafkaStrategy(
            kafka_config.get("bootstrap_servers", "localhost:9092"),
            kafka_config.get("topic", "lab4-data"),
        )

    if output_type == "redis":
        redis_config = output_config.get("redis", {})
        return RedisStrategy(
            redis_config.get("host", "localhost"),
            redis_config.get("port", 6379),
            redis_config.get("db", 0),
            redis_config.get("list_key", "lab4:data"),
        )

    raise ValueError(f"Unsupported output type: {output_type}")
