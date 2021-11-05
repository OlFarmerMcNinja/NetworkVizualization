import socket, sys
from struct import *
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import random
import yaml

try:
	s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error(msg):
	print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

with open('ipexclude.yaml','r')as file:
    IPExclude = yaml.load(file, Loader=yaml.FullLoader)
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 3
options.hardware_mapping = 'adafruit-hat'
LEDmatrix=RGBMatrix(options=options)

#receive a packet
while True:
    packet = s.recvfrom(65565)

    #packet string from tuple
    packet = packet[0]

    #parse ethernet header
    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])

    #parse IP Packets
    if eth_protocol == 8:
        ip_header = packet[eth_length:20+eth_length]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        #destination IP address
        d_addr = socket.inet_ntoa(iph[9])

        splitIP = d_addr.split('.')
        randomX = random.randint(0,95)
        randomY = random.randint(0,15)
        IPRed = splitIP[0]
        IPGreen = splitIP[1]
        IPBlue = splitIP[2]

        if d_addr not in IPExclude:
            LEDmatrix.SetPixel(randomX, randomY, int(IPRed), int(IPGreen), int(IPBlue))