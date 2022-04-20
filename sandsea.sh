type systemdata/version.dat
echo Installing PIP upgrade.
py -m pip install --upgrade pip
cls
echo Installing required libs.
py -m pip install -r systemdata/requirements.dat -q --no-warn-script-location
cls
py sandsea/sandsea.py loadgui
