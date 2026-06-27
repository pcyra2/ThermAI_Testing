FROM nvidia/cuda:12.2.2-devel-ubuntu22.04


RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    git \
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-setuptools \
    libprotobuf-dev \
    protobuf-compiler && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*


ENV CUDA_HOME="/usr/local/cuda" 
ENV LD_LIBRARY_PATH="${CUDA_HOME}/lib64::${LD_LIBRARY_PATH}"
ENV DOCKER="DOCKERENV"
ENV OMP_NUM_THREADS=6
ENV CUDA_VISIBLE_DEVICES=0
ENV PYTHONUNBUFFERED=1
RUN echo "export PATH=${CUDA_HOME}/bin:\$PATH" >> /etc/bash.bashrc
RUN echo "export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:\$LD_LIBRARY_PATH" >> /etc/bash.bashrc


RUN pip3 install cutensor-cu12
RUN pip3 install gpu4pyscf-cuda12x==1.4.0
RUN pip3 install GPUtil
RUN pip3 install libmsym
RUN pip3 install nvidia-pyindex
RUN pip3 install nvidia-cublas-cu12
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install setuptools --upgrade
RUN apt-get install -y ca-certificates gpg
RUN pip install cmake
RUN pip install basis-set-exchange
WORKDIR /app
ADD AmoryQuantum ./AmoryQuantum 
ADD setup.py .
RUN pip install -e . 

RUN pip install --prefer-binary pyscf
RUN pip install pyscf-dispersion 
RUN pip install pyscf==2.9


# CMD ["lspci"]
WORKDIR /app/data
CMD ["/bin/bash"]
