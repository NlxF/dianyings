#About

The reason it exists is that I am looking for work

#Deployment

__Django has a great document that tells how to deploy a project in production [HERE](https://docs.djangoproject.com/en/1.6/howto/deployment/)__

If you just want to have a preview or a develop environment you can follow the steps below

It's recommended that you deploy this project with  virtualenv.

_It took for granted that you have pip installed and cloned or downloaded the source files from github_

1. install virtualenv: `pip install virtualenv`

2. setup a virtualenv: `virtualenv dianying`

3. activate the virtualenv: `source ./dianying/bin/activate`

5. `cd` into the folder that contains dianying project

4. install the requirements: `pip install -r requirements.txt`

6. now you have to configure the database and some other settings in `deploy_settings.py` and `settings.py` in the folder `dianying` to fit you needs (__Don't forget the secret_key!__)

7. you can then run `python manage.py syncdb` to set up your database and add a superuser

8. run `python manage.py runserver 0.0.0.0:8000`, then you can access to your site via `http://ip:8000`

9. head to `http://ip:8000/admin/`, sign in as superuser and other users
