from datetime import datetime
import configparser
import tarfile
import docker
import io
import os

config = configparser.ConfigParser()
config.read('/cfg/main.ini')

for section in config.sections():
    config = {key:value for key, value in config.items(section)}
    print(section,config)

CONTAINER_NAME = "srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

# Set the folder and filename for the tar file
folder = datetime.now().strftime('%Y-%m')
filename = datetime.now().strftime(f'%Y-%m-%d_{CONTAINER_NAME}.tgz')

# Create the folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

# Open the tar file
with tarfile.open(f'{folder}/{filename}', 'w:gz') as tar:
    # Add the output of the function to backup/backup.sql in the tar file
    output = "This is the output of my function"
    output_bytes = output.encode('utf-8')
    tarinfo = tarfile.TarInfo('backup/backup.sql')
    tarinfo.size = len(output_bytes)
    tar.addfile(tarinfo, io.BytesIO(output_bytes))

    # Add the Readme.md file to the tar file
    readme_text = "hello world\n"
    readme_bytes = readme_text.encode('utf-8')
    tarinfo = tarfile.TarInfo('Readme.md')
    tarinfo.size = len(readme_bytes)
    tar.addfile(tarinfo, io.BytesIO(readme_bytes))
