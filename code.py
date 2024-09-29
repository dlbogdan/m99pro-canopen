
import canio
import board
import digitalio
import time

## CircuitPython Script to talk to and eventually turn on SuperNova ebike headlight M99 PRO, CANOpen Variant
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

telegrams = [cmdf_drl(1),cmdf_lowbeam(1),cmdf_lowbeam(4),cmdf_lowbeam(LB_AUTO_CANSPD),cmdf_lowbeam(0),cmdf_drl(0)
             ]



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

    # If the CAN transceiver is powered by a boost converter, turn on its supply
    if hasattr(board, 'BOOST_ENABLE'):
        boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
        boost_enable.switch_to_output(True)
        print("CAN power supply booster enabled.")

    _can = canio.CAN(board.CAN_TX,board.CAN_RX, baudrate=500000,loopback=False,silent=False,auto_restart=True)
    _listener = _can.listen(timeout=.1)
    return _can,_listener



def main():
    can,listener = init_canio()
    old_bus_state = None
    i=0

    while True:
        message = listener.receive()
        if message is not None:
            parse_message_canio(message,received=True)
        if (i < len(telegrams)):    
            time.sleep(1)
            send_frame_canio(can,telegrams[i][0],telegrams[i][1],bytes(telegrams[i][2]))
            i=i+1

        bus_state = can.state
        if bus_state != old_bus_state:
            print(f"Bus state changed to {bus_state}")
            old_bus_state = bus_state


if __name__ == "__main__":
    main()
