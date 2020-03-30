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
    i = 0   # a dummy variable we use to iterate
    while cidr - 8 >=  0:   # determines which of the 4 octets we need to do math to calculate
        cidr = cidr - 8
        i = i + 1
    subnetMask = []
    for j in range(i):  # uses the dumby variable j to determine which octets we can simply consider as 255
        subnetMask.append("255.")
    k = 8 - cidr    # using k as the 'inverse' of our cidr block makes the math simpler
    subnetOctet = pow(2,k)
    subnetOctet = 256 - subnetOctet # we use 256 instead of 255 because we're doing decimal math right now, not binary
    subnetMask.append(str(subnetOctet))
    i = i + 1   # makes sure we skip the octet we just calculated. We don't want to modify that octet
    while i <= 3:   # tosses 0 on the end of our subnet mask
        subnetMask.append(".0")
        i = i + 1
    subnetMask = ''.join(subnetMask)
    return(subnetMask)

def ip_space(blockSize,ipaddr):
    i = 3   # defining a dummy variable to iterate through
    while blockSize // 256 >= 1:    # gives us the block size of the octet we're working with
        blockSize = blockSize // 256
        i = i - 1
    ipaddr = ipaddr.split(".", 3)
    octet = int(ipaddr[i])  # determines which octet we'll be doing math with
    lowerOctet = octet
    while lowerOctet % blockSize != 0:  # subtracts 1 from our octet value until it's divible by our octet's block size
        lowerOctet = lowerOctet - 1
    upperOctet = lowerOctet + blockSize - 1 # subtracts 1 because we're switching between decimal and 'binary' math at this step
    j = i # another dummy iterator based on i, but for our upper bound this time
    ipaddr[i] = lowerOctet
    while i < 3: # this math is simply for when we have subnets larger than /24 and the trailing octets must be 0 or 255
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


