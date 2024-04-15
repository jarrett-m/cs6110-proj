
from z3 import *



for i in range(0, 51):

    dt = Real('dt')
    writes = Real('writes')
    reads = Real('reads')
    worse_channel_ratio = Real('worse_channel_ratio')
    mirror = Real('mirror')
    s = Optimize()


    s.add(writes == i)
    # s.add(writes >= 0)
    s.add(reads == 100 - writes)

    s.add(worse_channel_ratio < 1)
    s.add(worse_channel_ratio >= .5) 

    s.add(dt == 15)

    s.add(mirror == ((dt * writes) + (dt * reads / 2)))

    s.add(mirror <= (dt * ((writes + reads) * worse_channel_ratio)))



    if s.check() == sat:
        model = s.model()
        print(f"Write Ratio: {round((int(model.evaluate(writes).as_decimal(1))/100)*100)}%")
        print(f"Minimum Channel Imbalance: {round(float(model.evaluate(worse_channel_ratio).as_decimal(3)) * 100, 3)}%")
        print("")
    else:
        print("unsat")

