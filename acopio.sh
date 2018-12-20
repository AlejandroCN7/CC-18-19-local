#!/bin/bash

# az account list-locations --> Con esto puedo ver las localizaciones disponibles para el grupo de recursos
# Marco que por defecto sea la localización francesouth cuando no especifique localización al crear un grupo de recursos.
az configure --defaults location=francecentral

# A continuación, creamos el grupo de recursos como tal.
az group create --name myResourceGroup

#Una vez se ha creado el grupo de recursos, ya podemos crear la máquina virtual.
# https://docs.microsoft.com/es-es/azure/virtual-machines/linux/quick-create-cli --> Esta guía sirve para poder crear la máquina virtual y saber las opciones que podemos especificar
# El resto de opciones que utilizo las busqué en la terminal escribiendo: az vm create --help
# https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/ --> Con este enlace consulté los distintos tamaños que puedo asignar.
az vm create \
  --resource-group myResourceGroup \
  --name Ubuntu16 \
  --image UbuntuLTS \
  --admin-username alejandro \
  --generate-ssh-keys \
  --size Standard_B1s \
  --public-ip-address myPublicIpAddress \
  --public-ip-address-allocation static
# az vm image list --> Con esto se puede consultar las imágenes disponibles
# https://docs.microsoft.com/es-es/azure/virtual-network/virtual-network-deploy-static-pip-arm-cli--> Así encontre el modo de crear una ip pública para especificarla en ansible

# El siguiente paso sería abrir el puerto 80 para poder dar el servicio de mi aplicación desde ahí
# https://docs.microsoft.com/es-es/azure/virtual-machines/linux/nsg-quickstart --> Aquí es donde encontré la forma de abrir el puerto desde azure CLI
az vm open-port --resource-group myResourceGroup --name Ubuntu16 --port 80

#El paso final sería realizar el provisionamiento de la máquina virtual con ansible, para ello debemos de especificarle la ip de nuestra máquina.
#Encontré la opciones para realizar esto utilizando el comando: ansible-playbook --help
#Una vez encontre el campo que me interesaba, vi que podía ponerlo en JSON y busque una herramienta para poder sacar el campo que me interesaba (jq para sacar la ip pública de la máquina)
IP=`az network public-ip show   --resource-group myResourceGroup   --name myPublicIpAddress  --output json | jq ".ipAddress"`
# Tras mucho tiempo con errores, me di cuenta de que debía de quitarle las dobles comillas.
IP=`echo ${IP/\"/}`
IP=`echo ${IP/\"/}`

#https://stackoverflow.com/questions/44592141/ansible-ad-hoc-command-with-direct-host-specified-no-hosts-matched --> Este es el motivo por el que tuve que ponerle la coma al final de la IP.
ansible-playbook -i "$IP," -e 'host_key_checking=False' -b playbook.yml --user alejandro -v
