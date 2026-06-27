#!/bin/bash
docker run --privileged --runtime=nvidia -it -v $PWD:/app/data  amory-quantum:latest sp H2O.xyz