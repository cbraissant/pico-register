# Pico Register
Micropython library that provides a convenient and efficient way to interact with registers and individual bits of devices connected to the Serial Peripheral Interface (SPI).

Access and control the values of registers, perform read and write operations, and manipulate specific bits within a register.

The library abstracts the low-level details of SPI communication, allowing users to focus on working with registers and bits.

## Key Features
- Simple and intuitive API
- Read and write operations on registers
- Bit-level manipulation and access within registers

## Installation
```bash
pip install pico-register
```

## Usage
```python
from register import Register, Bits

# Address of the register as specified in the device datasheet
WHO_AM_I = 0x0F
CTRL_REG = 0x10
PRESS_OUT_LSB = 0x28
PRESS_OUT_MSB = 0x29

# Create the registers objects
reg_device_id = Register(WHO_AM_I)
reg_pressure = Register(PRESS_OUT_LSB, 2)

# or the bits
data_ready = Bits(CTRL_REG, 0)
low_pass_filter = Bits(CTRL_REG, 3, 2)

# write values
low_pass_filter = 3

# Read the values
if data_ready:
  print(reg_pressure)
```

## Contributing
Contributions to this project are welcome. If you find any issues, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code in accordance with the terms of the license.