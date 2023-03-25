import docker
import tarfile

CONTAINER_NAME = "srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

# Open the tar file
with tarfile.open('output.tgz', 'w:gz') as tar:
    # Add the output of the function to output.txt in the tar file
    output = "This is the output of my function"
    with tarfile.TarInfo('output.txt') as tarinfo:
        tarinfo.size = len(output)
        tar.addfile(tarinfo, fileobj=io.StringIO(output))

    # Add the Readme.md file to the tar file
    with tarfile.TarInfo('Readme.md') as tarinfo:
        tarinfo.size = len('hello world\n')
        tar.addfile(tarinfo, fileobj=io.StringIO('hello world\n'))
