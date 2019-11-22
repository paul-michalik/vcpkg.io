FROM ubuntu:18.04

WORKDIR /wrk

RUN apt-get update && apt-get install -y \
    build-essential \
    git git-lfs \
    gdb \
    curl wget unzip \
&& rm -rf /var/lib/apt/lists/*

# Custom programs. We install everything into a "/usr/local/bin" based tree
# CMake 3.14
RUN wget -O /tmp/cmake-installer.sh https://cmake.org/files/v3.14/cmake-3.14.4-Linux-x86_64.sh && \ 
 sh /tmp/cmake-installer.sh --skip-license --prefix=/usr/local/bin && \
 rm -rf /tmp/cmake-installer.sh