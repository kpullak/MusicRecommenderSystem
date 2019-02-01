
# Install necessary packages

sudo apt-get -y update
sudo apt-get install -y cookiecutter
sudo apt-get install unzip
sudo apt-get -y update
sudo apt-get install -y python-pip
sudo apt-get install -y python3-pip

export AIRFLOW_GPL_UNIDECODE=yes

# Install remaining packages
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
sudo pip3 install -r requirements.txt
cd

# Setup CRISP-DM Structure
# unzip CookieCutter.zip
# cd
# cookiecutter ~/CookieCutter

#
# Update & install dependencies
#
sudo apt-get install -y zip unzip curl bzip2 python-dev build-essential git libssl1.0.0 libssl-dev \
    software-properties-common debconf-utils python-software-properties python-pip

#
# Install Java and setup ENV
#
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get -y update
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
sudo apt-get install -y oracle-java8-installer oracle-java8-set-default 

export JAVA_HOME=/usr/lib/jvm/java-8-oracle
echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >>~/.bash_profile
echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >>~/.bashrc
source /etc/environment
echo $JAVA_HOME

#
# Install Miniconda
#
#echo "curl -sLko /tmp/Miniconda3-latest-Linux-x86_64.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh"
#curl -sLko /tmp/Miniconda3-latest-Linux-x86_64.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
#chmod +x /tmp/Miniconda3-latest-Linux-x86_64.sh
#/tmp/Miniconda3-latest-Linux-x86_64.sh -b -p ~/anaconda

#export PATH=~/anaconda/bin:$PATH
#echo 'export PATH=~/anaconda/bin:$PATH' >>~/.bash_profile

sudo apt-get install -y python3 python3-dev python3-numpy python3-scipy python3-setuptools python3-tk


#
# Install Spark
#
echo "wget http://d3kbcqa49mib13.cloudfront.net/spark-1.6.2-bin-hadoop2.6.tgz"
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.6.2-bin-hadoop2.6.tgz
tar -xzf spark-1.6.2-bin-hadoop2.6.tgz
rm spark-1.6.2-bin-hadoop2.6.tgz

echo "wget https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-hadoop2.6.tgz"
wget https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-hadoop2.6.tgz
tar -xzf spark-2.0.0-bin-hadoop2.6.tgz
rm spark-2.0.0-bin-hadoop2.6.tgz
cd ~

#echo "" >> ~/.bash_profile
echo "# Spark environment setup" >>~/.bash_profile
echo "# Spark environment setup" >>~/.bashrc
export SPARK_HOME=~/spark-2.0.0-bin-hadoop2.6
echo 'export SPARK_HOME=~/spark-2.0.0-bin-hadoop2.6' >>~/.bash_profile
echo 'export SPARK_HOME=~/spark-2.0.0-bin-hadoop2.6' >>~/.bashrc
export PATH=$PATH:$SPARK_HOME/bin
echo 'export PATH=$PATH:$SPARK_HOME/bin' >>~/.bash_profile
echo 'export PATH=$PATH:$SPARK_HOME/bin' >>~/.bashrc

export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3
#export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

echo 'export PYSPARK_PYTHON=/usr/bin/python3' >>~/.bash_profile
echo 'export PYSPARK_DRIVER_PYTHON=/usr/bin/python3' >>~/.bash_profile
#echo 'export PYSPARK_DRIVER_PYTHON_OPTS="notebook"' >>~/.bash_profile
echo 'export PYSPARK_PYTHON=/usr/bin/python3' >>~/.bashrc
echo 'export PYSPARK_DRIVER_PYTHON=/usr/bin/python3' >>~/.bashrc
#echo 'export PYSPARK_DRIVER_PYTHON_OPTS="notebook"' >>~/.bashrc

## Kafka install and setup
#
cd
echo "wget https://archive.apache.org/dist/kafka/0.10.1.0/kafka_2.10-0.10.1.0.tgz"
wget https://archive.apache.org/dist/kafka/0.10.1.0/kafka_2.10-0.10.1.0.tgz
tar -xzf kafka_2.10-0.10.1.0.tgz
rm kafka_2.10-0.10.1.0.tgz
echo "# Kafka environment setup" >>~/.bash_profile
echo "# Kafka environment setup" >>~/.bashrc
export KAFKA_HOME=~/kafka_2.10-0.10.1.0
echo 'export KAFKA_HOME=~/kafka_2.10-0.10.1.0' >>~/.bash_profile
echo 'export KAFKA_HOME=~/kafka_2.10-0.10.1.0' >>~/.bashrc


## MongoDB installation

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update
sudo apt-get install -y mongodb-org
# Pin the versions of MongoDB
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections


## Zookeeper installation

wget http://mirror.jax.hugeserver.com/apache/zookeeper/stable/zookeeper-3.4.10.tar.gz
tar -xzf zookeeper-3.4.10.tar.gz
rm zookeeper-3.4.10.tar.gz
export ZOOKEEPER_HOME=~/zookeeper-3.4.10
echo 'export ZOOKEEPER_HOME=~/zookeeper-3.4.10' >>~/.bash_profile
echo 'export ZOOKEEPER_HOME=~/zookeeper-3.4.10' >>~/.bashrc


## RStudio Installation

cd
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
sudo apt-get update
sudo apt-get install r-base r-base-dev
sudo apt-get install gdebi-core
wget https://download1.rstudio.org/rstudio-1.1.423-amd64.deb
sudo gdebi rstudio-1.1.423-amd64.deb
rm rstudio-1.1.423-amd64.deb

## Set project directory

export PROJECT_HOME=$(pwd)
echo 'export PROJECT_HOME=$(pwd)' >>~/.bash_profile
echo 'export PROJECT_HOME=$(pwd)' >>~/.bashrc

source ~/.bash_profile
source ~/.bashrc
#
# Cleanup
#
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

echo "DONE!"

