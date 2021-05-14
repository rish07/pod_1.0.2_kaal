#/usr/bin/python3

import sys
import os


import datetime
import json
import os
import pathlib
import click
import requests
import subprocess

root_dir = ""
credentials_file_name = "creds.json"
status_file_name = "status"
base_url = "https://kaalbackend.herokuapp.com/"

def read_user_data():

    credentials_file_path = os.path.join(root_dir, credentials_file_name)

    with open(credentials_file_path, 'r') as file:

        json_object = json.load(file)
        return json_object

@click.command('register')
def register_user():

    click.echo("👋 Welcome to Kaal !")
    click.echo()

    code = click.prompt("Enter your secret code here", type=str)
    click.echo()

    click.echo("⏱️  Please wait while your code is being validated!")
    click.echo()

    credentials_file_path = os.path.join(root_dir, credentials_file_name)

    # section to contact the backend API to validate code

    response = requests.post(
        "{}/validate".format(base_url), json.dumps({"userHash": code})
    )

    if response.status_code == 401:
        print("🤨 Your token seems to be invalid. Please try again!")
        return

    if response.status_code != 200:
        print(
            "🤯 I couldn't reach the servers. Please try again or contact the admin."
        )
        return

    response_data = response.json()

    user_data = {
        "userHash": code,
        "userName": response_data['user']['userName'],
        "pid": "0",
    }

    click.secho("✅ Congratulations ", nl=False)
    click.echo(
        click.style("{}".format(user_data['userName']), bold=True, fg='yellow'),
        nl=False,
    )
    click.echo("! Registration process is successful.\n")
    click.echo("🥺 Can't wait to hear the checkin and checkout commands.")

    file_data = json.dumps(user_data, indent=4)

    with open(credentials_file_path, "w") as file:
        file.write(file_data)


@click.command('checkin')
def checkin():
    flag = 1
    user_data = read_user_data()

    click.echo()

    click.echo(
        click.style("🌞 Checking you in {}!".format(user_data['userName']), fg='green')
    )

    hours = datetime.datetime.now().time().hour
    minutes = datetime.datetime.now().time().minute

    click.echo()

    click.echo("⏲  The time is ", nl=False)
    click.secho("{}:{}".format(hours, minutes), bold=True)

    click.echo()
    tracker_path = os.path.dirname(os.path.abspath(__file__))+"/track.py"
    click.echo("🧐 Getting some popcorn! 🍿 It's interesting to watch you work!")
    subprocess.call("python3 " + tracker_path+" &", shell=True)
    # subprocess.call("nohup ./ticker.py &", shell=True)
    # subprocess.call("nohup ./ticker.py >/dev/null 2>&1 &", shell=True)


@click.command('checkout')
def checkout():
    status_file_path = os.path.join(root_dir, status_file_name)

    user_data = read_user_data()

    click.echo()

    click.echo(
        click.style(
            "🌞 Checking you out {}!".format(user_data['userName']), fg='bright_black'
        )
    )

    hours = datetime.datetime.now().time().hour
    minutes = datetime.datetime.now().time().minute

    click.echo()

    click.echo("⏲  The time is ", nl=False)
    click.secho("{}:{}".format(hours, minutes), bold=True)

    click.echo()
    subprocess.call("kill -9 "+ str(user_data['pid']),shell=True)
    click.echo("😌 Great work today! Going to sleep! Bye! 🙌")
    

@click.command('away')
def set_away():

    click.echo("Setting away")

    credentials_file_path = os.path.join(root_dir, credentials_file_name)

    with open(credentials_file_path, "rb") as file:
        user_hash = file.readline().decode('UTF-8')[:-1]
        # user_name = file.readline().decode('UTF-8')

        data = {'userHash': user_hash, 'status': 'away'}

        res = requests.post("{}/status/".format(base_url), json.dumps(data))

        print(res.json())


@click.command('available')
def set_available():

    click.echo("Setting available")

    credentials_file_path = os.path.join(root_dir, credentials_file_name)

    with open(credentials_file_path, "rb") as file:
        user_hash = file.readline().decode('UTF-8')[:-1]
        # user_name = file.readline().decode('UTF-8')

        data = {'userHash': user_hash, 'status': 'available'}

        res = requests.post("{}/status/".format(base_url), json.dumps(data))

        print(res.json())


@click.group()
def init_cli():
    user_home_dir = os.path.dirname(os.path.abspath(__file__))

    global root_dir
    root_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
        click.echo("generated {}".format(root_dir))

init_cli.add_command(register_user)
init_cli.add_command(checkin)
init_cli.add_command(checkout)
init_cli.add_command(set_away)
init_cli.add_command(set_available)

if __name__ == '__main__':
    init_cli()

