import os
import requests
import json
import urllib
import argparse
from rich.console import Console
from rich.table import Column, Table
from operations import insert, get, delete, update, check_server_status, argument_parser
from utils import check_encryption_key


def main():
    console = Console()
    args = argument_parser()

    # Server address
    host = args.host
    SERVER_URL = host

    # check server availabality
    if check_server_status(SERVER_URL):

        # setup encryption key
        if args.key:
            if check_encryption_key(args.key):
                os.environ['ENC_KEY'] = args.key

            else:
                console.print('Encryption key is not valid', style='bold red')
                exit(-1)

        if args.insert:
            # insert one credential
            cred = {
                'service': args.service,
                'username': args.username,
                'email': args.email,
                'password': args.password
            }
            ROUTE = 'api/add_creds'
            resoponse = insert(cred, SERVER_URL, ROUTE).json()
            if resoponse['status'] == 'success':
                console.print('Credential inserted', style='bold green')
            else:
                console.print(resoponse['message'], style='bold red')

        if args.get:
            # get one or more credentials
            ROUTE = 'api/get_creds_all'
            if args.service is None:
                table = get(SERVER_URL, ROUTE)
                if table:
                    console.print('Listing all credentials', style='bold blue')
                    console.print(table)
                else:
                    console.print('No credentials to show',
                                  style='bold yellow')
            else:
                ROUTE = 'api/get_creds'
                table = get(SERVER_URL, ROUTE, service=args.service)
                if table:
                    console.print(
                        'Listing credentials of service [u]{}[/u]'.format(args.service), style='bold green')
                    console.print(table)
                else:
                    console.print('No credentials to show',
                                  style='bold yellow')

        if args.delete:
            # delete entry by id
            # API route is /api/del_creds/<ID>
            ROUTE = 'api/del_creds/'
            cred_id = args.id
            r = delete(SERVER_URL, ROUTE, cred_id)
            if r.json()['status'] == 'success':
                console.print(
                    'Credential of id [u]{}[/u] deleted successfully'.format(cred_id), style='bold green')

            else:
                console.print(
                    'Could not delete credential of id [u]{}[/u]', style='bold red')

        if args.update:
            # update credential entry
            new_cred = {
                'service': args.service,
                'username': args.username,
                'email': args.email,
                'password': args.password
            }
            ROUTE = '/api/update_creds/'
            # actual route /api/update_creds/<id>
            r = update(SERVER_URL, ROUTE, args.id, new_cred)
            if r.json()['status'] == 'success':
                console.print(
                    'Credentile of id [u]{}[/u] is updated successfully'.format(args.id), style='bold green')
            else:
                console.print(
                    'Could not update credentile of id [u]{}[/u]'.format(args.id), style='bold red')

    else:
        console.print(
            'Server is down, please check server connectivity', style='bold red')


if __name__ == "__main__":
    main()
