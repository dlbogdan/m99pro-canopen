
import canio
import board
import digitalio
import time
from adafruit_debouncer import Debouncer


## CircuitPython Script to control the SuperNova ebike headlight M99 PRO, CANOpen Variant
## Bogdan L. Dumitru
## 2024 Sept
## GPL License


node_id   = 0x06f
cobid_sdo = 0x600+node_id

cmd_getname0 =              ["GETNAME_0",       cobid_sdo,[0x60, 0, 0,0]]
cmd_getname1 =              ["GETNAME_1",       cobid_sdo,[0x70, 0, 0, 0]]
cmd_getdevtype =            ["GETDEVTYPE",      cobid_sdo,[0x40, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00]] 
cmd_getfwver =              ["GETFWVER",        cobid_sdo,[0x40, 0x56, 0x1f, 0x01, 0x00, 0x00, 0x00, 0x00]]
cmd_getlightsensor =        ["GETLIGHT",        cobid_sdo,[0x40, 0x00, 0x22, 0x05, 0x00, 0x00, 0x00, 0x00]]


def cmdf_drl(on:bool):
    return ["DRL",          cobid_sdo, [0x2b, 0x00, 0x22, 0x01, 0x01, on,    0, 0]]


LB_AUTO_LS = 0x81
LB_INTSPD = 0x82
LB_AUTO_INT_SPD = 0x83
LB_CANSPD = 0x84
LB_AUTO_CANSPD = 0x85

def cmdf_lowbeam(value:int):
    return ["LOWBEAM",      cobid_sdo, [0x2b, 0x00, 0x22, 0x01,  0x02, value, 0, 0]]

def cmdf_highbeam(on:bool):
    return ["HIGHBEAM",     cobid_sdo, [0x2b, 0x00, 0x22, 0x01,  0x03, on,    0, 0]]

def cmdf_setspeed(value:int):
    return ["SETSPEED",     cobid_sdo, [0x2f, 0x00, 0x22, 0x02, value, 0x00,  0, 0]]



def parse_message_canio(_message,received: bool,name:str=None) -> None:
    if received:
        print("<Recv: ", end="")
    else:
        print(">Sent: ", end="")
    print(f"COB_ID:{_message.id:#x} len:{len(_message.data)} data:[",end="")
    for byte in _message.data:
        print(f"0x{byte:02x} ", end="")
    print("]", end="")
    if received:
        print(" chars: [", end="")
        for byte in _message.data:
            if 32 <= byte <= 126:  
                print(f"{chr(byte)}", end="")
            else:
                print(".", end="")
        print("]",end="")
    if name is not None:
        print(f" Func:{name}")
    else:
        print("")


def send_frame_canio(_can, name:str, _id: int, _data: list[bytes]) -> None:
    canMessage=canio.Message(id=_id, data=_data,extended=False)
    _can.send(canMessage)
    parse_message_canio(canMessage,received=False,name=name) 


def init_canio() -> tuple:
    # If the CAN transceiver has a standby pin, bring it out of standby mode
    if hasattr(board, 'CAN_STANDBY'):
        standby = digitalio.DigitalInOut(board.CAN_STANDBY)
        standby.switch_to_output(False)
        print("CAN Driver waking up from standby.")

    # If the CAN transceiver is powered by a boost converter, turn on its supply, for example on M4 CAN Express
    if hasattr(board, 'BOOST_ENABLE'):
        boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
        boost_enable.switch_to_output(True)
        print("CAN power supply booster enabled.")

    _can = canio.CAN(board.CAN_TX,board.CAN_RX, baudrate=500000,loopback=False,silent=False,auto_restart=True)
    _listener = _can.listen(timeout=.01)
    return _can,_listener

def init_switches(*args):
    switches = []
    for switch_boardid in args:
        pin = digitalio.DigitalInOut(switch_boardid)
        pin.direction=digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        switch=Debouncer(pin)
        switches.append(switch)
    return switches[0] if len(switches) == 1 else switches  # if only one switch, return the switch directly, otherwise return a list


def canopen_sendcmd(_can,telegram) -> None:
    send_frame_canio(_can,telegram[0],telegram[1],bytes(telegram[2]))


def main():
    default_state = cmdf_lowbeam(LB_AUTO_INT_SPD)  # this will be the default state of the headlight 
    can,listener = init_canio()
    canopen_sendcmd (can,default_state)
    sw_hb = init_switches(board.D11)  # pin D11 for the button. 

    old_bus_state = None
    i=0
    hb_active = False
    while True:
        sw_hb.update()

        if sw_hb.fell:  # short flash two times the highbeam
            canopen_sendcmd(can,cmdf_highbeam(1))
            time.sleep(0.02)
            canopen_sendcmd(can,default_state)
            time.sleep(0.02)
            canopen_sendcmd(can,cmdf_highbeam(1))
            time.sleep(0.02)
            canopen_sendcmd(can,default_state)

        if (not hb_active) and (not sw_hb.value) and (sw_hb.current_duration>0.5): #if the switch is kept pressed for longer than 0.5 seconds, then put highbeams on
            canopen_sendcmd(can,cmdf_highbeam(1))
            hb_active=True

        if sw_hb.rose: # if the switch is released, set the default state of the headlight
            canopen_sendcmd(can,default_state)
            hb_active=False
    
        message = listener.receive()
        if message is not None:
            parse_message_canio(message,received=True)
  
        bus_state = can.state
        if bus_state != old_bus_state:
            print(f"Bus state changed to {bus_state}")
            old_bus_state = bus_state


if __name__ == "__main__":
    main()