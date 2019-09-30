import boto3
import click
session=boto3.Session(profile_name='shotty')
ec2=session.resource('ec2')

def filter_instance(project):
    instances=[]
    if project :
       filters=[{'Name':'tag:Name','Values':[project]}]
       instances=ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    "Commands for instances"
@instances.command('list')
@click.option('--project',default=None,
    help="Only instances for tag Name=:<name> ")

def list_instances(project):
    "List of ec2 instances"
    instances=filter_instance(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        print (','.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Name','No Tags')
        )))
    return
@instances.command('stop')
@click.option('--project',default=None,
    help="Only instances for tag Name=:<name> ")
def stop_instance(project):
    "Stopping of EC2 Instance"
    instances=filter_instance(project)
    for i in instances:
        print ("stopping instance{0}",i.id)
        i.stop()
    return
@instances.command('start')
@click.option('--project',default=None,
    help="Only instances for tag Name=<project>")
def start_instance(project):
    "Starting of EC2 Instances"
    instances=filter_instance(project)
    for i in instances :
        print("starting instance{0}",i.id)
        i.start()
    return

     #    print(i.id)
##        print(i.placement['AvailabilityZone'])
#        print(i.state['Name'])
#        print(i.public_dns_name)


if __name__ == '__main__':
   instances()
