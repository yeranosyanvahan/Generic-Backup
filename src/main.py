import docker
import tarfile
import io

CONTAINER_NAME = "srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

# Open the tar file
with tarfile.open('output.tgz', 'w:gz') as tar:
    # Add the output of the function to output.txt in the tar file
    output = "This is the output of my function"
    output_bytes = output.encode('utf-8')
    tarinfo = tarfile.TarInfo('backup/output.txt')
    tarinfo.size = len(output_bytes)
    tar.addfile(tarinfo, io.BytesIO(output_bytes))

    # Add the Readme.md file to the tar file
    readme_text = "hello world\n"
    readme_bytes = readme_text.encode('utf-8')
    tarinfo = tarfile.TarInfo('Readme.md')
    tarinfo.size = len(readme_bytes)
    tar.addfile(tarinfo, io.BytesIO(readme_bytes))
