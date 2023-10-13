Este documento tem como objetivo auxiliar no uso do Script.
O script irá listar as ami com mais de 6 meses, irá desregistra-las, em seguida ira excluir os snapshots com mais de 6 meses.
Você pode alterar o tempo de rentenção alterando esse parametro: seis_meses_antes = datetime.now(timezone.utc) - timedelta(days=180) <--- mude o 180 para o valor desejado.


-------------------Dependencias----------------------------
EC2 ou cloud shell
Role ec2 full acess, adicionar a role na EC2
Linux- apt-get update - apt install pip
Python3:pip install boto3 / botocore

-------------------Criar o documento----------------------

Crie um documento:
nano script_limpa_ami_snapshot.py
cole o conteudo do do codigo.
Altere os paremtros necessários
Salve: ctrl+o, ctrl+x

------------------Executando----------------------------

Para executar o script:
python3 script_limpa_ami_snapshot.py




