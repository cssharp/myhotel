酒店管理系统
=========
1. 创建项目
```
django-admin startproject myhotel
```
2. 创建酒店
```
python manage.py startapp hotels
```
3. 运行项目
```
python manage.py runserver 0:8000
```

4. 创建管理员
```
python manage.py makemigrations 
python manage.py migrate 
python manage.py createsuperuser 
```

5. 启动celery
```
celery -A myhotel.celery worker -l info -P eventlet --pool=solo
```

