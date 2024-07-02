import os, sys, django
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from utils.encrypt import md5
from web import models

models.Administrator.objects.create(username='admin',password=md5('admin123'),mobile='18888888856')
from django.conf import settings