#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade
sudo wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list)"
sudo apt -y install libcurl3
sudo apt install -y mysql-server mysql-client
sudo apt install expect -y


#Download and Configure MySQL
sudo apt-get -y install zsh htop
# Install MySQL Server in a Non-Interactive mode. Default root password will be "root"
echo "mysql-server-5.6 mysql-server/root_password password root" | sudo debconf-set-selections
echo "mysql-server-5.6 mysql-server/root_password_again password root" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
sudo mysql_secure_instalation


// Not required in actual script
MYSQL_ROOT_PASSWORD=senha123

SECURE_MYSQL=$(expect -c "
set timeout 10
spawn mysql_secure_installation
expect \"Enter current password for root (enter for none):\"
send \"$MYSQL\r\"
expect \"Change the root password?\"
send \"n\r\"
expect \"Remove anonymous users?\"
send \"y\r\"
expect \"Disallow root login remotely?\"
send \"y\r\"
expect \"Remove test database and access to it?\"
send \"y\r\"
expect \"Reload privilege tables now?\"
send \"y\r\"
expect eof
")

echo "$SECURE_MYSQL"

aptitude -y purge expect



mysql -e "DROP DATABASE IF EXISTS Cloud;"
mysql -e "CREATE DATABASE IF NOT EXISTS Cloud DEFAULT CHARACTER SET utf8 ;"
mysql -e "USE Cloud ;"
mysql -e "DROP TABLE IF EXISTS Cloud.Tarefas ;"
mysql -e "CREATE TABLE IF NOT EXISTS Cloud.Tarefas (Nome VARCHAR(45) UNIQUE,PRIMARY KEY (Nome))ENGINE = InnoDB;"

sudo apt install python3-pip
python3 -m pip install PyMySQL
