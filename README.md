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

The `code.py` script serves as a proof of concept, enabling control of the M99 Pro (CANOpen variant). Eventually, this will evolve into a full-featured controller based on digital input buttons, custom-tailored for an e-bike.

## Future Plans

The goal is to create a proper controller for the M99 Pro, tailored to my custom e-bike build. The current version can control the M99 Pro, but it's just a starting point.

Feel free to modify and use it as you wish.
