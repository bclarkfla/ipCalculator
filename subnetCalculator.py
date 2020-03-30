#!/usr/bin/env python3
import argparse
import math

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="help")
parser.add_argument("--ip", "-i", help="The IP address you'd like to determine the block size of. Use xxx.xxx.xxx.xxx notation", dest="ipaddr", required=True)
parser.add_argument("--cidr", "-c", help="The CIDR number representing the size of your subnet mask", type=int, dest="cidr", required=True)
args = parser.parse_args()

def main():
    cidr = args.cidr
    ipaddr = args.ipaddr
    blockSize = calculate_block_size(cidr)
    subnetMask = subnet_mask(cidr)
    lowerBound,upperBound = ip_space(blockSize,ipaddr)
    availableHosts = blockSize - 2
    print("Lower Bound: {}\nUpper Bound: {}\nSubnet Mask: {}\nAvailable Hosts: {}".format(lowerBound,upperBound,subnetMask,availableHosts))
    
    
def calculate_block_size(cidr):
    y = 32 - cidr
    blockSize = pow(2,y)
    return(blockSize)
    
def subnet_mask(cidr):
    i = 0
    while cidr - 8 >=  0:
        cidr = cidr - 8
        i = i + 1
    subnetMask = []
    for j in range(i):
        subnetMask.append("255.")
    k = 8 - cidr
    subnetOctet = pow(2,k)
    subnetOctet = 256 - subnetOctet
    subnetMask.append(str(subnetOctet))
    i = i + 1
    while i <= 3:
        subnetMask.append(".0")
        i = i + 1
    subnetMask = ''.join(subnetMask)
    return(subnetMask)

def ip_space(blockSize,ipaddr):
    i = 3
    while blockSize // 256 >= 1:
        blockSize = blockSize // 256
        i = i - 1
    ipaddr = ipaddr.split(".", 3)
    octet = int(ipaddr[i])
    lowerOctet = octet
    while lowerOctet % blockSize != 0:
        lowerOctet = lowerOctet - 1
    upperOctet = lowerOctet + blockSize - 1
    j = i
    ipaddr[i] = lowerOctet
    while i < 3:
        i = i + 1
        ipaddr[i] = 0
    lowerBound = '.'.join(str(e) for e in ipaddr)
    ipaddr[j] = upperOctet
    while j < 3:
        j = j + 1
        ipaddr[j] = 255
    upperBound = '.'.join(str(e) for e in ipaddr)
    return(lowerBound,upperBound)
    
main()


