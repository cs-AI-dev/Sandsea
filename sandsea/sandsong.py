import objects
import engine
import gui

def interpretText(text, parsingSandsongInitialTextSend=True):
	if parsingSandsongInitialTextSend: gui.log("Parsing Sandsong ...")



def interpretFile(filedir):
	gui.log("Loading file to parse ...")
	with open(filedir, "r") as f:
		gui.log("    ┣━ done.")
		gui.log("    ┗━ Beginning parse ...")
		interpretText(f.read(), parsingSandsongInitialTextSend=False)
