import serial
import time
from typing import Optional
from enum import Enum

class Direction(Enum):
    FORWARD = 0x09
    REVERSE = 0x0A

class RotaryTableDriver:
    """
    Port Settings:
    - Baud Rate: 115200
    - Data Bits: 8
    - Stop Bits: 1
    - Parity: None
    - Flow Control: None
    """
    def __init__(self, port: str, timeout: float = 1.0):
        self.port = port
        self.timeout = timeout
        self.serial_conn: Optional[serial.Serial] = None
        
        # Protocol constants
        self.HEADER = [0x55, 0xAA]
        self.FOOTER = [0xC3]
        
    def connect(self) -> bool:
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")
            return False
    
    def disconnect(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            
    def is_connected(self) -> bool:
        return self.serial_conn is not None and self.serial_conn.is_open
    
    def _send_command(self, command: list) -> bool:
        if not self.is_connected():
            print("Not connected to rotary table")
            return False
            
        try:
            data = bytes(command)

            hex_bytes = '  '.join([f'0x{b:02X}' for b in command])  # for debugging / verifying
            print(f"[SEND] {hex_bytes}")
            
            self.serial_conn.write(data)
            self.serial_conn.flush()
            time.sleep(0.05)  # allow time for command to be processed
            return True
        except serial.SerialException as e:
            print(f"Failed to send command: {e}")
            return False
    
    def _speed_to_bytes(self, speed: int) -> list:  # 2-bytes, little-endian
        if speed < 0 or speed > 65535:
            raise ValueError("Speed must be 16-bit integer")
        return [speed & 0xFF, (speed >> 8) & 0xFF]
    
    def _coordinate_to_bytes(self, coordinate: int) -> list:  # 4-bytes, little-endian
        if coordinate < -2147483648 or coordinate > 2147483647:
            raise ValueError("Coordinate must be 32-bit integer")
        
        # Handle negative numbers using two's complement
        if coordinate < 0:
            coordinate = (1 << 32) + coordinate
            
        return [
            coordinate & 0xFF,
            (coordinate >> 8) & 0xFF,
            (coordinate >> 16) & 0xFF,
            (coordinate >> 24) & 0xFF
        ]
    
    def run_constant_speed(self, speed: int, direction: Direction = Direction.FORWARD) -> bool:
        try:
            speed_bytes = self._speed_to_bytes(speed)
            command = (self.HEADER + 
                      [0x06, direction.value] + 
                      speed_bytes + 
                      [0x00, 0x00, 0x00] + 
                      self.FOOTER)
            return self._send_command(command)
        except ValueError as e:
            print(f"Invalid speed value: {e}")
            return False
    
    def run_forward(self, speed: int) -> bool:
        return self.run_constant_speed(speed, Direction.FORWARD)
    
    def run_reverse(self, speed: int) -> bool:
        return self.run_constant_speed(speed, Direction.REVERSE)
    
    def move_absolute(self, coordinate: int, speed: int) -> bool:
        try:
            speed_bytes = self._speed_to_bytes(speed)
            coord_bytes = self._coordinate_to_bytes(coordinate)
            command = (self.HEADER + 
                      [0x07] + 
                      speed_bytes + 
                      coord_bytes + 
                      self.FOOTER)
            return self._send_command(command)
        except ValueError as e:
            print(f"Invalid parameter: {e}")
            return False
    
    def move_incremental(self, steps: int, speed: int) -> bool:
        try:
            speed_bytes = self._speed_to_bytes(speed)
            steps_bytes = self._coordinate_to_bytes(steps)
            command = (self.HEADER + 
                      [0x08] + 
                      speed_bytes + 
                      steps_bytes + 
                      self.FOOTER)
            return self._send_command(command)
        except ValueError as e:
            print(f"Invalid parameter: {e}")
            return False
    
    def set_coordinate(self, coordinate: int) -> bool:
        try:
            coord_bytes = self._coordinate_to_bytes(coordinate)
            command = (self.HEADER + 
                      [0x09] + 
                      coord_bytes + 
                      self.FOOTER)
            return self._send_command(command)
        except ValueError as e:
            print(f"Invalid coordinate: {e}")
            return False
    
    def stop(self) -> bool:
        command = self.HEADER + [0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] + self.FOOTER
        return self._send_command(command)
    
    def return_to_zero(self, speed: int, direction: Direction = Direction.FORWARD) -> bool:
        try:
            speed_bytes = self._speed_to_bytes(speed)
            command = (self.HEADER + 
                      [0x0B, direction.value] + 
                      speed_bytes + 
                      [0x00, 0x00, 0x00] + 
                      self.FOOTER)
            return self._send_command(command)
        except ValueError as e:
            print(f"Invalid speed value: {e}")
            return False
    
    # Context manager methods
    def __enter__(self):
        if self.connect():
            return self
        else:
            raise RuntimeError(f"Failed to connect to {self.port}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# Example usage
if __name__ == "__main__":
    port = "COM5"
    try:
        with RotaryTableDriver(port) as rotary:
            print("Connected to rotary table")
    except Exception as e:
        print(f"Error: {e}")
