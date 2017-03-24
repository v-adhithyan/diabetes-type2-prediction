import csv
import numpy
import random
import time

variables = ["age", "weight", "sbp", "glucose", "cardio_events", "nephro_level", "necrosis_level"]
variables_init = ["0", "0", "0", "0", "0", "low", "null"]
simulated_values = []
simulation_length = 975

for i in range(simulation_length):
    dummy = {}
    for j in range(len(variables)):
        dummy[variables[j]] = variables_init[j]
    simulated_values.append(dummy)
#print simulated_values

real_values = []
with open("input.csv", "rb") as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        real_values.append(row)

acceptance_rate = 0
error = 0.08

t1 = time.clock()

for beta in range(25):
    for i in range(simulation_length):
        for alpha in range(7):
            aleatory_number = random.random()
            gaussian_profile = numpy.random.normal()
            if gaussian_profile > aleatory_number:
                acceptance_rate = acceptance_rate + 1
                acceptance = gaussian_profile + error
                simulated_values[i][variables[alpha]] = real_values[beta][variables[alpha]]

t2 = time.clock()

with open("output.csv", "wb") as f:
    writer = csv.DictWriter(f, fieldnames = variables)
    writer.writeheader()
    writer.writerows(simulated_values)

print "The total time is {} seconds".format(t2-t1)
print "The acceptance rate is {}".format(acceptance_rate)
