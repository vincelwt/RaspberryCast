#!/bin/sh

if [ `id -u` -ne 0 ]
then
  echo "Please start this script with root privileges!"
  echo "Try again with sudo."
  exit 0
fi

cat /etc/debian_version | grep 7. > /dev/null
if [ "$?" = "1" ]
then
  echo "This script was designed to run on Rasbian or a similar Debian 7.x distro!"
  echo "Do you wish to continue anyway?"
  while true; do
    read -p "" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 0;;
        * ) echo "Please answer with Yes or No [y|n].";;
    esac
  done
  echo ""
fi

echo "This script will install RaspberryCast"
echo "Do you wish to continue?"

while true; do
  read -p "" yn
  case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit 0;;
      * ) echo "Please answer with Yes or No [y|n].";;
  esac
done
echo ""
echo "============================================================"
echo ""
echo "Installing necessary dependencies... (This could take a while)"
echo ""
echo "============================================================"

apt-get install -y lsof x11-xserver-utils python-pip git wget omxplayer
echo "============================================================"

if [ "$?" = "1" ]
then
  echo "An unexpected error occured!"
  exit 0
fi

pip install youtube-dl

if [ "$?" = "1" ]
then
  echo "An unexpected error occured!"
  exit 0
fi

echo ""
echo "============================================================"
echo ""
echo "Cloning project..."
echo ""
echo "============================================================"

su - pi -c "git clone https://github.com/vincent-lwt/RaspberryCast.git"
mv RaspberryCast/RaspberryCast.sh RaspberryCast.sh
chmod +x RaspberryCast.sh

echo ""
echo "============================================================"
echo ""
echo "Adding project to startup"
echo ""
echo "============================================================"

chmod 666 /dev/tty1

cat > /etc/inittab  << EOF
id:2:initdefault:

si::sysinit:/etc/init.d/rcS

~~:S:wait:/sbin/sulogin

l0:0:wait:/etc/init.d/rc 0
l1:1:wait:/etc/init.d/rc 1
l2:2:wait:/etc/init.d/rc 2
l3:3:wait:/etc/init.d/rc 3
l4:4:wait:/etc/init.d/rc 4
l5:5:wait:/etc/init.d/rc 5
l6:6:wait:/etc/init.d/rc 6

ca:12345:ctrlaltdel:/sbin/shutdown -t1 -a -r now

pf::powerwait:/etc/init.d/powerfail start
pn::powerfailnow:/etc/init.d/powerfail now
po::powerokwait:/etc/init.d/powerfail stop

1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1
2:23:respawn:/sbin/getty 38400 tty2
3:23:respawn:/sbin/getty 38400 tty3
4:23:respawn:/sbin/getty 38400 tty4
5:23:respawn:/sbin/getty 38400 tty5
6:23:respawn:/sbin/getty 38400 tty6

T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100
EOF

cat > /etc/rc.local  << EOF
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"

fi
su - pi -c "/home/pi/RaspberryCast.sh start"
exit 0
EOF


rm setup.sh

echo "============================================================"
echo "Setup was successful!"
echo "Do not delete the 'RaspberryCast' folder as it contains all application data!"
echo "STARTING RASPBERRYCAST..."
echo "============================================================"

su - pi -c "/home/pi/RaspberryCast.sh start"

exit 0
