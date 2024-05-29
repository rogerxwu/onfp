from scapy.all import *


""" def create_netflow_v9_packet():
    # NetFlow v9 Header
    netflow_v9_header = (
        b"\x00\x09"  # Version 9
        b"\x00\x02"  # Count (2 FlowSets: one template and one data)
        b"\x00\x00\x00\x00"  # SysUptime (0 for simplicity)
        b"\x00\x00\x00\x00"  # UnixSecs (0 for simplicity)
        b"\x00\x00\x00\x00"  # FlowSequence (0 for simplicity)
        b"\x00\x00"  # Source ID (0 for simplicity)
    )

    # NetFlow v9 Template FlowSet Header
    template_flowset_header = (
        b"\x00\x00"  # FlowSet ID (0 for Template)
        b"\x00\x00"  # Length (36 bytes: 4 bytes for header + 32 bytes for template record)
    )

    # Template Record (Template ID 256)
    template_record = (
        b"\x01\x00"  # Template ID (256)
        b"\x00\x06"  # Field Count (6 fields for this example)
        # Field Specifiers
        b"\x00\x08"  # Field 1 Type (IPV4_SRC_ADDR)
        b"\x00\x04"  # Field 1 Length (4 bytes)
        b"\x00\x0c"  # Field 2 Type (IPV4_DST_ADDR)
        b"\x00\x04"  # Field 2 Length (4 bytes)
        b"\x00\x0a"  # Field 3 Type (L4_SRC_PORT)
        b"\x00\x02"  # Field 3 Length (2 bytes)
        b"\x00\x0e"  # Field 4 Type (L4_DST_PORT)
        b"\x00\x02"  # Field 4 Length (2 bytes)
        b"\x00\x04"  # Field 5 Type (PROTOCOL)
        b"\x00\x01"  # Field 5 Length (1 byte)
        b"\x00\x07"  # Field 6 Type (TCP_FLAGS)
        b"\x00\x01"  # Field 6 Length (1 byte)
    )

    # NetFlow v9 Data FlowSet Header
    data_flowset_header = (
        b"\x01\x00"  # FlowSet ID (256 for the template above)
        b"\x00\x18"  # Length (24 bytes: 4 bytes for header + 20 bytes for data record)
    )

    # Data Record (matching the template)
    data_record = (
        b"\xc0\xa8\x01\x01"  # Source IP Address (192.168.1.1)
        b"\xc0\xa8\x01\x02"  # Destination IP Address (192.168.1.2)
        b"\x00\x50"  # Source Port (80)
        b"\x01\xbb"  # Destination Port (443)
        b"\x06"  # Protocol (TCP)
        b"\x10"  # TCP Flags (ACK)
    )

    # Combine all parts into a single payload
    payload = (
        netflow_v9_header
        + template_flowset_header
        + template_record
        + data_flowset_header
        + data_record
    )

    return payload

 """


def create_netflow_v9_packet():
    header = Ether() / IP(dst="127.0.0.1") / UDP(dport=2055)
    netflow_header = NetflowHeader() / NetflowHeaderV9()

    # Let's first build the template. Those need an ID > 255.
    # The (full) list of possible fieldType is available in the
    # NetflowV910TemplateFieldTypes list. You can also use the int value.
    flowset = NetflowFlowsetV9(
        templates=[
            NetflowTemplateV9(
                template_fields=[
                    NetflowTemplateFieldV9(fieldType="IN_BYTES", fieldLength=1),
                    NetflowTemplateFieldV9(fieldType="IN_PKTS", fieldLength=4),
                    NetflowTemplateFieldV9(fieldType="PROTOCOL"),
                    NetflowTemplateFieldV9(fieldType="IPV4_SRC_ADDR"),
                    NetflowTemplateFieldV9(fieldType="IPV4_DST_ADDR"),
                ],
                templateID=256,
                fieldCount=5,
            )
        ],
        flowSetID=0,
    )
    # Let's generate the record class. This will be a Packet class
    # In case you provided several templates in ghe flowset, you will need
    # to pass the template ID as second parameter
    recordClass = GetNetflowRecordV9(flowset)
    # Now lets build the data records
    dataFS = NetflowDataflowsetV9(
        templateID=256,
        records=[  # Some random data.
            recordClass(
                IN_BYTES=b"\x12",
                IN_PKTS=b"\0\0\0\0",
                PROTOCOL=6,
                IPV4_SRC_ADDR="192.168.0.10",
                IPV4_DST_ADDR="192.168.0.11",
            ),
            recordClass(
                IN_BYTES=b"\x0c",
                IN_PKTS=b"\1\1\1\1",
                PROTOCOL=3,
                IPV4_SRC_ADDR="172.0.0.10",
                IPV4_DST_ADDR="172.0.0.11",
            ),
        ],
    )
    pkt = header / netflow_header / flowset / dataFS
    return pkt


def send_netflow_v9_packet(payload):
    # packet = IP(dst="127.0.0.1") / UDP(dport=2055) / Raw(load=payload)
    send(payload)


# Create NetFlow v9 packet payload
payload = create_netflow_v9_packet()

# Send the NetFlow v9 packet
send_netflow_v9_packet(payload)
