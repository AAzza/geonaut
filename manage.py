import datetime

from jinja2 import Environment, FileSystemLoader
from flask.ext.script import Manager

from server import create_app


manager = Manager(create_app)


@manager.command
def generate_manifest(out_path=None):
    """ Generate manifest.appcache from the templates/manifest.appcache.jinja"""
    now = datetime.datetime.now()
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('manifest.appcache.jinja')
    manifest = template.render(date=now)
    if out_path:
        with open(out_path, 'w') as out:
            out.write(manifest)
    else:
        print manifest


if __name__ == "__main__":
    manager.run()
