import argparse
import csv
import math
import os

lines = [] # input
angles = [] # output

def export_path_csv(l):
    EXPORT_DIR = "Temp"
    EXPORT_FILE_NAME = "angles.csv"
    FULL_EXPORT_FILE_PATH = os.path.join(EXPORT_DIR, EXPORT_FILE_NAME)
    # create temp folder
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    with open(FULL_EXPORT_FILE_PATH, "w") as file:
        for i in range(len(l)):
            line = str(l[i][0]) + "," + str(l[i][1]) + "," + str(l[i][2]) + "," + str(l[i][3]) + "\n"
            file.write(line)

def main():
    # parse the command-line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help="Enable debug outputs.")
    parser.add_argument("-la", dest="la", required=True, action="store",
                        type=float, help="Length of arm A (servo 1 to servo 2)")
    parser.add_argument("-lb", dest="lb", required=True, action="store",
                        type=float, help="Length of arm B (servo 2 to servo pen)")
    parser.add_argument("-s", "--src_csv_path", required=True, dest="src_csv_path",
                        action="store", type=str, help="Path to the source csv file")
    parser.set_defaults(debug=False)
    cmd_args = parser.parse_args()

    # set arm lengths
    la = cmd_args.la
    lb = cmd_args.lb

    # put vectors from CSV into an array
    with open(cmd_args.src_csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            i = 0
            while i < len(row): # convert vectors from str to int
                row[i] = int(row[i])
                i += 1
            lines.append(row)

    # calculate angles
    for line in lines:
        # origin angles
        ac = math.sqrt(line[0] ** 2 + line[1] ** 2) # assuming servo 1 is at 0,0
        bac = math.acos((math.sqrt(la) + math.sqrt(ac) - math.sqrt(lb)) / (2.0 * la * ac))
        yac = math.asin(line[0] / ac)  # assuming servo 1 is at 0,0
        yab = (math.pi - yac - bac) if line[1] > 0 else (yac - bac) # assuming servo 1 is at 0,0
        angle_a1 = yab
        angle_b1 = math.acos((math.sqrt(la) + math.sqrt(lb) - math.sqrt(ac)) / (2.0 *la *lb))

        # destination angles
        ac = math.sqrt(line[2] ** 2 + line[3] ** 2) # assuming servo 1 is at 0,0
        bac = math.acos((math.sqrt(la) + math.sqrt(ac) - math.sqrt(lb)) / (2.0 * la * ac))
        yac = math.asin(line[2] / ac)  # assuming servo 1 is at 0,0
        yab = (math.pi - yac - bac) if line[3] > 0 else (yac - bac) # assuming servo 1 is at 0,0
        angle_a2 = yab
        angle_b2 = math.acos((math.sqrt(la) + math.sqrt(lb) - math.sqrt(ac)) / (2.0 * la * lb))

        angle = []
        angle.append(angle_a1)
        angle.append(angle_b1)
        angle.append(angle_a2)
        angle.append(angle_b2)

        angles.append(angle)

    if cmd_args.debug:
        export_path_csv(angles)

# main program entry point
if __name__ == "__main__":
    main()