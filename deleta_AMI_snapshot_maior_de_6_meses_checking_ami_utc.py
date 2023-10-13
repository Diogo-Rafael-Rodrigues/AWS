import boto3
from datetime import datetime, timedelta, timezone

# Configuração do cliente AWS
ec2 = boto3.client('ec2', region_name='sa-east-1')  # Substitua 'us-east-2' pela sua região

# Calcula a data atual menos 6 meses
seis_meses_antes = datetime.now(timezone.utc) - timedelta(days=180)

# Lista todas as AMIs
images = ec2.describe_images(Owners=['self'])['Images']
# Lista todos os snapshots
response = ec2.describe_snapshots(OwnerIds=['self'])

#variavel para saber quantos foram excluidos
quantidade_AMI_exlcuidas = 0
quantidade_snapshot_exlcuidos = 0


for image in images:
    ami_id = image['ImageId']
    creation_date = image['CreationDate']

    # Converte a data de criação em um objeto datetime
    creation_datetime = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

    # Verifica se a AMI tem mais de 6 meses
    if creation_datetime < seis_meses_antes:
        print(f"Excluindo AMI {ami_id} criada em {creation_datetime}")

        quantidade_AMI_exlcuidas += 1

        # cria e adiciona os ids dos snapshots no LOG
        with open("LOG_Ami.txt", "a") as file:
            file.write(f"{ami_id}\n")
        file.close()
        # Deregistra a AMI (isso também exclui os snapshots associados a ela)
        ec2.deregister_image(ImageId=ami_id)
    else:
        print(f"AMI {ami_id} está dentro do limite de 6 meses e não será excluída.")

for snapshot in response['Snapshots']:
    snapshot_id = snapshot['SnapshotId']
    snapshot_date = snapshot['StartTime']    

    # Verifica se o snapshot é mais antigo do que 6 meses
    if snapshot_date < seis_meses_antes:
        # Verifica se o snapshot está associado a uma AMI
        image_associated = False
        images = ec2.describe_images(Filters=[{'Name': 'block-device-mapping.snapshot-id', 'Values': [snapshot_id]}])
        if images['Images']:
            image_associated = True

        if image_associated:
            print(f"O snapshot {snapshot_id} está associado a uma AMI e não será excluído.")
        else:
            print(f"Excluindo snapshot {snapshot_id} criado em {snapshot_date}")
            
            quantidade_snapshot_exlcuidos += 1
            
            # cria e adiciona os ids dos snapshots no LOG
            with open("arquivo.txt", "a") as file:
                file.write(f"{snapshot_id}\n")
            file.close()
                           
            # Exclui o snapshot
            ec2.delete_snapshot(SnapshotId=snapshot_id)

    else:
        print(f"Snapshot {snapshot_id} está dentro do limite de 6 meses e não será excluído.")

print(f'Foram excluidos {quantidade_AMI_exlcuidas} AMIs ao todo.')
print(f'Foram excluidos {quantidade_snapshot_exlcuidos} snapshots ao todo.')
