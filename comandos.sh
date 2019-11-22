#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade
sudo wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list)"
sudo apt -y install libcurl3
sudo apt install expect -y

#Download and Configure MySQL
sudo apt-get -y install zsh htop
# Install MySQL Server in a Non-Interactive mode. Default root password will be "root"
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


sudo apt -y install python3-pip
python3 -m pip install PyMySQL
pip3 install flask

mysql -uroot -proot << EOF
CREATE USER IF NOT EXISTS "delch"@"localhost" IDENTIFIED BY "senha123";
GRANT ALL PRIVILEGES ON *.* TO "delch"@"localhost";
FLUSH PRIVILEGES;
EOF

sudo service mysql restart

sudo mysql -udelch -psenha123 "DROP DATABASE IF EXISTS Cloud;"
mysql -udelch -psenha123 "CREATE DATABASE IF NOT EXISTS Cloud DEFAULT CHARACTER SET utf8 ;"
mysql -udelch -psenha123 "USE Cloud ;"
mysql -udelch -psenha123 "DROP TABLE IF EXISTS Cloud.Tarefas ;"
mysql -udelch -psenha123 "CREATE TABLE IF NOT EXISTS Cloud.Tarefas (Nome VARCHAR(45) UNIQUE,PRIMARY KEY (Nome))ENGINE = InnoDB;"


sudo apt purge expect -y





