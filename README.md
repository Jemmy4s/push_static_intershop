# push_static_intershop
Push static file intershop


## Install : 

We need to have `python 3.8` and `pip`

`pip install pyyaml`

`pip install`

## Configure :

serveur_path: 'server cartridge'
ssh_key_dir: "full path of you private key"
ssh_key_path: "XXX.pri"
serv_dev: "isas1@1.1.1.14.1:"
projet_path: ''
commande:  "scp -i" 

## Example result : 
scp -i XXX.pri 
C:\ish\projects\ish-rajasmart-7\src\my_cart\staticfiles\cartridge\localizations\static.pipeline isas1@1.1.1.14.1:/opt/intershop/XXX/release/localizations/static.pipeline