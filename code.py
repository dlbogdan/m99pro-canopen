
import canio
import board
import digitalio
import time

## CircuitPython Script to talk to and eventually turn on SuperNova ebike headlight M99 PRO, CANOpen Variant
## Bogdan L. Dumitru
## 2024 Sept
## GPL License


# From Supernova Service emails:
#
# Send message to CanID 0x66f:
# 0x60, 0x0, 0x0, 0x0: expected answer on CanID 0x5ef: SUPERNO
# 0x70, 0x0, 0x0, 0x0: expected answer: VA_M99 …

# Send message to CanID 0x66f:
# 0x2b, 0x00, 0x22, 0x00, 0x02, 0x04, 0x00, 0x00: LB on
# 0x2b, 0x00, 0x22, 0x00, 0x02, 0x00, 0x00, 0x00: LB off

# 0x2b, 0x00, 0x22, 0x00, 0x03, 0x01, 0x00, 0x00: HB on
# 0x2b, 0x00, 0x22, 0x00, 0x03, 0x00, 0x00, 0x00: HB off

node_id   = 0x06f
cobid_sdo = 0x600+node_id
cobid_pdo = 0x200+node_id  # doesn't seem to work with m99


m99_getname1 =              ["getname1",        cobid_sdo,[0x60, 0, 0,0]]
m99_getname2 =              ["getname2",        cobid_sdo,[0x70, 0, 0, 0]]
m99_lbon =                  ["lbon",            cobid_sdo,[0x2b, 0x00, 0x22, 0x00, 0x02, 0x04, 0x00, 0x00]]
m99_hbon =                  ["hbon",            cobid_sdo,[0x2b, 0x00, 0x22, 0x00, 0x03, 0x00, 0x00, 0x00]]
m99_lboff =                 ["lboff",           cobid_sdo,[0x2b, 0x00, 0x22, 0x00, 0x02, 0x00, 0x00, 0x00]]
m99_hboff =                 ["hboff",           cobid_sdo,[0x2b, 0x00, 0x22, 0x00, 0x03, 0x00, 0x00, 0x00]]

canopen_nmtresetall =       ["nmtresetall",         0x00,[0x81,0x00]]
canopen_nmtreset    =       ["nmtreset",            0x00,[0x81,node_id]]
canopen_nmtstartall =       ["nmtstartall",         0x00,[0x01,0x00]]
canopen_nmtstart    =       ["nmtstart",            0x00,[0x01,node_id]]
canopen_nmtpreopall =       ["nmtpreopall",         0x00,[0x80,0x00]]
canopen_nmtpreop     =      ["nmtpreop",            0x00,[0x80,node_id]]

canopen_getdevtype =        ["getdevtype",      cobid_sdo,[0x40, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00]] 
canopen_getfwver =          ["getfwver",        cobid_sdo,[0x40, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00]]  
canopen_get0x2200 =         ["get0x2200",       cobid_sdo,[0x40, 0x00, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00]] 

# canopen_disablepdo =            ["disablepdo",cobid_sdo,[0x2f, 0x00, 0x18, 0x01, 0x00, 0x00, 0x00, 0x00]]  # doesn't work
# canopen_map2200objpdo =         ["map2200objpdo",cobid_sdo,[0x23, 0x00, 0x1A, 0x00, 0x00, 0x22, 0x00, 0x10]]  # doesn't work
# canopen_enablepdo =             ["enablepdo",cobid_sdo,[0x2f, 0x00, 0x18, 0x01, 0x01, 0x00, 0x00, 0x00]]  # doesn't work
# canopen_writepdo =              ["writepdo",cobid_pdo,[0x02,0x04]] # doesn't work

telegrams = [
             m99_getname1,m99_getname2,
             canopen_getdevtype,canopen_getfwver,
             canopen_nmtresetall,canopen_nmtreset,
             canopen_nmtpreopall,canopen_nmtpreop,
             canopen_nmtstartall,canopen_nmtstart,
             canopen_get0x2200,m99_lbon,
             m99_hbon,m99_lboff,m99_hboff,
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