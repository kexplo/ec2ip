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
@click.option('--show-instance-id', '-i', is_flag=True, default=False)
@click.option('--show-tag', '-t', is_flag=True, default=True)
@click.option('--include-stopped-instances', '-s', is_flag=True)
def cli(name, find, verbose, show_instance_id, show_tag,
        include_stopped_instances):
    """Find private ip of EC2 instances.\n
    inspired by yeonghoey's ec2ip.py
    (https://github.com/yeonghoey/dotfiles/blob/master/python/ec2ip.py)
    """
    if verbose:
        show_instance_id = show_tag = True
    found_instances = list()
    # for region in boto3.client('ec2').describe_regions()['Regions']:
    #     ec2 = boto3.resource('ec2', region_name=region['RegionName'])
    filter_instance_states = ['running']
    if include_stopped_instances:
        filter_instance_states.append('stopped')
    for region_name in ('ap-northeast-1', 'ap-northeast-2', 'us-east-1'):
        ec2 = boto3.resource('ec2', region_name=region_name)
        instances = ec2.instances.filter(Filters=[
            {'Name': 'instance-state-name',
             'Values': filter_instance_states}])
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
            name_tag = found_tags[0]
            found_instances.append((instance.instance_id, name_tag,
                                    instance.private_ip_address))

    if not found_instances:
        print('Not found', file=sys.stderr)
        return 1
    column_count = 1
    if show_instance_id:
        column_count += 1
    if show_tag:
        column_count += 1
    column_fmt_str = '\t'.join(['{}'] * column_count)
    for instance_id, tag, private_ip in found_instances:
        picked_columns = []
        if show_instance_id:
            picked_columns.append(instance_id)
        if show_tag:
            picked_columns.append(tag)
        picked_columns.append(private_ip)
        print (column_fmt_str.format(*picked_columns))
    return 0


if __name__ == '__main__':
    cli()
