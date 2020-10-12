import os
import shutil
import subprocess

import click

from trading_bot.data import get_data_folder_path
from trading_bot.models import get_models_folder_path


here = os.path.abspath(os.path.dirname(__file__))


def move_model(model_name):
    cwd = os.getcwd()
    models_path = get_models_folder_path()
    shutil.copy(f'{models_path}/{model_name}', cwd)
    shutil.move(f'{cwd}/{model_name}', f'{cwd}/model.keras')


def download_historical_data():
    download = ['python', 'trading_bot/data/download.py']
    subprocess.run(download)


def move_historical_data():
    cwd = os.getcwd()
    data_path = get_data_folder_path()
    shutil.move(f'{data_path}/bitcoin.csv', cwd)


def build_image():
    build = ['docker', 'build', '-t', 'trading-bot', '.']
    subprocess.run(build)


def run_image():
    run = ['docker', 'run', '-p', '8000:8000', 'trading-bot']
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
    run_image()


if __name__ == "__main__":
    run_app()
