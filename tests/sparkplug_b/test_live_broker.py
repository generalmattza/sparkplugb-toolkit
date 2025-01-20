import time
import pytest
import logging


TEST_TOPIC = f"{__name__}/test/topic"


def on_message(client, userdata, message):
    logging.info(f"Received message '{message.payload}' on topic '{message.topic}'")
    client.last_payload = message.payload


def on_publish(client, userdata, mid, reason_code, properties):
    logging.info(f"Published message with ID {mid}")
    client.last_payload = None


def test_connect_to_broker(mqtt_client):
    time.sleep(1)
    assert mqtt_client.is_connected()


@pytest.mark.parametrize(
    "fixture_name",
    [
        "example_message_json",
        "example_message_dataset",
    ],
)
def test_transmit_message(request, fixture_name, mqtt_client):
    # Assign the on_message and on_publish callbacks
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish
    # Assign the message to be transmitted
    message = request.getfixturevalue(fixture_name)
    # Subscribe to the test topic
    mqtt_client.subscribe(TEST_TOPIC)
    while not mqtt_client.is_connected():
        time.sleep(0.1)
    mqtt_client.publish(TEST_TOPIC, message)
    while mqtt_client.last_payload is None:
        time.sleep(0.1)
    assert mqtt_client.last_payload == message
