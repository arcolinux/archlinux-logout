#!/bin/sh

echo "This will install arcolinux-logout files in your system. Existing source files will be overwritten"

if [ "$(groups | grep "root" -c)" -eq 0 ]; then
  echo "This script must be run with root privileges"
  exit 1
fi

if [ ! -r "/etc/arcologout.conf" ]; then
  cp "etc/arcologout.conf" "/etc"
else
  echo "Config file already exists in /etc. It won't be overwritten"
fi

cp -Rf "usr/share" "/usr/"
cp -Rf "usr/local" "/usr/"

echo "files copied"
echo "You can run the app by typing 'arcolinux-logout' in a shell prompt"
echo "NOTE that '/usr/local/bin/' must be included in your system PATH"
