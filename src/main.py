import docker
import tarfile

CONTAINER_NAME="srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"')

print(output.output.decode('utf-8'))

# Open the tar file for writing
with tarfile.open('/output.gz', 'w:gz') as output_tar:

    # Add the output of the function to a file in the archive
    output = 'The output of the function goes here.'
    output_bytes = output.encode('utf-8')
    output_file = tarfile.TarInfo('output.txt')
    output_file.size = len(output_bytes)
    output_tar.addfile(output_file, fileobj=io.BytesIO(output_bytes))

    # Add a new file to the archive
    readme_bytes = b'hello world'
    readme_file = tarfile.TarInfo('Readme.md')
    readme_file.size = len(readme_bytes)
    output_tar.addfile(readme_file, fileobj=io.BytesIO(readme_bytes))
