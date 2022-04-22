import objects
import engine
import gui

def interpretText(text, parsingSandsongInitialTextSend=True, mode=None):
	if parsingSandsongInitialTextSend:
		gui.log("Parsing Sandsong ...")

	if mode == None:
		return False
	elif mode == 0:

	elif mode == 1:

	elif mode == 2:

	else:
		return False

def interpretFile(filedir):
	gui.log("Loading file to parse ...")
	if len(filedir.split(".")) == 3 and filedir.split(".")[2] == in ["song", "sandsong"]
	with open(filedir, "r") as f:
		gui.log("    ┣━ done.")
		gui.log("    ┗━ Beginning parse ...")
		tid = filedir.split(".")[1]
		if tid in ["a", "arc", "archive"]:
			t = 0
		elif tid in ["gp", "gproc", "genp", "genproc", "genprocess"]:
			t = 1
		elif tid in ["d", "dat", "data"]:
			t = 2
		else:
			gui.log("Invalid file format.")
			return False
		interpretText(f.read(), parsingSandsongInitialTextSend=False, t)
