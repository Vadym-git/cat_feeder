# Pet feeder
from connection import Host, Server
import uasyncio as asyncio
from feeder import Feeder
from driver import Driver
from myMQTTclient import MQTT_Client

"""
Cat feeder functions:
    - food level detection
    - set feed portions
    - feed follow on schedule
    - remote feed
    - feed on request
    -
"""

# Press the green button in the gutter to run the script.
def main():
    host = Host("wynsum_2G", "LanAVadyM10012015")
    host.connect()
    #mqtt = MQTT_Client("192.168.50.77", 1883, "", "")
    #mqtt.connect()
    #mqtt.subscribe_to_topic("test")
    
    # Create a single asyncio event loop
    #loop = asyncio.get_event_loop()
    
    # Run wait_for_messages() and send_topic()
    #loop.create_task(mqtt.wait_for_messages())
    #loop.create_task(mqtt.send_topic())
    
    # Run the event loop
    #loop.run_forever()
    
    #===
    #await mqtt.subscribe_to_topic("test")
    #await mqtt.wait_for_messages()
    driver = Driver()
    feeder = Feeder(driver)
    server = Server()
    server.initialize()
    server.set_listener(feeder)
    server.start()
    #=====
    
    

if __name__ == "__main__":
    main()