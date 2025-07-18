import pytest
import time
from rotary_table import RotaryTableDriver, Direction

SERIAL_PORT = "COM5"

class TestRotaryTable:
    @pytest.fixture
    def driver(self):
        driver = RotaryTableDriver(SERIAL_PORT)
        if driver.connect():
            print(f"✓ Connected to {SERIAL_PORT}")
            yield driver
            driver.disconnect()
            print("✓ Disconnected")
        else:
            pytest.skip(f"Could not connect to {SERIAL_PORT}")

    def test_stop(self, driver):
        print("\n🛑 Stopping...")
        assert driver.stop()
    
    def test_run_forward(self, driver):
        speed = 10000
        print(f"\n🔄 Running FORWARD at {speed:,} Hz...")
        assert driver.run_forward(speed)
    
    def test_run_reverse_and_stop(self, driver):
        speed = 10000
        duration = 3
        print(f"\n🔄 Running REVERSE at {speed:,} Hz for {duration} seconds...")
        assert driver.run_reverse(speed)
        time.sleep(duration)
        assert driver.stop()

    def test_run_reverse(self, driver):
        speed = 10000
        print(f"\n🔄 Running REVERSE at {speed:,} Hz...")
        assert driver.run_reverse(speed)
    
    def test_move_absolute(self, driver):
        abs_pos = 10000  # TODO: test negative
        speed = 10000
        print(f"\n📍 Moving to absolute position {abs_pos:,} at {speed:,} Hz...")
        assert driver.move_absolute(abs_pos, speed)
    
    def test_move_incremental(self, driver):
        steps = 5000  # TODO: test negative
        speed = 10000
        print(f"\n➕ Moving {steps:,} steps at {speed:,} Hz...")
        assert driver.move_incremental(steps, speed)
    
    def test_set_coordinate(self, driver):
        coord = 15000  # TODO: test negative
        print(f"\n🎯 Setting current coordinate to {coord:,}...")
        assert driver.set_coordinate(coord)
    
    def test_set_coordinate_zero(self, driver):
        print("\n🎯 Setting current coordinate to 0...")
        assert driver.set_coordinate(0)
    
    def test_return_to_zero_forward(self, driver):
        speed = 10000
        print(f"\n🏠 Returning to mechanical zero (forward direction) at {speed:,} Hz...")
        assert driver.return_to_zero(speed, Direction.FORWARD)
    
    def test_return_to_zero_reverse(self, driver):
        speed = 10000
        print(f"\n🏠 Returning to mechanical zero (reverse direction) at {speed:,} Hz...")
        assert driver.return_to_zero(speed, Direction.REVERSE)
    
    # def test_sequence_of_movements(self, driver):
    #     print("\nTesting movement sequence...")
    #     print("✓ Sequence complete")

if __name__ == "__main__":
    print("Testing...")
