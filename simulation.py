import csv
import numpy
import random
import time

real_values = []
simulated_values = []
with open("input.csv", "rb") as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        real_values.append(row)

acceptance_rate = 0
error = 0.08

t1 = time.clock()

for beta in range(25):
    for i in range(39):
        for alpha in range(7):
            aleatory_number = random.random()
            gaussian_profile = numpy.random.normal()
            if gaussian_profile > aleatory_number:
                acceptance_rate = acceptance_rate + 1
                print "S({},{},{}) = {}".format(beta, i, alpha, gaussian_profile + error)

t2 = time.clock()
print "The total time is {}".format(t2-t1)

print acceptance_rate
