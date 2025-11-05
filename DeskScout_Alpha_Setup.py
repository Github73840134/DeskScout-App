import zipimport,zipfile,urllib.request as request,os,sys,json,shutil,subprocess
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
window.refresh()
try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/manifest.json")
	path = json.loads(resp.read())[sys.platform]['alpha']
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
window['status'].update("Downloading DeskScout")
window.refresh()

try:
	resp = request.urlopen(f"https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/{path}")
	file = open(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","app.zip"),'wb+')
	file.write(resp.read())
	file.close()
	
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 3")
	exit(0)
window['status'].update("Installing DeskScout")
window.refresh()
try:
	os.mkdir(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout Alpha"))
except FileExistsError:
	messagebox.showinfo("DeskScout Installer","You already have DeskScout Alpha installed. If you want to update please do so via the app. If your app is corrupted delete the app before installing")
	exit(0)
try:
	zip = zipfile.ZipFile(os.path.join(os.environ["temp"],"DeskScout Alpha Installer","app.zip"))
	zip.extractall(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],"DeskScout Alpha"))
	zip.close()
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 4")
	exit(0)
shutil.rmtree(os.path.join(os.environ["temp"],"DeskScout Alpha Installer"))
window.close()
subprocess.Popen(f"pyw \"{os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'DeskScout Alpha','app','DeskScout.pyw')}\"",start_new_session=True)
print("DONE!")