from z3 import *

#defining the variables
k = Int('k')
k_prime = Int('k_prime')
l = Int('l')
tCAS = Int('tCAS')
tRCD = Int('tRCD')
tCWD = Int('tCWD')
tBURST = Int('tBURST')
tRTRS = Int('tRTRS')
tRRD = Int('tRRD')
tFAW = Int('tFAW')
tWTR = Int('tWTR')
s = Optimize()

#set dram timings
s.add(tCAS == 11)
s.add(tRCD == 11)
s.add(tCWD == 5)
s.add(tBURST == 4)
s.add(tRTRS == 2)
s.add(tRRD == 5)
s.add(tFAW == 24)
s.add(tWTR == 6)

s.add(k > 0)
s.add(k_prime > 0)
s.add(l >= tBURST + tRTRS) # so the paper says that l >= tBURST + tRTRS, but also says
# The smallest value of l (l ≥ 6) that fulfils these equations is 7.
# if i do > i get 7, if i do >= i get 6, so i'm going to go with 7

# #solve for rank partitioning
# s.add(((k*l) - tCAS - tRCD) != ((k_prime * l) - tRCD - tCWD))
s.add(((k*l) - tCAS - tRCD) != ((k_prime * l) - tCAS))
# s.add(((k*l) - tCAS - tRCD) != ((k_prime * l) - tCWD))
# s.add(((k*l) - tCWD - tRCD )!= ((k_prime * l )- tCAS))
# s.add(((k*l) - tCWD - tRCD) != ((k_prime * l) - tCWD))
# s.add(((k*l) - tCAS) != ((k_prime * l) - tCWD))


#tRRD constraint
s.add(k == k_prime + 1)
# NO tRRD DELAY FOR A R TO W OR W TO R COS WE ARE ONLY DOING R TO R
# s.add(((k*l) - tCAS - tRCD) - ((k_prime * l) - tCWD - tRCD) >= tRRD)
# s.add(((k*l) - tCWD - tRCD) - ((k_prime * l) - tCAS - tRCD) >= tRRD)
s.add(((k*l) - tCAS - tRCD) - ((k_prime * l) - tCAS - tRCD) >= tRRD)
# R TO R ONLY
# s.add(((k*l) - tCWD - tRCD) - ((k_prime * l) - tCWD - tRCD) >= tRRD)

# NO READ TO WRITE DELAY COS WE ARE ONLY READING BACK TO BACK
# #tWTR worse case read to write dalay
# s.add(((k*l) - tCWD) - ((k_prime * l) - tCAS) >= tCWD + tBURST)
# s.add(((k*l) - tCAS) - ((k_prime * l) - tCWD) >= tCWD + tBURST + tWTR)

s.minimize(l)
first_l = l

if s.check() == sat:
    model = s.model()
    print("Everything Else Contraint")
    print(f"Minimum value of l is {model.evaluate(l)}")
    print(f"Value of k is {model.evaluate(k)}")
    print(f"Value of k_prime is {model.evaluate(k_prime)}")

else:
    print("No solution")
    print(s.check())

print("")

#now solve for tFAW
s2 = Optimize()
s2.add(tCAS == 11)
s2.add(tRCD == 11)
s2.add(tCWD == 5)
s2.add(tBURST == 4)
s2.add(tRTRS == 2)
s2.add(tRRD == 5)
s2.add(tFAW == 24)
s2.add(tWTR == 6)

s2.add(k > 0)
s2.add(k_prime > 0)
s2.add(l > tBURST + tRTRS) # so the paper says that l >= tBURST + tRTRS, but also says
# The smallest value of l (l ≥ 6) that fulfils these equations is 7.

#tFAW
s2.add(k == k_prime + 4)
# s2.add(((k*l) - tCAS - tRCD) - ((k_prime * l) - tCWD - tRCD) >= tFAW)
# s2.add(((k*l) - tCWD - tRCD) - ((k_prime * l) - tCAS - tRCD) >= tFAW)
s2.add(((k*l) - tCAS - tRCD) - ((k_prime * l) - tCAS - tRCD) >= tFAW)
# s2.add(((k*l) - tCWD - tRCD) - ((k_prime * l) - tCWD - tRCD) >= tFAW)

s2.minimize(l)


if s2.check() == sat:
    model = s2.model()
    print("FAW Contraint")
    print(f"Minimum value of l is {model.evaluate(l)} or {model.evaluate(first_l)}")
    print(f"Value of k is {model.evaluate(k)}")
    print(f"Value of k_prime is {model.evaluate(k_prime)}")
else:
    print("No solution")
    print(s2.check())