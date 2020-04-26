pyinstaller --onedir --name="graphical_ai" src/main.py^
 --add-binary=".venv/Lib/site-packages/sklearn/.libs;."^
 --add-binary=".venv/Lib/site-packages/sklearn;./sklearn"^
 --add-data="src;."

