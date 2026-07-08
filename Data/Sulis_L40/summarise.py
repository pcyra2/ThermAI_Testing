import json
import os
import glob
import numpy

def main():
    out_files = glob.glob("pes.*.json") 
    data = numpy.zeros([4,len(out_files)])
    
    for i, file in enumerate(out_files):
        assert os.path.isfile(file)
        with open(file, "r") as f:
            dat = json.load(f)
        if i == 0:
            keys = dat.keys()
        for j, key in enumerate(keys):
            if "time"in key:
                data[j,i] = float(dat[key])
#        data[i] = float(dat["total_time"])

    print(data)
    for i, key in enumerate(keys):
        if "time" in key:
            print(f"{key} Average = {numpy.average(data[i,:])} seconds")

if __name__ == "__main__":
    main()
