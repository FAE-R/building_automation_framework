# Importing the AppConfig class from django.apps module.
from django.apps import AppConfig


# Defining a configuration class for the 'agents' application.
class AutomatedLabConfig(AppConfig):
    
    # Setting the default primary key field type for models in this application.
    # 
    # In Django models, each model typically has a primary key field that uniquely identifies each record in the database.
    # By default, Django uses an 'AutoField' for primary keys, which is an integer field that automatically increments with each new record.
    #
    # 'BigAutoField' is a type of 'AutoField' that uses a 64-bit integer instead of a 32-bit integer.
    # This means it can store much larger numbers, making it suitable for applications that expect to handle a large number of records.
    #
    # Setting 'default_auto_field' to 'django.db.models.BigAutoField' ensures that all primary key fields in this app will use 'BigAutoField'
    # unless explicitly overridden in a model definition.
    default_auto_field = 'django.db.models.BigAutoField'

    
    # Naming the application. This should match the name of the app directory.
    name = 'agents'
