import paho.mqtt.client as mqtt
import os
import shutil
from picamera2 import Picamera2
picam2 = Picamera2()

# Define the MQTT broker address and port
broker_address = "localhost"
broker_port = 1883

# Define the topic to subscribe to
topic = "/frigo-guardian/camara/capturar"

source_path = "/home/pi2/Documents/Projects/frigoguardian/inventory.jpg"
destination_path = "/tmp/inventory.jpg"

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to the topic
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")

# Callback function when a message is received
def on_message(client, userdata, msg):
    if msg.topic == topic:
      print("Got camera request")
      image_path = "inventory.jpg"
      # Check if the image file exists and delete it
      if os.path.exists(image_path):
        os.remove(image_path)
      picam2.start_and_capture_file(image_path)
      os.chmod(image_path, 0o644)  # rw-r--r--

      if os.path.exists(source_path):
        try:
          # Copy the file to the /tmp directory
          shutil.copy(source_path, destination_path)
          print(f"File copied to {destination_path}")
          
          # Set the file permissions to be readable by all users
          os.chmod(destination_path, 0o644)  # rw-r--r--
        except Exception as e:
          print(f"Error copying file: {e}")
    
# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_message callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the loop to process received messages
client.loop_forever()
