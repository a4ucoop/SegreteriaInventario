from default_settings import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
    	   # 'ENGINE': 'django.db.backends.sqlite3',
    	   # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'SegreteriaInventario',
        'USER': 'SegInve',
        'PASSWORD': 'SegreteriaInventarioPass',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },
    'cineca': {
        'ENGINE': 'django.db.backends.oracle',
        #'NAME': 'UGOV_HOSTING_CINECA_PROD',
        'NAME': 'cman01-ext.dbc.cineca.it:5555/UGOV_UNICAM_PROD_ext.cineca.it',
        'USER': 'SIAIE_UNICAM_PROD',
        'PASSWORD': 'ldle2!d3',
        'HOST': '',
        'PORT': '',
    }
}

