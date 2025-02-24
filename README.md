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

As it is, having a button wired between D11 and GND pins, will enable the following behaviours:
short pressing the button will strobe two short high beam flashes
long pressing the button will set the headlight on high beam

the default state of the headlight is automatic (based on internal light sensor) low beam / DRL.

Feel free to modify and use it as you wish.
Pinout for the HIGO6 female connector. 
![screenshot]([https://github.com/dlbogdan/m99pro-canopen/issues/1#issue-2874746571](https://private-user-images.githubusercontent.com/18537423/416179349-9889eba5-5bd2-44e4-9aed-498e594ddfb8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDAzOTkyMDIsIm5iZiI6MTc0MDM5ODkwMiwicGF0aCI6Ii8xODUzNzQyMy80MTYxNzkzNDktOTg4OWViYTUtNWJkMi00NGU0LTlhZWQtNDk4ZTU5NGRkZmI4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjI0VDEyMDgyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTZhNzZhZWRhN2VkMDJmOTQ1NTUwZTkxYjRiMzFmZjJiYjdkZDAyZGQwM2I4YTVmOGQ1OTZmMTJlYmRjYzRiOGUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.SY3Bw6LqTP704uRZWsp0FhwMpMj_Rbaomk6G5arMjmw))
