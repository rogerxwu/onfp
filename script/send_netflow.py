from scapy.all import *

# Craft the NetFlow header and data
# This is an example of NetFlow v5 header
netflow_header = (
    b"\x00\x05"  # Version 5
    b"\x00\x01"  # Count (1 flow)
    b"\x00\x00\x00\x00"  # SysUptime (0 for simplicity)
    b"\x00\x00\x00\x00"  # UnixSecs (0 for simplicity)
    b"\x00\x00\x00\x00"  # UnixNsecs (0 for simplicity)
    b"\x00\x00\x00\x00"  # FlowSequence (0 for simplicity)
    b"\x00\x00"  # EngineType, EngineID (0 for simplicity)
    b"\x00\x00"  # SamplingInterval (0 for simplicity)
)

# Example of a NetFlow v5 flow record
flow_record = (
    b"\xc0\xa8\x01\x01"  # Source IP Address (192.168.1.1)
    b"\xc0\xa8\x01\x02"  # Destination IP Address (192.168.1.2)
    b"\x00\x00\x00\x00"  # Next Hop IP Address (0.0.0.0)
    b"\x00\x00"  # Input Interface (0 for simplicity)
    b"\x00\x00"  # Output Interface (0 for simplicity)
    b"\x00\x00\x00\x00"  # Packets (0 for simplicity)
    b"\x00\x00\x00\x00"  # Octets (0 for simplicity)
    b"\x00\x00\x00\x00"  # Start SysUptime (0 for simplicity)
    b"\x00\x00\x00\x00"  # End SysUptime (0 for simplicity)
    b"\x00\x00"  # Source Port (0 for simplicity)
    b"\x00\x00"  # Destination Port (0 for simplicity)
    b"\x00\x00"  # Padding1 (0 for simplicity)
    b"\x00"  # TCP Flags (0 for simplicity)
    b"\x00"  # Protocol (0 for simplicity)
    b"\x00"  # TOS (0 for simplicity)
    b"\x00"  # Padding2 (0 for simplicity)
    b"\x00\x00"  # Source AS (0 for simplicity)
    b"\x00\x00"  # Destination AS (0 for simplicity)
    b"\x00\x00"  # Source Mask (0 for simplicity)
    b"\x00\x00"  # Destination Mask (0 for simplicity)
    b"\x00\x00\x00\x00"  # Padding3 (0 for simplicity)
)

# Combine the header and flow record into a single payload
payload = netflow_header + flow_record

# Create the UDP packet
packet = IP(dst="127.0.0.1") / UDP(dport=2055) / Raw(load=payload)

# Send the packet
for i in range(100):
    send(packet)
