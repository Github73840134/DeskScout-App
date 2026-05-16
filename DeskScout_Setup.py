# DeskScout alpha one click installer
# Author: Seth Edwards 
# Version 1.0


# Imports
import zipimport,zipfile,urllib.request as request,os,sys,json,shutil,subprocess,ctypes
from tkinter import messagebox

# Create a temporary folder for the installer
try:
	os.mkdir(os.path.join(os.environ["temp"],"DeskScout Installer"))

except FileExistsError:
	print("Temp directory already exists")
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n{str(e)}\n\nPhase 1")
	exit(0)

# Add it to the system path
sys.path.append(os.path.join(os.environ["temp"],"DeskScout"))

# Download the UI library
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],"DeskScout Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import gui as sg
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 2")
	exit(0)

import gui as sg
sg.theme('SystemDefault')

layout = [
	[sg.Text("Getting ready to install",key="status")]
]
window = sg.Window("DeskScout Installer",layout,finalize=True,disable_close=True)
window.refresh()

# Get path for the correct binary
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform]['stable']
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)

# Create the apps directors
try:
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
except FileExistsError:
	

	ans = messagebox.askyesno("DeskScout Installer","You already have DeskScout installed. Do you want to overwrite?")
	if not ans:
		shutil.rmtree(os.path.join(os.environ["temp"],"DeskScout Installer"))
		exit(0)
window['status'].update("Downloading DeskScout (1/2)")
window.refresh()

# Download the installer
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/bin/{sys.platform}/installer.zip")
	file = open(os.path.join(os.environ["temp"],"DeskScout Installer","installer.zip"),'wb+')
	file.write(resp.read())
	file.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
# Download the zip
window['status'].update("Downloading DeskScout (2/2)")
window.refresh()
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],"DeskScout Installer","app.zip"),'wb+')
	file.write(resp.read())
	file.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)

window['status'].update("Installing DeskScout")
window.refresh()

# Install the installer files
try:
	zip = zipfile.ZipFile(os.path.join(os.environ["temp"],"DeskScout Installer","installer.zip"))
	zip.extractall(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
	zip.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 5")
	exit(0)
resp = subprocess.run(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout','app','updater.py')}\" -file \"{os.path.join(os.environ["temp"],"DeskScout Installer","app.zip")}\"",shell=True)
if resp.returncode != 0:
	shutil.rmtree(os.path.join(os.environ["temp"],"DeskScout Installer"))
	window.close()
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 6")
	exit(0)
# Clean up
shutil.rmtree(os.path.join(os.environ["temp"],"DeskScout Installer"))
window.close()

# Launch app
subprocess.Popen(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout','app','DeskScout.pyw')}\"",start_new_session=True)
print("DONE!")