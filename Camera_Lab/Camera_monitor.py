#coding:utf-8
#python:3
import sys
import os
from time import sleep
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

def get_tasklist():
    tasklist_v_fo_csv = os.popen('tasklist /v /fo csv').read()
    tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
    temp_list = []
    for tasklist in tasklist_v_fo_csv_list:
        tasklist = tasklist.replace("[", "").replace("]", "").replace("\"", "")
        temp = tasklist.split(",")
        if temp != "" and temp[0] in ["chrome.exe", "python.exe"]:
            temp_list.append(temp)

    for temp in temp_list:
        if "Camera" in temp:
            return False

    for temp in temp_list:
        if ("Google Chrome" in temp[-1]):
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            print('---Google Chrome exist---')
            os.system(cmd)
    return True

def Main():
    while 1:
        if get_tasklist():
            os.chdir(BASE_PATH)
            if os.path.exists(r"{}\xls_name.txt".format(BASE_PATH)):
                with open(r"{}\xls_name.txt".format(BASE_PATH), "r") as f:
                    xls_name = f.readline()
                if xls_name != sys.argv[1]:
                    with open(r"{}\xls_name.txt".format(BASE_PATH), "w") as ff:
                        ff.write(sys.argv[1])
            else:
                with open(r"{}\xls_name.txt".format(BASE_PATH), "w") as ff:
                    ff.write(sys.argv[1])
            os.system('start "Camera" python Camera.py')
            #os.system('start "Camera" C:\\Users\\hsiaochi\\AppData\\Local\\Continuum\\anaconda3\\envs\\python36\\python Camera.py')
            sleep(5)


if __name__ == "__main__":
    Main()