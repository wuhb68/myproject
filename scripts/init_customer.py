import os, sys, django

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from utils.encrypt import md5
from web import models

# level_object = models.Level.objects.create(
#     title='VIP',
#     percent='80'
# )
models.Customer.objects.create(
    username='wuhb1',
    password=md5('wuhb1'),
    mobile='18888888889',
    level_id=1,
    creator_id=1,
)
