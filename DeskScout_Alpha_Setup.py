import zipimport,zipfile,urllib.request as request,os,sys,json
from tkinter import messagebox

try:
	os.mkdir(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))

except FileExistsError:
	print("Temp directory already exists")
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n{str(e)}\n\nPhase 1")
	exit(0)
sys.path.append(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))

try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import PySimpleGUI as sg
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 2")
	exit(0)
import PySimpleGUI as sg

layout = [
	[sg.Text("Getting ready to install",key="status")]
]
window = sg.Window("DeskScout Installer",layout,finalize=True,no_titlebar=True)
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform]['alpha']
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
window['status'].update("Downloading DeskScout")
try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","app.zip"),'wb+')
	file.write(resp.read())
	file.close()
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
window['status'].update("Installing DeskScout")
try:
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout"))
except IsADirectoryError:
	messagebox.showinfo("DeskScout Installer","You already have DeskScout installed. If you want to update please do so via the app. Otherwise delete the app before installing")