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

apt-get install -y lsof python-pip git wget omxplayer
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

sed -i '/1:23/c\1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1' /etc/inittab

sed -i '/exit/c\su - pi -c \"/home/pi/RaspberryCast.sh start\"\nexit 0' /etc/rc.local

rm setup.sh

echo "============================================================"
echo "Setup was successful!"
echo "Do not delete the 'RaspberryCast' folder as it contains all application data!"
echo "STARTING RASPBERRYCAST..."
echo "============================================================"

su - pi -c "/home/pi/RaspberryCast.sh start"

exit 0
