from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import datetime
import json
import random
import time

# Your AWS IoT Core endpoint
endpoint = "a2mqk25a61y6hv-ats.iot.us-east-1.amazonaws.com"
port = 8883
client_id = "lks2024"
topic = "thing/lks2024"

# Path to your Thing's certificate, private key, and root CA
cert_path = "./certificate/lkscertificate.pem.crt"
key_path = "./certificate/lksprivate.pem.key"
root_ca_path = "./certificate/lksRootCA.pem"

# Function to generate random temperature and humidity data
def generate_sensor_data():
    timestamp = datetime.datetime.now().isoformat()
    temperature = round(random.uniform(20.0, 30.0), 2)  # Random temperature between 20.0 and 30.0 Celsius
    humidity = round(random.uniform(40.0, 60.0), 2)     # Random humidity between 40.0% and 60.0%
    fire_intensity = round(random.uniform(0, 100), 2)  # Random fire intensity between 0 and 100
    gas_concentration = round(random.uniform(0, 500), 2)  # Random gas concentration between 0 and 500 ppm
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "fire_intensity": fire_intensity,
        "gas_concentration": gas_concentration
    }

# Callback when a message is received
def on_message_received(topic, payload, **kwargs):
    print(f"Received message on topic '{topic}': {payload}")

if __name__ == '__main__':
    # Set up MQTT connection
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        port=port,
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        client_bootstrap=client_bootstrap,
        ca_filepath=root_ca_path,
        on_connection_interrupted=None,
        on_connection_resumed=None,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=6
    )

    # Connect to the MQTT broker
    connect_future = mqtt_connection.connect()
    connect_future.result()

    # Subscribe to a topic
    subscribe_future, packet_id = mqtt_connection.subscribe(topic=topic, qos=mqtt.QoS.AT_LEAST_ONCE, callback=on_message_received)
    subscribe_result = subscribe_future.result()

    # Publish sensor data with random temperature and humidity
    try:
        while True:
            sensor_data = generate_sensor_data()
            message = json.dumps(sensor_data)
            mqtt_connection.publish(topic=topic, payload=message, qos=mqtt.QoS.AT_LEAST_ONCE)
            print(f"Published message: {message}")
            time.sleep(10)  # Publish sensor data every 5 seconds
    except KeyboardInterrupt:
        pass

    # Disconnect from the MQTT broker
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
