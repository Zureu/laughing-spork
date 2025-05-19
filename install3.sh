pkg update && pkg upgrade -y
wget -P $PREFIX/bin https://raw.githubusercontent.com/Zureu/laughing-spork/refs/heads/main/Botwa.py
mv $PREFIX/bin/Botwa.py  $PREFIX/bin/Botwa
chmod +x $PREFIX/bin/Botwa
Botwa
