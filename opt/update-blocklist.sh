#!/bin/sh
set -e
HOSTS_RAW=https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
tmpfile=$(mktemp)

wget -nv -O $tmpfile $HOSTS_RAW

cat /etc/pihole/black.list.d/*.list | awk '{ print "0.0.0.0 "$1 }' >> $tmpfile

# Blocks A records by returning my fake ad server instead. Blocks AAAA records by returning ::
cat $tmpfile | awk '$1 == "0.0.0.0"  { print "10.5.0.1 "$2 }' > /etc/pihole/black.list
cat $tmpfile | awk '$1 == "0.0.0.0"  { print ":: "$2 }' >> /etc/pihole/black.list

rm $tmpfile
systemctl restart dnsmasq
