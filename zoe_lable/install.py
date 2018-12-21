#coding:utf-8
#python:3
import sys
import os
from os import path
import winshell
PYTHON_NAME="zoe_lib.py"

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
    title = 'lib_other'
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

# 测试完成
def delete_shortcut_from_desktop(argv):
    target = argv
    s = path.basename(target)
    fname = path.splitext(s)[0]
    delfile = path.join(winshell.desktop(), fname + '.lnk')
    winshell.delete_file(delfile)

# 测试完成
def create_shortcut_to_desktop(argv):
    target = argv
    title = 'lib_other'
    s = path.basename(target)
    fname = path.splitext(s)[0]

    winshell.CreateShortcut(
        Path=path.join(winshell.desktop(), fname + '.lnk'),#桌面快捷方式
        Target=target,
        Icon=(target, 0),
        Description=title)

# 未测试
def create_shortcut_to_startup(argv):
    target = argv
    title = '我的快捷方式'
    s = path.basename(target)
    fname = path.splitext(s)[0]
    winshell.CreateShortcut(
        Path=path.join(winshell.startup(),
                       fname + '.lnk'),
        Target=target,
        Icon=(target, 0),
        Description=title)

# 未测试
def delete_shortcut_from_startup(argv):
    target = argv
    s = path.basename(target)
    fname = path.splitext(s)[0]
    delfile = path.join(winshell.startup(), fname + '.lnk')
    winshell.delete_file(delfile)

def Change():
    new_path = os.path.dirname(os.path.realpath(__file__))
    new_cmd = "python {}\\{} %1".format(new_path, PYTHON_NAME)
    with open("{}\\lib.bat".format(new_path), "r") as f:
        line = f.readline()
    if line == new_cmd:
        print("same")
        return 
    with open("{}\\lib.bat".format(new_path), "w") as f:
        f.write(new_cmd)
    
if __name__ == "__main__":
    Change()
    create_shortcut_to_sendto(sys.argv[1])
    # delete_shortcut_from_sendto(sys.argv[1])
    
    # create_shortcut_to_desktop(sys.argv[1])
    # delete_shortcut_from_desktop(sys.argv[1])

    # create_shortcut_to_startup(sys.argv[1])
    os.system("pause")