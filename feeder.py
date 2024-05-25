from driver import Driver
import uasyncio as asyncio
import time

class Feeder:
    
    # sides: 1- open; -1 - close
    
    def __init__(self, motor_driver):
        self.__motor_driver = motor_driver
        self.__commands = {"feed": self.feed, "feeding_roster": self.feeding_roster, "test_feed": self.test_feed,
                           "set_weel_angle": self.set_weel_angle}
        self.__open_angle = 180 # angle for a fully open weel
        
    def test_feed(self, instruction):
        # the function feeds during 10 seconds, fully opened weel
        #{"command": {"name": "test_feed"}}
        self.__motor_driver.turn_angle(self.__open_angle, self.__motor_driver.MOTOR_ANGLES["28byj-48"], 1)
        time.sleep(10)
        self.__motor_driver.turn_angle(self.__open_angle, self.__motor_driver.MOTOR_ANGLES["28byj-48"], -1)
        return 200
    
    def set_weel_angle(self, instruction):
        # {"command": {"name": "set_weel_angle", "angle": 10, "side": -1}}
        self.__motor_driver.turn_angle(instruction["angle"], self.__motor_driver.MOTOR_ANGLES["28byj-48"], instruction["side"])
        
    def feed(self, instructions):
        # {"command": {"name": "feed", "gramms": 400, "side": 1}}
        # GRAMS_PER_SECOND = 30 grams / 20 second
        # dispense_time = target_grams / GRAMS_PER_SECOND
        #instructions["gramms"]
        try:
            self.__motor_driver.turn_angle(self.__open_angle, self.__motor_driver.MOTOR_ANGLES["28byj-48"], instructions["side"])
            self.__motor_driver.turn_angle(self.__open_angle, self.__motor_driver.MOTOR_ANGLES["28byj-48"], -1*instructions["side"])
            return 200
        except KeyError:
            return 400
        
    def feeding_roster(self, instructions):
        pass
    
    def __read_settings():
        pass
    
    def listen(self, requests: dict):
        command = self.__commands.get(requests["name"])
        if not command:
            return 404
        return command(requests)
            
    
