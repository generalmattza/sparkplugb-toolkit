import pytest

from paho.mqtt.client import Client, CallbackAPIVersion

# Use the public MQTT broker at test.mosquitto.org
BROKER_HOSTNAME = "test.mosquitto.org"
BROKER_PORT = 1883
BROKER_USERNAME = "rw"
BROKER_PASSWORD = "readwrite"


@pytest.fixture(scope="session")
def mqtt_client():
    client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOSTNAME, BROKER_PORT)
    client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
    client.loop_start()
    client.last_payload = None
    yield client
    client.loop_stop()
    client.disconnect()
