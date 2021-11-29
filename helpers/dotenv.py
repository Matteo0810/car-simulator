import os


def dotenv():
    content = open('.env', 'r').readlines()
    for line in content:
        key, value = line.split('=')
        os.environ[key.upper()] = value


def get_env(key: str):
    value = os.getenv(key)
    if type(eval(value)) is not str:
        return eval(value)
    return value
