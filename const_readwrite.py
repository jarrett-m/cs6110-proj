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

s.add(k >= 1)
s.add(l >= tBURST + tRTRS) # so the paper says that l >= tBURST + tRTRS,
#but if we are solving for constant Activate it shoudl be RCD as it follows an activate
s.add(k == k_prime + 1) #if k = k' + 1
# #solve for rank partitioning
s.add(((k*l) - tCAS - tBURST) != ((k_prime * l) - tCWD - tBURST))
s.add(((k*l) - tCAS - tBURST) != ((k_prime * l) - tBURST))
s.add(((k*l) - tBURST )!= ((k_prime * l )- tCAS - tBURST))
s.add(((k*l) - tBURST) != ((k_prime * l) - tCWD - tBURST))
s.add(((k*l) - tBURST) != ((k_prime * l) - tBURST))

#tRRD constraint
s.add(k == k_prime + 1) #if k = k' + 1
s.add(((k*l) - tCAS - tBURST) - ((k_prime * l) - tCWD - tBURST) >= tRRD)
s.add(((k*l) - tCWD - tBURST) - ((k_prime * l) - tCAS - tBURST) >= tRRD)
s.add(((k*l) - tCAS - tBURST) - ((k_prime * l) - tCAS - tBURST) >= tRRD)
s.add(((k*l) - tCWD - tBURST) - ((k_prime * l) - tCWD - tBURST) >= tRRD)

#tWTR worse case read to write dalay
s.add(k == k_prime + 1) #if k = k' + 1
s.add(((k*l) - tBURST) - ((k_prime * l) - tBURST) >= tCWD + tBURST)
s.add(((k*l) - tBURST) - ((k_prime * l) - tBURST) >= tCWD + tBURST + tWTR)

s.minimize(l)


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


s2.add(k > 4)
s2.add(l >= tRCD)
#tFAW
s2.add(k == k_prime + 4)
s2.add(((k*l) - tCAS - tBURST) - ((k_prime * l) - tCWD - tBURST) >= tFAW)
s2.add(((k*l) - tCWD - tBURST) - ((k_prime * l) - tCAS - tBURST) >= tFAW)
s2.add(((k*l) - tCAS - tBURST) - ((k_prime * l) - tCAS - tBURST) >= tFAW)
s2.add(((k*l) - tCWD - tBURST) - ((k_prime * l) - tCWD - tBURST) >= tFAW)

s2.minimize(l)

if s2.check() == sat:
    model = s2.model()
    print("FAW Contraint")
    print(f"Minimum value of l is {model.evaluate(l)}")
    print(f"Value of k is {model.evaluate(k)}")
    print(f"Value of k_prime is {model.evaluate(k_prime)}")
else:
    print("No solution")
    print(s2.check())