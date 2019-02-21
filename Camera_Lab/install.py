#coding:utf-8
#python:3
import sys
import os
from os import path
import winshell
PYTHON_NAME="Camera_monitor.py"


# 测试完成
def delete_shortcut_from_sendto(argv):
    target = argv
    s = path.basename(target)
    fname = path.splitext(s)[0]
    delfile = path.join(winshell.sendto(), fname + '.lnk')
    winshell.delete_file(delfile)

# 测试完成
def create_shortcut_to_sendto(argv):
    target = argv
    title = 'Camera_other'
    s = path.basename(target)
    fname = path.splitext(s)[0]
    path_ = path.join(winshell.sendto(), fname + '.lnk')
    print(path_)
    if os.path.isfile(path_):
        print("{} exists".format(path_))
        delete_shortcut_from_sendto(target)
    winshell.CreateShortcut(
        Path=path_,#右键sendto快捷方式
        Target=target,
        Icon=(target, 0),
        Description=title)

def Change():
    new_path = os.path.dirname(os.path.realpath(__file__))
    # os.chdir(PYTHON_PATH)
    new_cmd = "python {}\\{} %1".format(new_path, PYTHON_NAME)
    # new_cmd = "C:\\Users\\hsiaochi\\AppData\\Local\\Continuum\\anaconda3\\envs\\python36\\python {}\\{} %1".format(
    #     new_path, PYTHON_NAME)
    with open("{}\\Camera.bat".format(new_path), "r") as f:
        line = f.readline()
    if line == new_cmd:
        print("same")
        return 
    with open("{}\\Camera.bat".format(new_path), "w") as f:
        f.write(new_cmd)
    
if __name__ == "__main__":
    Change()
    try:
        delete_shortcut_from_sendto(sys.argv[1])
    except:
        print("Camera.bat not find; pass")
    create_shortcut_to_sendto(sys.argv[1])
    # os.system("pause")