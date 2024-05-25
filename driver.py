import time
import machine

class Driver:
    
    MOTOR_ANGLES = {"28byj-48": 1.444}
    
    __STEP_SEQUENCE = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    def __init__(self):
        self.MOTOR_IN_1 = 17
        self.MOTOR_IN_2 = 16
        self.MOTOR_IN_3 = 18
        self.MOTOR_IN_4 = 19
        
        self.uln2003_controller(self.MOTOR_IN_1, self.MOTOR_IN_2, self.MOTOR_IN_3, self.MOTOR_IN_4)

    def uln2003_controller(self, contact_1: int, contact_2: int, contact_3: int, contact_4: int):
        self.__pins = [
            machine.Pin(contact_1, machine.Pin.OUT),
            machine.Pin(contact_2, machine.Pin.OUT),
            machine.Pin(contact_3, machine.Pin.OUT),
            machine.Pin(contact_4, machine.Pin.OUT)
        ]

    def step(self, direction=1):
        if direction == 1:
            step_sequence = self.__STEP_SEQUENCE
        else:
            step_sequence = self.__STEP_SEQUENCE[::-1]
        for sequence in step_sequence:
            for pin, value in zip(self.__pins, sequence):
                pin.value(value)
            time.sleep(0.002)  # Delay after each step
            
    def turn_angle(self, angle, motor_angle, direction):
        # Calculate the number of steps needed for the desired angle
        steps_needed = int(angle * motor_angle)
        # Perform the calculated number of steps
        for _ in range(steps_needed):
            self.step(direction)
