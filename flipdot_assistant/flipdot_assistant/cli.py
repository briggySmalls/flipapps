import os
import click
import json

import google.oauth2.credentials

from assistant import FlipdotAssistant

DEFAULT_CREDENTIALS_FILE = os.path.join(
    os.path.expanduser('~/.config'),
    'google-oauthlib-tool',
    'credentials.json'
)


@click.command()
@click.option(
    '--credentials',
    default=DEFAULT_CREDENTIALS_FILE,
    help='Path to store and read OAuth2 credentials')
@click.option(
    '--device_model_id', help='The device model ID registered with Google')
@click.option(
    '--project_id',
    help='The project ID used to register device instances.')
@click.version_option()
def main(credentials, device_model_id, project_id):
    with open(credentials, 'r') as credentials_file:
        credentials = google.oauth2.credentials.Credentials(
            token=None, **json.load(credentials_file))

    with FlipdotAssistant(credentials,
                          device_model_id,
                          project_id) as assistant:
        assistant.run()


if __name__ == '__main__':
    main()
