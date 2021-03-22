import requests
import json
import urllib
import argparse
from rich.console import Console
from rich.table import Column, Table


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='set API host', required=True)
    parser.add_argument(
        '-K', '--key', help='set the unique crypotgraphic key', required=False)

    # insertion operation
    parser.add_argument('-I', '--insert', dest='insert',
                        help='insert user credentials', action='store_true')
    # Get operation
    parser.add_argument('-G', '--get', dest='get',
                        help='get all creds', action='store_true')
    # Delete operation
    parser.add_argument('-D', '--delete', dest='delete',
                        help='delete entry credentials table', action='store_true')
    # Update operation
    parser.add_argument('-U', '--update', dest='update',
                        help='upgrade entry', action='store_true')

    parser.add_argument('-i', '--id', dest='id', help='set id')
    parser.add_argument('-s', '--service', dest='service',
                        help='set service name')
    parser.add_argument('-u', '--user', dest='username', help='set username')
    parser.add_argument('-e', '--email', dest='email', help='set user email')
    parser.add_argument('-p', '--password', dest='password',
                        help='set user password')

    args = parser.parse_args()
    return args


def check_server_status(url):
    try:
        requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False


def insert(cred, url, route):
    r = requests.post(url+route, json=cred)
    return r


def get(url, route, service=None):

    if service is None:
        r = requests.get(url+route)
        response = r.json()
        if isinstance(response, list) and response[0]['status'] == 'success':
            # Consruct table
            table = Table(show_header=True, header_style='bold white')
            table.add_column('ID', style='dim', width=5)
            table.add_column('Service')
            table.add_column('Username')
            table.add_column('Email')
            table.add_column('Password')

            for cred in response:
                table.add_row(str(cred['id']), cred['service'],
                              cred['username'], cred['email'], cred['password'])

            return table
    else:
        r = requests.get(url+route, params={'service': service})
        response = r.json()
        if isinstance(response, list) and response[0]['status'] == 'success':
            # Consruct table
            table = Table(show_header=True, header_style='bold white')
            table.add_column('ID', style='dim', width=5)
            table.add_column('Service')
            table.add_column('Username')
            table.add_column('Email')
            table.add_column('Password')

            for cred in resoponse:
                table.add_row(str(cred['id']), cred['service'],
                              cred['username'], cred['email'], cred['password'])
            return table


def delete(url, route, cred_id):
    r = requests.delete(url+route+'{}'.format(cred_id))
    return r


def update(url, route, cred_id, new_cred):
    r = requests.put(url+route+'{}'.format(cred_id), json=new_cred)
    return r
