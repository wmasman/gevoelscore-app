import os,math,csv
from datetime import date,datetime
from pathlib import Path
import numpy as np
exec(open("stress_felt_curve.py").read().split("def main")[0])
master=load_master(); cutoff=find_device_baseline_cutoff(master)
s,g,c=build_pool(master,cutoff,False)
for thr in (45,50,55):
    print(f"stress> {thr}: n={int((s>thr).sum())}  (crash among them: {int(c[s>thr].sum())})")
print("top band (42-69) count:", int((s>=42).sum()))
