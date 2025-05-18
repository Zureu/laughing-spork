pkg update && pkg upgrade -y
wget -P $PREFIX/bin https://raw.githubusercontent.com/Zureu/laughing-spork/refs/heads/main/ChDDoS.py
mv $PREFIX/bin/ChDDoS.py  $PREFIX/bin/ChDDoS
chmod +x $PREFIX/bin/ChDDoS
ChDDoS
