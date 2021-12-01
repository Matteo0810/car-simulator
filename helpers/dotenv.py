import os, re


def dotenv():
    content = open('.env', 'r').readlines()
    for line in content:
        key, value = line.split('=')
        os.environ[key.upper()] = value


def get_env(key: str):
    value = os.getenv(key)
    if value is not None:
        if type(eval(value)) is not str:
            return eval(value)
        value = re.sub(r'^"|"$', '', value)
        return value.strip()
    raise ValueError('Clé introuvable dans le fichier .env')
