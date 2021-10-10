# coding:utf-8
# Created by PyCharm.
# Author  : nick（飞虎队工作室）
# Wechat  : cai9503
# Shop    : https://shop.zbj.com/6463852/
# Date    : 2021/10/5
# Time    : 17:42
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhotel.settings')  # 设置django环境

#app = Celery('myhotel',  backend='redis://localhost:6379/1', broker='redis://localhost:6379/1')
app = Celery('myhotel')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY') #  使用CELERY_ 作为前缀，在settings中写配置

# Load task modules from all registered Django apps.
app.autodiscover_tasks()  # 发现任务文件每个app下的task.py

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


