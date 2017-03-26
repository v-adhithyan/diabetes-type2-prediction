import argparse
import csv
import matplotlib.pyplot as plt
import math
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

#simulated_values = real_values + simulated_values

acceptance_rate = 0
error = 0.08

def show_histogram(input):
    x = []
    y = []
    for k, v in input.items():
        x.append(k)
    x.sort()

    for val in x:
        y.append(input[val])

    print "x {}".format(x)
    print "y {}".format(y)

    hist, bins = numpy.histogram(y, bins = x)
    width = numpy.diff(bins)
    center = (bins[:-1] + bins[1:]) / 2

    #fig, ax = plt.subplots(figsize=(8,3))
    #x.bar(center, hist, align='center', width=width)
    #x.set_xticks(bins)
    #fig.savefig("/tmp/out.png")
    #plt.hist(y, bins = [40] + x)

    plt.show()

def is_depression(val):
    return val > 0 and val <= 0.33

def is_necrosis(val):
    return val > 0.33 and val <= 0.66

def is_nephropathy(val):
    return val > 0.66 and val <= 1.00

def d_z(val):
    x11 = 10.0 ** 2
    x12 = 10.0 ** 2
    x13 = 70.0
    x14 = 2.0
    dis = (val - x13) / x14
    dis = dis ** 2

    return x11 / (x12 + dis)

def w_z(val):
    x21 = 100.0
    x22 = 55.0
    x23 = 40.0
    dis = ((val - x22) / x23) ** 2
    dis = math.exp(-dis)

    return x21 * dis

def g_z(val):
    x31 = 150.0
    x32 = 0.3
    x33 = 440.0
    dis = random.random() * (val - 30) / 0.05

    return (x31 + (dis * x32)) / x33

def c_z(val):
    x51 = 2.1
    x52 = 0.5
    x53 = 0.00066
    x54 = 3.0
    z = x52 + (x53 * ((val - 30) / 0.05))
    c = 1 + ((2 * random.random()) ** x54)

    return (z * c) / x51

def p_z(val):
    x41 = 1.9
    x42 = 0.09
    x43 = 0.04
    x44 = 0.05

    num = 110.0 + (x42 * (val - 30) / 0.05)
    den = 70.0 + (x43 * (val - 30) / 0.05)

    return (x41 * num / den) + (x44 * (2 * random.random()) - 1)

def ps_z(val):
    return 1 - (d_z(val) * w_z(val) * g_z(val) * p_z(val) * c_z(val))

def necrosis_wrto_glucose_and_depression():
    count = 0
    #print "The length of sim values is {}".format(len(simulated_values))
    age_count = {}
    age_count[50] = 0
    age_count[60] = 0
    age_count[70] = 0
    age_count[80] = 0

    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0

    for m in range(simulation_length):
        nj = random.randint(0, simulation_length - 1)
        #print nj
        patient = simulated_values[nj]
        age = int(patient["age"])
        #weight = int(patient["weight"])
        glucose = int(patient["glucose"])

        if age >= 30 and age <=80:
            zk = age
            if d_z(age) > 0.5:
                if g_z(age) > 0.5:
                    if c_z(age) > 0.66:
                        p1 = p1 + 1
                        if age >= 50 and age < 60:
                            #print "50"
                            age_count[50] = age_count[50] + 1
                        if age >= 60 and age < 70:
                            #print "60"
                            age_count[60] = age_count[60] + 1
                        if age >= 70 and age < 80:
                            #print "70"
                            age_count[70] = age_count[70] + 1
                        if age >= 80:
                            #print "80"
                            age_count[80] = age_count[80] + 1
            if d_z(age) > 0.3:
                if w_z(age) > 0.2:
                    if g_z(age) > 0.4:
                        if c_z(age) > 0.66:
                            p2 = p2 + 1
            if w_z(age) > 0.9:
                if p_z(age) > 0.9:
                    if c_z(age) > 0.66:
                        p3 = p3 + 1
            if ps_z(age) < 0.65:
                #print "ps < 0.65"
                a = 0
            if w_z(age) > 0.8:
                if g_z(age) > 0.5:
                    if c_z(age) > 0.33 and c_z(age) < 0.66:
                        p4 = p4 + 1
            if g_z(age) > 0.5:
                if p_z(age) > 0.9:
                    if c_z(age) > 0.33 and c_z(age) < 0.66:
                        p5 = p5 + 1
            if ps_z(age) < 0.65:
                #print
                a = 5

    #print age_count
    #show_histogram(age_count)
    print "Necrosis due to glucose and depression {}".format(p1)
    print "Necrosis due to glucose overweight depression {}".format(p2)
    print "Necrosis due to overweight sbp {}".format(p3)
    print "Necrosis due to overweight and glucose {}".format(p4)
    print "Necrosis due to glucose and sbp {}".format(p5)

    #print "The number of critic patients is {}".format(count)

def identify_critical_patients():
    necrosis_wrto_glucose_and_depression()



parser = argparse.ArgumentParser()
parser.add_argument("--simulate", help = "Run a new monte carlo simulation and use new values for prediction", action = "store_true")
args = parser.parse_args()

#t1 = time.clock()

if args.simulate:
    print "New simulation ..."
    for beta in range(25):
        for i in range(simulation_length):
            for alpha in range(7):
                aleatory_number = random.random()
                gaussian_profile = numpy.random.normal()
                if gaussian_profile > aleatory_number:
                    acceptance_rate = acceptance_rate + 1
                    acceptance = gaussian_profile + error
                    simulated_values[i][variables[alpha]] = real_values[beta][variables[alpha]]

#t2 = time.clock()

    with open("output.csv", "wb") as f:
        writer = csv.DictWriter(f, fieldnames = variables)
        writer.writeheader()
        writer.writerows(simulated_values)

    identify_critical_patients()

else:
    print "Read simulated values ...."
    with open("output.csv", "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            print row
