echo Starting up Sandsea ...
echo This might take a moment
echo ........................
echo Installing PIP upgrade
py -m pip install --upgrade pip -q
echo done.
echo Installing required libs
py -m pip install -r systemdata/requirements.dat -q
echo done.
py sandsea/sandsea.py
