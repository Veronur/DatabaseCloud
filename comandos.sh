#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade
sudo wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list)"
sudo apt -y install libcurl3
sudo apt install expect -y

sudo apt-get -y install zsh htop
echo "mysql-server-5.6 mysql-server/root_password password root" | sudo debconf-set-selections
echo "mysql-server-5.6 mysql-server/root_password_again password root" | sudo debconf-set-selections
sudo apt install -y mysql-server mysql-client
    sudo mysql_secure_instalation

MYSQL_ROOT_PASSWORD=root

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



mysql -uroot -proot << EOF
CREATE USER IF NOT EXISTS "delch"@"localhost" IDENTIFIED BY "senha123";
GRANT ALL PRIVILEGES ON *.* TO "delch"@"localhost";
GRANT ALL ON *.* TO delch@'%' IDENTIFIED BY 'senha123';
GRANT ALL ON *.* TO delch@'0.0.0.0' IDENTIFIED BY 'senha123';
FLUSH PRIVILEGES;
EOF

mysql -udelch -psenha123 << EOF
DROP DATABASE IF EXISTS Cloud;
CREATE DATABASE IF NOT EXISTS Cloud DEFAULT CHARACTER SET utf8 ;
USE Cloud ;
DROP TABLE IF EXISTS Cloud.Tarefas ;
CREATE TABLE IF NOT EXISTS Cloud.Tarefas (Nome VARCHAR(45) UNIQUE,PRIMARY KEY (Nome))ENGINE = InnoDB;
EOF

sudo /sbin/iptables -A INPUT -i eth0 -p tcp --destination-port 3306 -j ACCEPT
cd /etc/mysql/mysql.conf.d/
sudo sed -i '43 s/^/#/' mysqld.cnf
sudo service mysql restart
