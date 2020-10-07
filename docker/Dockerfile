FROM ubuntu:18.04
WORKDIR /home/sqed-demo

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y clang cmake libpcre* wget unzip build-essential automake libgmp-dev curl nano libboost-dev default-jdk libclang-dev llvm llvm-dev lbzip2 libncurses5-dev git libtool iverilog bison flex libreadline-dev gawk tcl-dev libffi-dev graphviz xdot pkg-config gtkwave

RUN git clone -b pono https://github.com/upscale-project/generic-sqed-demo.git

RUN cd generic-sqed-demo && ./setup-yosys.sh && ./setup-pono.sh

