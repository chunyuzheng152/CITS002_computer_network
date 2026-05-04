# config.py
# This file stores the fixed values given in the project PDF.

#IP、MAC、network、protocol number、DATA/ACK、最大 segment size 是 PDF 明确规定的。
#routing table、MAC table、TTL 默认值的具体 Python 写法，是我根据 PDF 要求自己设计的。

# IP addresses
HOST_A_IP = "10.0.1.10"
HOST_B_IP = "10.0.2.20"

ROUTER_R1_IF1_IP = "10.0.1.1"
ROUTER_R1_IF2_IP = "10.0.2.1"

# MAC addresses
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"

ROUTER_R1_IF1_MAC = "BB:BB:BB:BB:BB:BB"
ROUTER_R1_IF2_MAC = "CC:CC:CC:CC:CC:CC"

# Network addresses
NETWORK_1 = "10.0.1.0/24"
NETWORK_2 = "10.0.2.0/24"

# Protocol constants
ETH_TYPE_IPV4 = "0x0800"
IP_PROTOCOL_UDP = 17

# TTL
DEFAULT_TTL = 4

# Transport constants
SRC_PORT = 5000
DST_PORT = 80

DATA = 0
ACK = 1

# Maximum data size for one UDP-like segment
MAX_SEGMENT_DATA_SIZE = 500

# MAC lookup tables
HOST_A_MAC_TABLE = {
    ROUTER_R1_IF1_IP: ROUTER_R1_IF1_MAC
}

HOST_B_MAC_TABLE = {
    ROUTER_R1_IF2_IP: ROUTER_R1_IF2_MAC
}

ROUTER_R1_MAC_TABLE = {
    HOST_A_IP: HOST_A_MAC,
    HOST_B_IP: HOST_B_MAC
}

# Routing tables
HOST_A_ROUTING_TABLE = {
    NETWORK_2: {
        "next_hop": ROUTER_R1_IF1_IP,
        "interface": "host_a_if"
    }
}

HOST_B_ROUTING_TABLE = {
    NETWORK_1: {
        "next_hop": ROUTER_R1_IF2_IP,
        "interface": "host_b_if"
    }
}

ROUTER_R1_ROUTING_TABLE = {
    NETWORK_1: {
        "next_hop": "direct",
        "interface": "if1"
    },
    NETWORK_2: {
        "next_hop": "direct",
        "interface": "if2"
    }
}