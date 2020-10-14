import os
import shutil
import subprocess

import click

from trading_bot.data import get_data_folder_path
from trading_bot.models import get_models_folder_path


here = os.path.abspath(os.path.dirname(__file__))


def move_model(model_name):
    """Move the specified model to the trading_bot/app/data folder
    which is the docker container's volume."""
    models_path = get_models_folder_path()
    app_data_path = 'trading_bot/app/data'
    shutil.copy(f'{models_path}/{model_name}', app_data_path)
    shutil.move(f'{app_data_path}/{model_name}',
                f'{app_data_path}/model')


def download_historical_data():
    """Runs the download.py script in trading_bot/data."""
    download = ['python', 'trading_bot/data/download.py']
    subprocess.run(download)


def move_historical_data():
    """Move the bitcoin.csv file to trading_bot/app/data folder which
    is the docker container's volume."""
    data_path = get_data_folder_path()
    app_data_path = 'trading_bot/app/data'
    shutil.copy(f'{data_path}/bitcoin.csv', app_data_path)


def build_image():
    """Build the docker image."""
    build = ['docker', 'build', '-t', 'trading-bot', '.']
    subprocess.run(build)


def remove_container():
    stop = ['docker', 'container', 'stop', 'trading-bot']
    subprocess.run(stop)
    remove = ['docker', 'container', 'rm', 'trading-bot']
    subprocess.run(remove)


def run_image():
    """Run the docker image."""
    run = ['docker', 'run',
           '-p', '8000:8000',
           '-v', f'{os.getcwd()}/trading_bot/app/data:/data',
           '--name', 'trading-bot',
           'trading-bot']
    subprocess.run(run)


@click.command()
@click.option('--model-name', help='Name of model in the models/ folder',
              required=True, type=str)
@click.option('--rebuild', is_flag=True, default=False,
              help='Add this if you wish to rebuild the container')
def run_app(model_name, rebuild):
    move_model(model_name)
    download_historical_data()
    move_historical_data()
    if rebuild:
        build_image()
    remove_container()
    run_image()


if __name__ == "__main__":
    run_app()
