# DeskScout one click installer
# Author: Seth Edwards 
# Version 1.0


# Imports
import zipimport,zipfile,urllib.request as request,os,sys,json,shutil,subprocess,ctypes,urllib
from tkinter import messagebox
ptype = "Alpha" #Blank for stable
def cs(v):
	if v < 1024:
		return str(v)+" B"
	elif v >= 1024 and v < 1_000_024:
		return str(round(v/1024))+" KB"
	elif v > 1_000_024  < 1_000_000_024:
		return str(round(v/1e+6,2))+" MB"
	elif v >= 1_000_000_024:
		return str(round(v/1e+9,2))+" GB"

# Create a temporary folder for the installer
try:
	os.mkdir(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))

except FileExistsError:
	print("Temp directory already exists")
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n{str(e)}\n\nPhase 1")
	exit(0)

# Add it to the system path
sys.path.append(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))

# Download the UI library
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import gui as sg
except urllib.error.URLError as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\nReason: No internet connection\n{str(e)}\nPhase: 2")
	exit(0)
except OSError:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\nReason: Filesystem Error\n{str(e)}\nPhase: 2")
	exit(0)
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\nReason: Unknown\n{str(e)}\nPhase: 2")
	exit(0)
import gui as sg
sg.theme('SystemDefault')

layout = [
	[sg.Text("Getting ready to install",key="status")],
	[sg.ProgressBar(0,key="prog",size=(20,20))],
	[sg.Text("",key="status2")]

]
window = sg.Window(f"DeskScout {ptype} Installer",layout,finalize=True,disable_close=True)
window.refresh()

# Get path for the correct binary
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform][ptype.lower()]
	
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype}Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)

# Create the apps directors
try:
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
except FileExistsError:
	

	ans = messagebox.askyesno(f"DeskScout {ptype} Installer","You already have DeskScout installed. Do you want to overwrite?")
	if not ans:
		shutil.rmtree(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))
		exit(0)
	shutil.rmtree(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
window['status2'].update("Please wait")
window.refresh()

# Download the installer
import io
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/bin/{sys.platform}/installer.zip")
	length = int(resp.headers.get("Content-Length"))
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","installer.zip"),'wb+')
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
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
# Download the zip
window['status'].update("Downloading DeskScout")
window.refresh()
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","app.zip"),'wb+')
	length = int(resp.headers.get("Content-Length"))
	while True:
		x = resp.read(io.DEFAULT_BUFFER_SIZE)
		file.write(x)
		if not x:
			break
		window['status'].update(f"Downloading DeskScout")
		window['status2'].update(f"2/2 {round((file.tell()/length)*100)}% ({cs(file.tell())})")
		window['prog'].UpdateBar(file.tell(),max=length)
		
		window.refresh()
	file.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)

window['status'].update("Installing DeskScout")
window['status2'].update(visible=False)
window['prog'].update(visible=False)

window.refresh()
window.close()
# Install the installer files
try:
	zip = zipfile.ZipFile(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","installer.zip"))
	zip.extractall(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
	zip.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 5")
	exit(0)
resp = subprocess.run(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout','app','updater.py')}\" -file \"{os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","app.zip")}\"",shell=True)
if resp.returncode != 0:
	shutil.rmtree(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))
	window.close()
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout Phase: 6")
	exit(0)
# Clean up
shutil.rmtree(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))
# Launch app
subprocess.Popen(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout','app','DeskScout.pyw')}\"",start_new_session=True)
print("DONE!")