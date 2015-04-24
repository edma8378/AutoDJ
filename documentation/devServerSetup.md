Hugs and Kisses from your alumni-senpai.

This is the documentation for how to build your very own development server that will simulate the environment that will be used at the Radio station! Setting this up requires a few things. I built this on a Raspberry Pi B+ and used the Raspbian OS. For the entire semester I kept the server running in my bedroom closet plugged into a hard drive full of music. In addition to following the instructions below, make sure you configure your router to allow port forwarding for port 22 (SSH) and port 80 (web server) to the server (DHCP is useful here).

This setup has some security holes that can be easily fixed as long as the admin is aware of them. Make sure to set up fail2ban so the server is safe from attacks. Also make sure that the files holding your gmail password and your github password are hidden away in root folder. Additionally, make sure you impose strong passwords for all users, and try to separate out user privileges accordingly.


I did not configure a DNS server because I secretly enjoy typing in ip addresses in web browsers.

Finally, these instructions are not the final word here. Make sure to customize the server to suit your team, add more users/groups, make some neat scripts, do some cool shit.

Don’t get hacked, RTFM,
~Eric “Fluffy” Lobato

--------------------------------------------------------------------------

#Documentation for RasbPI

After installing the operating system and getting the system off the ground.

##Step 1:

Added users and configured some groups: developers- allows group ownership on files, nosu- make sure nobody can elevate to root.

##Step 2: Configure sudo permissions using visudo:


root ALL=(ALL:ALL) ALL
testing-user ALL=(ALL:ALL) /usr/bin/apt-get install *, /bin/cp, /usr/bin/wget, /usr/bin/make install, /usr/local/bin/webdriver-manager *

##Step 3: Run Scripts:

ipchecker and firewallconfig, I would personally recommend something to make festive messages of the day

##Step 4: Create Cronjobs:

	Note: For the git pull cronjob to work you MUST configure the login info to be stored locally,
	see the instructions under EXTRA.

```
0 */2 * * * /root/Documents/ipchecker.sh
10 * * * * cd /var/www/AutoDJ && git pull -f origin dev
0 22 * * * cd /home/noize-machine/AutoDJ/backend  && ./PlayMaker.py tomorrow
0 22 * * * ps -ef | grep "[W]atchdog.py" | head -n1 >& /dev/null && if [[ $? -eq 0 ]]; then         echo "watchdog ACTIVE"; else cd /home/noize-machine/AutoDJ/backend && nohup ./Watchdog.py < /dev/null > nohup.out 2> nohup.out & ; fi
```

##Step 5:    Dependencies
install:
git
fail2block -> a ssh blocker
iceweasel -> The superior web browser
apache2
mysql-server
 php5 libapache2-mod-php5
heirloom-mailx


##Step 6:   Some security!
sshd_config
PermitRootlogin: no


/etc/pam.d/su 
-> Enable users in nosu group to not use su


Configure fail2ban:

in /etc/fail2ban/jail.conf -> enable ssh and apache ip banning
set bantime to something crazy high
	consider whitelisting your teammates……..or not. I promise they will get locked out just by mistyping their passwords.


Set timezone
 cp /usr/share/zoneinfo/America/Denver /etc/localtime


##Step 7:
EXTRA
sudo update-alternatives --config editor  -> set vim as default #nanoisforplebs
Git setup:
git clone https://github.com/edma8378/AutoDJ.git  -> in /var/www/
git checkout -b dev origin/dev
set up auto login -> sudo  git config credential.helper store /root/info
   				  git pull -f origin dev
   				  log in [password will be stored in .git-credentials in /root]
generate playlists and set up cron
Adding Your own music to be played:


Mount the music hard drive:
with the music drive attached:
    mkdir /mnt/Music-Drive
    sudo blkid to find uuid


    edit fstab:
     /mnt/Music/folder	 /var/www/AutoDJ/app/music/rotation	none   gid=1005,umask=001,bind 	0 	0

    sudo mount -a

See other documentation for how to customize music times/ shows/playlists








##Scripts for you to use:

----------------------------------------------------------------------------------------------------------------------------

##ipchecker.sh
```
#!/bin/bash

#this is a script to check the WAN address of a machine
#and email a user if it has changed. -> code review version
#This is amazing if you set up your server in your closet and don’t have a static ipaddress from Comcast
# Users store this file in a secure place, run as a root cronjob, and add your gmail account and password to it.
#Users will also have to allow untrusted emails in their gmail account settings
#Requires heirloom mailx -> see dependancies in setup guide
#Written by Eric Lobato 2014-2015, allowed for use by all radio1190 projects teams

curl -s checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//' > current_ip

diff -q current_ip old_ip
if [ $? -gt 0 ]
then
        echo "Ips have changed" && cat current_ip | mailx -v -r "YOUREMAIL@gmail.com" -s "Your new web-server IP" -S
        smtp="smtp.gmail.com:587" -S smtp-use-starttls -S smtp-auth=login -S smtp-auth-user="elobato92" -S
        smtp-auth-password="(<YOURGMAILPASSWORD>" -S ssl-verify=ignore elobato92@gmail.com && mv current_ip old_ip

else
        echo "The address has not changed."

fi
```

-----------------------------------------------------------------------------------------------------------------

##		iptables_default.sh
``` 
#!/bin/bash
#
# This is a script to generate default rules for iptables, the linux firewall
# Run this once during server setup to build the firewall. 
#Written by Eric Lobato 2014-2015, allowed for use by all radio 1190 teams
#
# Flush all current rules from iptables
#
 iptables -F
#
# Allow SSH connections on tcp port 22
# This is essential when working on remote servers via SSH to prevent locking yourself out of the system
#
 iptables -A INPUT -p tcp --dport 22 -j ACCEPT
#
# Set default policies for INPUT, FORWARD and OUTPUT chains
#
 iptables -P INPUT DROP
 iptables -P FORWARD DROP
 iptables -P OUTPUT ACCEPT
#
# Set access for localhost
#
 iptables -A INPUT -i lo -j ACCEPT
#
# Accept packets belonging to established and related connections
#
 iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#
# Save settings
#
 /sbin/service iptables save
#
# List rules
#
 iptables -L -v
```

