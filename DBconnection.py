DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '', #your_database_name
        'USER': 'postgres', #your_database_user
        'PASSWORD': '', #your_database_password
        'HOST': 'localhost',  # Replace with your PostgreSQL server's address if necessary
        'PORT': '5432',          # Leave empty to use the default PostgreSQL port (usually 5432)
    }
}