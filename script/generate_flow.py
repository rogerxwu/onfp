from scapy.all import *


def build_netflow_v5_packet():
    netflow = (
        NetflowHeader() / NetflowHeaderV5(count=5) / NetflowRecordV5(dst="192.168.0.1")
    )
    pkt = Ether() / IP() / UDP() / netflow

    wrpcap("netflow_traffic.pcap", pkt)


def build_netflow_v9_packet():
    header = Ether() / IP() / UDP()
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

    # Write the packets to a pcap file
    wrpcap("netflow_traffic.pcap", pkt)


if __name__ == "__main__":
    # build_netflow_v9_packet()
    build_netflow_v5_packet()
