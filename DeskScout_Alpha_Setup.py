# DeskScout one click installer
# Author: Seth Edwards 
# Version 1.0

print("DeskScout One-Click Installer")
print("Getting ready to install")
# Imports
import zipimport,zipfile,urllib.request as request,os,sys,json,shutil,subprocess,ctypes,urllib,time
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
	print("Creating temporary directory")

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
	print("Downloading UI Toolkit")
	print("Requesting https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import gui as sg
	print("Success!")
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
print("\u001b[2J\u001b[0;0HFollow the prompts on the window appearing shortly or press CTRL+C here to cancel")

# Get path for the correct binary
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform][ptype.lower()]
	
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
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
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f"DeskScout"))
window['status2'].update("Please wait")
window.refresh()
bps = 0
# Download the installer
import io
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/bin/{sys.platform}/logo.ico")
	length = int(resp.headers.get("Content-Length"))
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","logo.ico"),'wb+')
	last = time.time()
	xps = 0
	while True:
		x = resp.read(io.DEFAULT_BUFFER_SIZE)
		file.write(x)
		if time.time()-last >= 1:
			bps = xps
			xps = 0
			last = time.time()
		else:
			xps += len(x)
			
		if not x:
			break
		window['status'].update(f"Downloading DeskScout {ptype}")
		window['status2'].update(f"1/3 {round((file.tell()/length)*100)}% ({cs(file.tell())}) at {cs(bps)}/sec")
		window['prog'].UpdateBar(file.tell(),max=length)
		window.refresh()
		
	file.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
bps = 0
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/bin/{sys.platform}/installer.zip")
	length = int(resp.headers.get("Content-Length"))
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","installer.zip"),'wb+')
	last = time.time()
	xps = 0
	while True:
		x = resp.read(io.DEFAULT_BUFFER_SIZE)
		file.write(x)
		if time.time()-last >= 1:
			bps = xps
			xps = 0
			last = time.time()
		else:
			xps += len(x)
			
		if not x:
			break
		window['status'].update(f"Downloading DeskScout {ptype}")
		window['status2'].update(f"2/3 {round((file.tell()/length)*100)}% ({cs(file.tell())}) at {cs(bps)}/sec")
		window['prog'].UpdateBar(file.tell(),max=length)
		window.refresh()
		
	file.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
# Download the zip
window['status'].update(f"Downloading DeskScout {ptype}")
window.refresh()
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","app.zip"),'wb+')
	length = int(resp.headers.get("Content-Length"))
	xps = 0
	while True:
		x = resp.read(io.DEFAULT_BUFFER_SIZE)
		file.write(x)
		if time.time()-last >= 1:
			bps = xps
			xps = 0
			last = time.time()
		else:
			xps += len(x)
			
		if not x:
			break
		window['status'].update(f"Downloading DeskScout {ptype}")
		window['status2'].update(f"3/3 {round((file.tell()/length)*100)}% ({cs(file.tell())}) at {cs(bps)}/sec")
		window['prog'].UpdateBar(file.tell(),max=length)
		
		window.refresh()
	file.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)

window['status'].update(f"Installing DeskScout {ptype}")
window['status2'].update(visible=False)
window['prog'].update(visible=False)

window.refresh()
window.close()
# Install the installer files
try:
	zip = zipfile.ZipFile(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","installer.zip"))
	zip.extractall(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f"DeskScout {ptype}"))
	zip.close()
except Exception as e:
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout {ptype}\n\n{str(e)}\nPhase: 5")
	exit(0)
resp = subprocess.run(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f"DeskScout {ptype}",'app','updater.py')}\" -file \"{os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","app.zip")}\"",shell=True)
if resp.returncode != 0:
	shutil.rmtree(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))
	window.close()
	messagebox.showerror(f"DeskScout {ptype} Installer",f"Unable to install DeskScout {ptype} Phase: 6")
	exit(0)
shutil.copy(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer","logo.ico"),
			os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f'DeskScout {ptype}',"assets","shortcut.ico"))
import subprocess
import sys
import os

# Get actual desktop path (supports OneDrive)
desktop = subprocess.check_output(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        "[Environment]::GetFolderPath('Desktop')"
    ],
    text=True
).strip()

shortcut = os.path.join(desktop, f"DeskScout {ptype}.lnk")

script = os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f'DeskScout {ptype}','app')

# Your icon file (.ico recommended)
icon = os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f'DeskScout {ptype}',"assets","shortcut.ico")

pythonw = os.path.join(
    os.path.dirname(sys.executable),
    "pythonw.exe"
)

arguments = os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f'DeskScout {ptype}','app','DeskScout.pyw')

powershell_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut}")

$Shortcut.TargetPath = "{pythonw}"
$Shortcut.Arguments = '"{arguments}"'
$Shortcut.WorkingDirectory = "{os.path.dirname(script)}"

# Set icon
$Shortcut.IconLocation = "{icon}"

$Shortcut.Description = "DeskScout"

$Shortcut.Save()
'''

subprocess.run(
    ["powershell", "-Command", powershell_script],
    check=True
)

print("Shortcut created!")
# Clean up
shutil.rmtree(os.path.join(os.environ["temp"],f"DeskScout {ptype} Installer"))
# Launch app
if messagebox.askyesno(f"DeskSccout {ptype} Installer","DeskScout was installed successfully!\nDo you want to launch the app?"):
	subprocess.Popen(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],f"DeskScout {ptype}",'app','DeskScout.pyw')}\"",start_new_session=True)
