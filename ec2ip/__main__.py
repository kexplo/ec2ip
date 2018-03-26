# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys

import boto3
import click


__all__ = ['cli']


@click.command()
@click.argument('name')
@click.option('--find', '-f', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def cli(name, find, verbose):
    """Find private ip of EC2 instances.\n
    inspired by yeonghoey's ec2ip.py
    (https://github.com/yeonghoey/dotfiles/blob/master/python/ec2ip.py)
    """
    found_instances = {}
    # for region in boto3.client('ec2').describe_regions()['Regions']:
    #     ec2 = boto3.resource('ec2', region_name=region['RegionName'])
    for region_name in ('ap-northeast-1', 'ap-northeast-2'):
        ec2 = boto3.resource('ec2', region_name=region_name)
        instances = ec2.instances.filter(Filters=[
            {'Name': 'instance-state-name',
             'Values': ['running']}])
        for instance in instances:
            if not instance.tags:
                continue
            if find:
                found_tags = [tag['Value'] for tag in instance.tags
                            if tag['Key'] == 'Name' and name in tag['Value']]
            else:
                found_tags = [tag['Value'] for tag in instance.tags
                            if tag['Key'] == 'Name' and tag['Value'] == name]
            if not found_tags:
                continue
            found_instances[found_tags[0]] = instance.private_ip_address
            # found_instances[found_tags[0]] = instance.instance_id

    if not found_instances:
        print('Not found', file=sys.stderr)
        return 1
    for tag, private_ip in found_instances.viewitems():
        if find or verbose:
            print ('{0}\t{1}'.format(tag, private_ip))
    return 0


if __name__ == '__main__':
    cli()
