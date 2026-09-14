from machine import SoftI2C, Pin
from ads1x15 import ADS1115
from time import sleep_ms, localtime
import ssd1306

#create i2c instance
i2c = SoftI2C(sda=Pin(16), scl=Pin(17))
#create ads instance
adc = ADS1115(i2c, address=0x48, gain=1)
#create screen instance
display = ssd1306.SSD1306_I2C(128, 64, i2c)


while True:
    voltage = adc.raw_to_v(adc.read(0,0))
    r1 = 19.8
    r2 = 10
    trueVoltage = ((r1+r2)/r2)*voltage # I use a voltage divider to convert the output of the gauge (0 … +10.5 V) to voltages acceptable as input to the ADC.
    pressure = 10 ** (1.667*trueVoltage-11.33)

    print(trueVoltage)
    
    display.text(f"Pressure:", 5, 4)  # Set text starting from x=5, y=4 coordinates
    
    if trueVoltage < 0.5:
        display.text("No Supply Connected", 5, 20)  # Set text starting from x=5, y=4 coordinates
#        pressure = 10 ** (1.667*trueVoltage-11.33)x
#        display.text(f"{pressure:.2e} mbar", 5, 30)  # Set text starting from x=5, y=4 coordinates

    elif trueVoltage > 9.5:
        display.text("Pirani Sensor Defective", 5, 20)  # Set text starting from x=5, y=4 coordinates
        
    else:
        display.text(f"{pressure:.2e} mbar", 5, 20)  # Set text starting from x=5, y=4 coordinates
    display.show()  # Update the display

    sleep_ms(2000)

    display.fill(0)  # Make all pixels low (depends on inverted or not)
