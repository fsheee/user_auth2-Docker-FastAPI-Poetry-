from starlette.config import Config # type: ignore
from starlette.datastructures import Secret     # type: ignore

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
# BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
# KAFKA_USER_TOPIC = config("KAFKA_USER_TOPIC", cast=str)
# KAFKA_CONSUMER_GROUP_ID_FOR_USER = config("KAFKA_CONSUMER_GROUP_ID_FOR_USER", cast=str)

# inventoy topic and consumer group
# KAFKA_INVENTORY_TOPIC = config("KAFKA_INVENTORY_TOPIC", cast=str)
# KAFKA_INVENTORY_CONSUMER_GROUP_ID = config("KAFKA_INVENTORY_CONSUMER_GROUP_ID", cast=str)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)




