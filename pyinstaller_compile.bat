pyinstaller --onedir --noconfirm --clean --name="graphical_ai" src/main.py^
 --hidden-import="tensorflow"^
 --add-binary=".venv/Lib/site-packages/sklearn/.libs;."^
 --add-binary=".venv/Lib/site-packages/sklearn;./sklearn"^
 --exclude-module="tkinter"^
 --exclude-module="grpc"^
 --exclude-module="h5py"^
 --add-data="src;."

cd dist/graphical_ai
graphical_ai
cd ../..
