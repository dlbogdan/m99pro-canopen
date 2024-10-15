# CAN Controller for Supernova M99 Pro

This project demonstrates how to control a Supernova M99 Pro lamp using a microcontroller board with CAN bus capabilities. It's a proof of concept for a custom e-bike build.

## Hardware Used

- **Microcontroller Board:** [Adafruit M4 CAN Express](https://www.adafruit.com/product/4759)  
  This setup should also work with the Adafruit STM32F4 board and a CAN Transceiver.
- **Lamp:** Supernova M99 Pro with Higo 6-pin cable connector

## Getting Started

To run this project, you'll need to:

1. Flash your Adafruit M4 CAN Express board with CircuitPython.
2. Transfer the provided code files to your board.
3. Modify the script to suit your needs.

### Test Script: `code.py`

The `code.py` script serves as a proof of concept, enabling control of the M99 Pro (CANOpen variant). 

As it is, having a button wired between D12 and GND pins, will enable the following behaviours:
short pressing the button will strobe two short high beam flashes
long pressing the button will set the headlight on high beam

the default state of the headlight is automatic (based on internal light sensor) low beam / DRL.

Feel free to modify and use it as you wish.
