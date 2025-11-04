import zipimport,zipfile,urllib.request as request,os,sys
from tkinter import messagebox

try:
	os.mkdir(os.path.join(os.environ["temp"],"DeskScout Installer"))

except FileExistsError:
	print("Temp directory already exists")
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n{str(e)}\n\nPhase 1")
sys.path.append(os.path.join(os.environ["temp"],"DeskScout_Installer"))

try:
	resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/DeskScout-App/refs/heads/main/mods/gui.py")
	file = open(os.path.join(os.environ["temp"],"DeskScout Installer","gui.py"),'wb+')
	file.write(resp.read())
	file.close()
	import PySimpleGUI as sg
except Exception as e:
	messagebox.showerror("DeskScout Installer",f"Unable to install DeskScout\n\n{str(e)}\nPhase: 2")
