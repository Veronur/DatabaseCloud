#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade
sudo wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list)"
sudo apt -y install libcurl3
sudo apt install -y mysql-server mysql-client
sudo apt install expect -y


mysql -e "DROP DATABASE IF EXISTS Cloud;"
mysql -e "CREATE DATABASE IF NOT EXISTS Cloud DEFAULT CHARACTER SET utf8 ;"
mysql -e "USE Cloud ;"
mysql -e "DROP TABLE IF EXISTS Cloud.Tarefas ;"
mysql -e "CREATE TABLE IF NOT EXISTS Cloud.Tarefas (Nome VARCHAR(45) UNIQUE,PRIMARY KEY (Nome))ENGINE = InnoDB;"



