# -*- coding: UTF-8 -*-
import argparse
import logging
import os
import sys
import requests

import django
from django.core import management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'apps')

os.chdir(BASE_DIR)
sys.path.insert(0, APP_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartdoc.settings")
django.setup()


def collect_static():
    """
     收集静态文件到指定目录
     本项目主要是将前端vue/dist的前端项目放到静态目录下面
    :return:
    """
    logging.info("Collect static files")
    try:
        management.call_command('collectstatic', '--no-input', '-c', verbosity=0, interactive=False)
        logging.info("Collect static files done")
    except:
        pass


def perform_db_migrate():
    """
    初始化数据库表
    """
    logging.info("Check database structure change ...")
    logging.info("Migrate model change to database ...")
    try:
        management.call_command('migrate')
    except Exception as e:
        logging.error('Perform migrate failed, exit', exc_info=True)
        sys.exit(11)


def start_services():
    management.call_command('migrate')
    management.call_command('runserver', "0.0.0.0:8088")


def get_latest_tag(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，会引发HTTPError异常
        return response.json()['tag_name']
    except requests.RequestException as e:
        print(f"Failed to fetch the latest tag: {e}")
        return None


if __name__ == '__main__':
    os.environ['HF_HOME'] = '/opt/kb_builder/model/base'
    latest_tag = get_latest_tag('hduchat', 'KB-Builder')
    if latest_tag:
        print(f"************** KB Builder version: {latest_tag} **************")
        os.environ['KB_BUILDER_VERSION'] = latest_tag
    
    parser = argparse.ArgumentParser(
        description="""
           qabot service control tools;

           Example: \r\n

           %(prog)s start all -d;
           """
    )
    parser.add_argument(
        'action', type=str,
        choices=("start", "upgrade_db", "collect_static"),
        help="Action to run"
    )
    args = parser.parse_args()

    action = args.action
    if action == "upgrade_db":
        perform_db_migrate()
    elif action == "collect_static":
        collect_static()
    else:
        collect_static()
        start_services()
