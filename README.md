# Python Challenge

This is the answer to the Python Challenge built upon a simple chat room built using Django Channels ([original repo](https://github.com/ploggingdev/djangochat)).

It consists of a chatroom where commands can be written. A `command` is any message that starts with a `/`.

## Setup instructions:

Database setup :

```
sudo -u postgres psql

CREATE DATABASE djangochat;

CREATE USER djangochatuser WITH PASSWORD 'YOUR_PASSWORD';

ALTER ROLE djangochatuser SET client_encoding TO 'utf8';

ALTER ROLE djangochatuser SET default_transaction_isolation TO 'read committed';

ALTER ROLE djangochatuser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE djangochat TO djangochatuser;

\q
```

Setup Django project :

```
git clone https://github.com/ploggingdev/djangochat.git

sudo apt install python3-venv

cd djangochat

mkdir venv

python3 -m venv venv/djangochat

source venv/djangochat/bin/activate

pip install -r requirements.txt

pip install --upgrade pip
```

Add environment variables :

```
sudo vim ~/.bashrc
# or ~/.zshrc

#append the following to the end of the file

export djangochat_secret_key="SECRET_KEY"

export djangochat_db_name="djangochat"

export djangochat_db_user="djangochatuser"

export djangochat_db_password="YOUR_PASSWORD"

export djangochat_postmark_token="POSTMARK_TOKEN"

export DJANGO_SETTINGS_MODULE=djangochat.settings
```

Source the env variables :

```
deactivate

source ~/.bashrc

source venv/djangochat/bin/activate
```

Perform database migration : 

```
python manage.py migrate
```

Install redis by following this [guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04).

Create Django superuser :

```
python manage.py createsuperuser
```

Start the development server :

```
python manage.py runserver --noreload
```
The `noreload` flag is used to avoid duplicated instances of the singletons due to Django running twice.

Start celery :

```
celery -A chatdemo worker -B -l info
```

Visit the local development server at `127.0.0.1:8000` to test the site.
