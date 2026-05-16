# DeskScout alpha one click installer
# Author: Seth Edwards 
# Version 1.0

def cs(v):
	if v < 1024:
		return str(v)+" B"
	elif v >= 1024 and v < 1_000_024:
		return str(round(v/1024))+" KB"
	elif v > 1_000_024  < 1_000_000_024:
		return str(round(v/1e+6,2))+" MB"
	elif v >= 1_000_000_024:
		return str(round(v/1e+9,2))+" GB"
# Imports
import zipimport,zipfile,urllib.request as request,os,sys,json,shutil,subprocess,ctypes,urllib
from tkinter import messagebox

# Create a temporary folder for the installer
try:
	os.mkdir(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))

except FileExistsError:
	print("Temp directory already exists")
except Exception as e:
	messagebox.showerror("DeskScout Alpha Installer",f"Unable to install DeskScout\n{str(e)}\n\nPhase 1")
	exit(0)

# Add it to the system path
sys.path.append(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))

# Download the UI library
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import gui as sg
except urllib.error.URLError as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\nReason: No internet connection\n{str(e)}\nPhase: 2")
	exit(0)
except OSError:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\nReason: Filesystem Error\n{str(e)}\nPhase: 2")
	exit(0)
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\nReason: Unknown\n{str(e)}\nPhase: 2")
	exit(0)

import gui as sg
sg.theme('SystemDefault')

layout = [
	[sg.Text("Getting ready to install",key="status")],
	[sg.ProgressBar(0,key="prog",size=(20,20))],
	[sg.Text("",key="status2")]
]
window = sg.Window("DeskScout Installer",layout,finalize=True,disable_close=True)
window.refresh()

# Get path for the correct binary
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform]['alpha']
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
import os,io
# Create the apps directors
window['status'].update("Downloading DeskScout Alpha")
window.refresh()
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","app.zip"),'wb+')
	length = int(resp.headers.get("Content-Length"))
	while True:
		x = resp.read(io.DEFAULT_BUFFER_SIZE)
		file.write(x)
		if not x:
			break
		window['status'].update(f"Downloading DeskScout")
		window['status2'].update(f"1/2 {round((file.tell()/length)*100)}% ({cs(file.tell())})")
		window['prog'].UpdateBar(file.tell(),max=length)
		
		window.refresh()
	file.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)

window['status'].update("Installing DeskScout")
window['status2'].update("2/2 Please wait...")
window['prog'].update(visible=False)



window['status'].update("Installing DeskScout")
window.refresh()

# Install the app files
try:
	zip = zipfile.ZipFile(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","app.zip"))
	zip.extractall(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout Alpha"))
	zip.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)

# Clean up
shutil.rmtree(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))
window.close()

# Launch app
subprocess.Popen(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout Alpha','app','DeskScout.pyw')}\"",start_new_session=True)
print("DONE!")