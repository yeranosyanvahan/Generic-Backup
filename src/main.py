from datetime import datetime
import configparser
import tarfile
import docker
import io
import os
import sys

def COMMANDS(DBTYPE):
    if(DBTYPE == 'postgresql'):
        return ("su postgres -c 'pg_dumpall -U {pguser}'",
        """ This is readme for recovering postgresql """)
    elif(DBTYPE == 'mysql'):
        return (""" mysqldump --all-databases -u{mysql_user} -p"{mysql_password}" """,  
            """ This is readme for recovering mysql """)
    else:
        print("COMMANDS functions accepts only mysql and postgresql ")


if not os.path.isfile('cfg/main.ini'):
    print("cfg/main.ini does not exist, Please configure it before using the script")
    sys.exit()

config = configparser.ConfigParser()
config.read('cfg/main.ini')

for section in config.sections():
    keys = {key:value for key, value in config.items(section)}
    # do some checks to make sure everything is ok
    if("backuptype" not in keys):
        print("BACKUPTYPE is not present in main.ini")
        sys.exit()
    if("dbtype" not in keys):
        print("DBTYPE is not present in main.ini")
        sys.exit()

    if(keys["backuptype"]!= "docker"):
        print("Only docker BACKUPTYPE is supported")
        sys.exit()       

    if(keys["dbtype"] not in ["mysql","postgresql"]):
        print("Only docker mysql and postgresql DBTYPE is supported")
        sys.exit()

    CONTAINER_NAME=section
    #do the backup
    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)

    COMMAND, README = COMMANDS(keys["dbtype"])
    COMMAND = COMMAND.format(**keys)

    # Set the folder and filename for the tar file
    folder = datetime.now().strftime('%Y-%m')
    filename = datetime.now().strftime(f'%Y-%m-%d_{CONTAINER_NAME}.tgz')

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Open the tar file
    with tarfile.open(f'{folder}/{filename}', 'w:gz') as tar:
        # Create a subprocess to run the backup command in the container
        proc = container.exec_run(COMMAND, stdout=True, stderr=True, stream=True)

        # Add the stdout and stderr streams of the subprocess to the tar file
        tar.addfile(tarfile.TarInfo('backup/backup.sql'), proc.stdout)
        tar.addfile(tarfile.TarInfo('backup/backup_stderr.txt'), proc.stderr)

        # Add the Readme.md file to the tar file
        readme_bytes = README.encode('utf-8')
        tarinfo = tarfile.TarInfo('Readme.md')
        tarinfo.size = len(readme_bytes)
        tar.addfile(tarinfo, io.BytesIO(readme_bytes))
