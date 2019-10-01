import boto3
import click
import botocore

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

def has_pending_snapshot(volume):
    snapshots=list(volume.snapshots.all())
    return snapshots and snapshots[0].state =='pending'

@click.group()
def cli():
    "Shotty manages EC2 instances/Volumes"

@cli.group('snapshots')
def snapshots():
     "Commands for Snapshots"
@snapshots.command('list')
@click.option('--project',default=None,
    help="Only snapshots for tag Name=:<name> ")
@click.option('--all','list_all',default=False,is_flag=True,
    help="lists all snapshots for each volume just not the latest")

def list_snapshots(project,list_all):
    "List of ec2 snapshots"
    instances=filter_instance(project)
    for i in instances :
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(",".join((
                      s.id,
                      v.id,
                      i.id,
                      s.state,
                      s.progress,
                      s.start_time.strftime("%c")
                      )))
                if s.state == "completed" and not list_all : break
    return


@cli.group('volumes')
def volumes():
     "Commands for volumes"
@volumes.command('list')
@click.option('--project',default=None,
    help="Only Volumes for tag Name=:<name> ")

def list_volumes(project):
    "List of ec2 volumes"
    instances=filter_instance(project)
    for i in instances :
        for v in i.volumes.all():
            print(",".join((
            v.id,
            i.id,
            v.state,
            str(v.size)+"GiB",
            v.encrypted and "Encrypted" or "Not encrypted"
            )))
    return


@cli.group('instances')
def instances():
    "Commands for instances"
@instances.command('snapshot',
   help="create snapshots for the instance")
@click.option('--project',default=None,
    help="Only instances for tag Name=:<name> ")

def create_snapshot(project):
    "Creating a Snapshots"
    instances=filter_instance(project)

    for i in instances:

        print ("stopping {0}". format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e :
            print ("Could not stop {0} ".format(i.id)+str(e))
            continue

        i.wait_until_stopped()

        for v in i.volumes.all():
            print("creating snapshots {0}".format(v.id))
            v.create_snapshot(Description="created by python")
        print("Starting Instance{0}".format(i.id))
        i.start()
        i.wait_until_running()
    print ("COMPLETE")
    return

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

        try:
            i.stop()
        except botocore.exceptions.ClientError as e :
            print ("Could not stop {0} ".format(i.id)+str(e))
            continue
    return
@instances.command('start')
@click.option('--project',default=None,
    help="Only instances for tag Name=<project>")
def start_instance(project):
    "Starting of EC2 Instances"
    instances=filter_instance(project)
    for i in instances :
        print("starting instance{0}",i.id)
        try:
            i.start()
        except botocore.exceptions.ClientError as e :
            print ("Could not start {0} ".format(i.id)+str(e))
            continue

    return

     #    print(i.id)
##        print(i.placement['AvailabilityZone'])
#        print(i.state['Name'])
#        print(i.public_dns_name)


if __name__ == '__main__':
   cli()
