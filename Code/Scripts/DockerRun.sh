#!/bin/bash
docker run --privileged --runtime=nvidia -it -v $PWD:/app/data  forcetest:latest sp MOLECULE.xyz