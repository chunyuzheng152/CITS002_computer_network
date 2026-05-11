import sys
from config import *
from devices import Host, Router

def main():
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <message_size>")
        sys.exit(1)
        
    try:
        data_size = int(sys.argv[1])
    except ValueError:
        print("Error: message_size must be an integer.")
        sys.exit(1)
    
    data = "A" * data_size
    
    host_a = Host(name="Host A", ip=HOST_A_IP, mac=HOST_A_MAC)
    host_b = Host(name="Host B", ip=HOST_B_IP, mac=HOST_B_MAC)
    router_r1 = Router(name="Router R1")

    
    network = {
        "host_a": host_a,
        "host_b": host_b,
        "router": router_r1
    }

    host_a.send_data(HOST_B_IP, data, network)

if __name__ == "__main__":
    main()