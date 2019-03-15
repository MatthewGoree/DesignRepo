import math
import matplotlib.pyplot as plt
import random as rand
import numpy as np

def distance(theta, radius):
    deg = theta * 180 / math.pi
    if (deg <= 90):
        return theta * radius
    if (deg > 270):
        return (theta - 2 * math.pi) * radius
    if (deg > 90) and (deg <= 180):
        return (math.pi - theta) * radius
    if (deg > 180) and (deg <= 270):
        return (math.pi - theta) * radius
    else:
        print(deg)

# added test as an argument so this can be used with multiple sims
def rtest(sim_test):
    #Does a run with random initial theta
    theta_0 = rand.random() * 2 * math.pi
    a = sim_test(theta_0)

    print('Final angle: ', a["theta"][-1])

    plt.subplot(2,2,1)
    plt.plot(a["time"], a["theta"])
    plt.xlabel("time (s)")
    plt.ylabel("Theta (rad)")

    plt.subplot(2,2,2)
    plt.plot(a["time"], a["avel"])
    plt.xlabel("time (s)")
    plt.ylabel("avel")

    plt.subplot(2,2,3)
    plt.plot(a["time"], a["dv"])
    plt.xlabel("time")
    plt.ylabel("dv")

    plt.subplot(2,2,4)
    plt.plot(a["time"], a["distance"])
    plt.xlabel("time")
    plt.ylabel("distance")
    plt.show()


def mtest(n):
    #Perform n sims with random starting angles
    #prints the percentage of successful runs
    #returns a list of distances

    results = [test(rand.random() * 2 * math.pi)["distance"][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .3]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results


def otest(n):
    #performs n sims with angles incremented from 0 to 2pi
    #prints percentage of successful runs
    #returns a list of distances

    results = [test(i * 2 * math.pi / n)['distance'][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .2]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results


def test(theta):
    #performs a sim with given starting angle
    motor_mass = .845 #kg
    propeller_mass = .300 #kg
    added_mass = .2 #weight of whatever we add to motor (kg)

    m = motor_mass + propeller_mass + added_mass
    prop_length = .7 #meter
    prop_rad = prop_length / 2
    motor_rad = .089 / 2 #meters


    prop_I = 0.004064 * 2
    motor_I = (motor_mass * motor_rad ** 2) / 2 #I = m * r ^2 for thin shelled cylinder, assume only half of motor mass is spinning
    #I = m * 4 * r / 12

    I = prop_I + motor_I

    f_const = 8.89644 #2lbs of force

    max_iter = 50000
    dt = .00005
    avel = 15000 * math.pi/30 # 15000 rpm to rad/sec
    magnet_range = math.pi/6

    all_theta = [theta]
    all_avel = [avel]
    all_dv = [0]
    
    # aero drag values
    air_density = 1.225
    v = 26.8
    A = 6.4 * 100**-2
    Cd_front = .01
    Cd_back = .34

    # old values still needed for older functions - want to remove in the future
    r=1
    l=.2

    for i in range(1,max_iter):
        #Friction
        avel = avel * .997

        #Magnet Force
        if (theta < magnet_range) or ((theta < math.pi + magnet_range) and (theta > math.pi)):
            f = -1 * math.fabs(math.sin(theta)) * f_const
            all_dv.append(-1)

        elif (theta > math.pi - magnet_range) or ((theta < math.pi) and theta > math.pi - magnet_range):
            f = 1 * math.fabs(math.sin(theta)) * f_const
            all_dv.append(1)

        else:
            f = 0
            all_dv.append(0)

        #Aero Torque = force_back * half length of prop - force_front * half length of prop
        # Cd is adjusted for angle with the cos 
        aero_torque = (air_density * v**2 * A / 2) * (Cd_back - Cd_front) * math.fabs(math.cos(theta)) * prop_length /4

        torque = f * l + aero_torque
        dv = torque * dt / I
        avel = avel + dv
        theta = theta + avel * dt

        #reset theta to within 2pi range
        if (theta >= 2 * math.pi):
            theta = theta - (2 * math.pi)
        if (theta < 0):
            theta += 2 * math.pi

        all_theta.append(theta)
        all_avel.append(avel)

    all_t = [i * dt for i in range(max_iter)]
    all_distance = [distance(i,r) for i in all_theta]
    return {"time" : all_t, "theta" : all_theta, "avel" : all_avel,
            "distance" : all_distance, "dv" : all_dv}

def save_data(test, fname):
    np.savetxt(fname, np.c_[test["time"], test["theta"], test["distance"]], delimiter = ',')

if __name__ == '__main__':
    print('here')
    rtest(test)
