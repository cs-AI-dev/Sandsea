type systemdata/version.dat
echo Installing PIP upgrade
py -m pip install --upgrade pip -q
echo done.
echo Installing required libs
py -m pip install -r systemdata/requirements.dat -q --no-warn-script-location
echo done.
py sandsea/sandsea.py loadgui
