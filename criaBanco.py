import os
import boto3
from botocore.exceptions import ClientError
import time


ec2 = boto3.client('ec2',region_name='us-east-2')

instancia = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Owner',
            'Values': ['Lucca Delchairo Costabile']
        }
    ]  
)


def geraKeyPair():
    chaves = ec2.describe_key_pairs()['KeyPairs']
    k=0
    for i in chaves: 
        if i['KeyName']=="Aps3Delch":
            response = ec2.delete_key_pair(KeyName='Aps3Delch')
            response = ec2.create_key_pair(KeyName='Aps3Delch') 
            f= open("Aps3Delch.pem","w+")
            f.write(response['KeyMaterial'])
            #f.close()
            #os.chmod("Aps3Delch.pem", 400)
            break
        k+=1
    if k == len(chaves):
        response = ec2.create_key_pair(KeyName='Aps3Delch')
        f= open("Aps3Delch.pem","w+")
        f.write(response['KeyMaterial'])
        #f.close()
        #os.chmod("Aps3Delch.pem", 400)
    return response

def createSecurityGroup():
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    try:
        SG = ec2.describe_security_groups()['SecurityGroups']
        #print(response)
    except ClientError as e:
        #print('2')
        print(e)

    k=0
    for i in SG: 
        if i['GroupName']=='APS_Delch':
            try:
                response = ec2.delete_security_group(GroupName='APS_Delch')
                #print('Security Group Deleted')
            except ClientError as e:
                #print("1")
                print(e)    
            try:
                response = ec2.create_security_group(GroupName='APS_Delch',
                                                    Description='Security group da APS',
                                                    VpcId=vpc_id)
                security_group_id = response['GroupId']
                #print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
                #print('antes')
                data = ec2.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {'IpProtocol': 'tcp',
                        'FromPort': 5000,
                        'ToPort': 5000,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                        {'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    ])
                #print('depois')
                #print('Ingress Successfully Set %s' % data)
            except ClientError as e:
                #print('3')
                print(e)
            break
        k+=1
    if k == len(SG):
            try:
                response = ec2.create_security_group(GroupName='APS_Delch',
                                                    Description='Security group da APS',
                                                    VpcId=vpc_id)
                security_group_id = response['GroupId']
                #print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

                data = ec2.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {'IpProtocol': 'tcp',
                        'FromPort': 5000,
                        'ToPort': 5000,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                        {'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    ])
                #print('Ingress Successfully Set %s' % data)
            except ClientError as e:
                print(e)    
    return response

for i in instancia['Reservations']:
    for j in i['Instances']:
        idDelete.append(j['InstanceId'])

if (len(idDelete)!= 0):

    response = ec2.terminate_instances(InstanceIds=idDelete)

    waiter = ec2.get_waiter('instance_terminated')
    waiter.wait(InstanceIds=idDelete)

KeyPair = geraKeyPair()
SecurityGroup = createSecurityGroup()
sgid=SecurityGroup['GroupId']
defaultSGid  = ec2.describe_security_groups(GroupNames=['default'])
defaultSGid = defaultSGid['SecurityGroups'][0]['GroupId']
user_data_script = '''#!/bin/bash
cd /home/ubuntu
git clone https://github.com/Veronur/DatabaseCloud.git
cd ../..
sudo sh /home/ubuntu/APS1Coud/comandos.sh
sudo nano /etc/rc.local
echo "#!/bin/sh -e" >> /etc/rc.local
echo "cd .." >> /etc/rc.local
echo "cd home/ubuntu/APS1Coud" >> /etc/rc.local
echo "python3 serverFlask.py" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local
chmod +x /etc/rc.local
sudo reboot'''

instance = ec2i.run_instances(
    ImageId='ami-04b9e92b5572fa0d1',
    InstanceType='t2.micro',
    KeyName='Aps3Delch',
    MaxCount=1,
    MinCount=1,
    SecurityGroupIds=[sgid,defaultSGid],
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType':'instance',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value':'Lucca Delchairo Costabile'
                },
                {
                    'Key': 'Name',
                    'Value':'PROJETO_DELCH'
                }
            ]
        }   
    ])
