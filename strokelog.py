import pyrow
import time

if __name__ == '__main__':

    # Connecting to erg
    ergs = list(pyrow.find())
    if len(ergs) == 0:
        exit("No ergs found.")

    erg = pyrow.pyrow(ergs[0])
    print("Connected to erg.")

    # Open and prepare file
    write_file = open('workout.csv', 'w')
    write_file.write('Time, Distance, SPM, Pace, Force Plot\n')

    # Loop until workout has begun
    workout = erg.get_workout()
    print("Waiting for workout to start ...")
    while workout['state'] == 0:
        time.sleep(1)
        workout = erg.get_workout()
    print("Workout has begun")

    # Loop until workout ends
    while workout['state'] == 1:

        forceplot = erg.get_force_plot()
        # Loop while waiting for drive
        while forceplot['strokestate'] != 2 and workout['state'] == 1:
            # ToDo: sleep?
            forceplot = erg.get_force_plot()
            workout = erg.get_workout()

        # Record force data during the drive
        # start of pull (when strokestate first changed to 2)
        force = forceplot['forceplot']
        monitor = erg.get_monitor()  # get monitor data for start of stroke
        # Loop during drive
        while forceplot['strokestate'] == 2:
            # ToDo: sleep?
            forceplot = erg.get_force_plot()
            force.extend(forceplot['forceplot'])

        forceplot = erg.get_force_plot()
        force.extend(forceplot['forceplot'])

        # Write data to write_file
        workoutdata = str(monitor['time']) + "," + str(monitor['distance']) + "," + \
            str(monitor['spm']) + "," + str(monitor['pace']) + ","

        forcedata = ",".join([str(f) for f in force])
        write_file.write(workoutdata + forcedata + '\n')

        # Get workout conditions
        workout = erg.get_workout()

    write_file.close()
    print("Workout has ended")
