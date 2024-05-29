# Stage 1: Use a centos base image to install dependencies and build sflowtool
FROM centos:7 as builder

# Install necessary dependencies
RUN yum update -y && \
    yum install -y wget make gcc

# Download and install sflowtool
RUN wget http://www.inmon.com/bin/sflowtool-3.22.tar.gz && \
    tar -xzf sflowtool-3.22.tar.gz && \
    cd sflowtool-3.22 && \
    ./configure && \
    make && \
    make install

# Stage 2: Use the official Logstash image as the base image
FROM docker.elastic.co/logstash/logstash:8.11.0

# Copy the sflowtool binary from the builder stage
COPY --from=builder /usr/local/bin/sflowtool /usr/local/bin/sflowtool

# Copy sflowtool-wrapper.sh to image
COPY --chmod=755 script/sflowtool-wrapper.sh /usr/share/logstash/sflowtool-wrapper.sh




