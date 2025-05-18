pkg update && pkg upgrade -y
wget -P $PREFIX/bin https://raw.githubusercontent.com/Zureu/laughing-spork/refs/heads/main/ChDDoS.py
mv $PREFIX/bin/XDDoS.py  $PREFIX/bin/XDDoS
chmod +x $PREFIX/bin/XDDoS
XDDoS
