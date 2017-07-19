#!/bin/bash

#########################################################################################################
#
# System setup
#
# 3. AML SparkBatch
# 4. AML CLI
#
#########################################################################################################

## Create installation directory for AML bits (SparkBatch, Livy)
AZUREML_INSTALLDIR=/opt/microsoft/azureml
mkdir -p ${AZUREML_INSTALLDIR}

## Create a temp directory for downloads, etc.
echo "Setting up tmp directory"
AZUREML_TMP=/tmp/azureml/
rm -rf ${AZUREML_TMP}
mkdir -p ${AZUREML_TMP}
cd ${AZUREML_TMP}

## Install SparkBatch
echo "Installing azureml spark-batch"
rm -rf ${AZUREML_INSTALLDIR}/azureml
AZUREML_TARFILE=azureml.tar.gz
AZUREML_TARFILEURI=https://amlsamples.blob.core.windows.net/apps/${AZUREML_TARFILE}
wget -nv $AZUREML_TARFILEURI -P ${AZUREML_TMP}
tar -zxf ${AZUREML_TMP}${AZUREML_TARFILE} -C ${AZUREML_INSTALLDIR}

## Starting SparkBatch as service
echo "Starting azureml spark-batch as service"
cat >/etc/systemd/system/multi-user.target.wants/azureml.service <<EOL
[[Unit]
Description=azureml service

[Service]
Type=simple
User=root
Environment=YARN_CONF_DIR=
Environment=SPARK_HOME=/dsvm/tools/spark/current
Environment=PYSPARK_PYTHON=/anaconda/bin/python
Environment=LIVY_URL=http://localhost:8998
Restart=always
RestartSec=5
ExecStart=${AZUREML_INSTALLDIR}/azureml/bin/catalina.sh run
ExecStopPost=rm -rf $CATALINA_HOME/temp/*

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl stop azureml.service
systemctl start azureml.service

## Install AML CLI
echo "Installing azureml cli"

## First upgrade pip and setuptools to avoid running into this issue:
## https://github.com/GoogleCloudPlatform/google-cloud-python/issues/2990
/anaconda/envs/py35/bin/pip install pip setuptools --upgrade
/anaconda/bin/pip install pip setuptools --upgrade

## Anaconda Python 3.5
sudo /anaconda/envs/py35/bin/pip install azure-cli-ml --upgrade
sudo /anaconda/envs/py35/bin/pip install azure-cli --upgrade 
sudo /anaconda/envs/py35/bin/pip install azure-cli-core --upgrade

## Anaconda Python 2.7 
sudo /anaconda/bin/pip install azure-cli-ml --upgrade
sudo /anaconda/bin/pip install azure-cli --upgrade
sudo /anaconda/bin/pip install azure-cli-core --upgrade

## reinstall backports, as the --upgrade flag above causes issues
sudo /anaconda/bin/pip uninstall -y backports.shutil-get-terminal-size
sudo /anaconda/bin/pip install backports.shutil-get-terminal-size

USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)

## place magic
wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/samples/magic/az_ml_magic.py -O ${USER_HOME}/.ipython/profile_default/startup/az_ml_magic.py

## restart kernel
kill $(pgrep -f '/anaconda/bin/python -m ipykernel')

echo "Success."
