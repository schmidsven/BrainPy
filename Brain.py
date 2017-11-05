import math
import subprocess
import psutil
from collections import deque
from nltk.corpus import wordnet

def energy():
    p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    o_max  = [l for l in output.splitlines() if "MaxCapacity" in l][0]
    o_cur  = [l for l in output.splitlines() if "CurrentCapacity" in l][0]
    b_max  = float(o_max.rpartition("=")[-1].strip())
    b_cur  = float(o_cur.rpartition("=")[-1].strip())
    charge = b_cur / b_max
    answer = int(math.ceil(10 * charge))
    return charge

