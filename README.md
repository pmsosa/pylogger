<h1>Pylogger</h1>

<h3>A Python Keylogger for Windows</h3>



<h3>DISCLAIMERS:</h3> 

1. **DON'T DO BAD THINGS.** THIS PROGRAM IS MEANT FOR PERSONAL USES ONLY. USE IT ONLY IN COMPUTERS WHERE YOU HAVE AUTHORIZED ACCESS.
2. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

<hr>

### Read this program's postmortem at [my blog](http://konukoii.com/blog/2016/09/27/capture-the-keys-chapter-2-pylogger/). ###

<h3>Requirements</h3>
 
- [PyWin32](http://starship.python.net/~skippy/win32/Downloads.html)
- [PyHook](https://sourceforge.net/projects/pyhook/)
- [Py2Exe](http://py2exe.org/)


<h3>Setup</h3>

- Step 1. Customize pylogger.py variables to your desire
  - You can customize the trigger passwords, the filename, location, extensions, filesize, among other things.

- Step 2. Turn the pylogger**.py** to a pylogger**.pyw** so that the console doesn't show up when you run the program

- Step 3. Customize setup.py to your desire.
  - You can customize the name of the executable, description, and other options.

- Step 4. Run **python setup.py**. This will make the executable which you will find in the dist/ folder along with any other dependencies.

- Step 5. Run the program. Now you are key-logging!

<h3>Triggers</h3>

While the program is running you can activate special triggers that perform different operations. Here are the following implemented triggers.

| Triggers      | String to Type		 |  Explanation 				   		  |
|:------------- |:----------------------:| :------------------------------------: |
| Kill			| "pykill" 				 | Destroy Itself (including logs) 		  |
| Status     	| "pystatus" 			 | Makes a Beeping sound	    		  |
| Dump			| "pydump<drive_letter>" | Copy all logs to provided drive letter |
| Pause/Resume	| "pypause"/"pyresume"	 | Pause/Resume logging 				  |
| Quit			| "pyquit"				 | Turn Off Keylogger 				  	  | 

<h3>Ideas</h3>

- **Add Encryption to the logging process:** Provides an extra layer of security, so that if someone finds those logs, they can't see what is inside them.
- **Zip logs:** Provides simplicity and more stealth
- **Data exfiltration:** Right now the only way for data exfiltration is through the dump command, which requires physical access to the machine. There are a lot of interesting and different ways to do this. Since the purpose of this program was to keylog my own computer, I have not added any data exfiltration methods.
- **Arguments in a .conf file** Not sure if I even want to do this. I like having everything in one executable. However it would be nice to be able to change values once the executable has been made.
- **More interesting methods? If you have any ideas feel free to add an issue.**
