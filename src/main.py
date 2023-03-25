import docker
import tarfile
import gzip
import io

CONTAINER_NAME="srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

# function that generates output
def generate_output():
    return "This is the output of my function"

# open the existing tar file for writing
with tarfile.open('output.tar', 'w:gz') as tf:
    
    # create a TarInfo object for the output file
    info = tarfile.TarInfo('output.gz')
    output_bytes = output.encode('utf-8')
    info.size = len(output_bytes)
    
    # create a GzipFile object for writing compressed data
    with gzip.open('output.gz', 'wb') as gz:
        
        # write the output to the GzipFile
        gz.write(output_bytes)
        
        # add the output file to the tar file
        tf.addfile(info, gz)
        
    # create a TarInfo object for the Readme file
    readme_info = tarfile.TarInfo('Readme.md')
    readme_bytes = b'hello world'
    readme_info.size = len(readme_bytes)
    
    # create a file-like object with the contents of the Readme file
    readme_obj = io.BytesIO(readme_bytes)
    
    # add the Readme file to the tar file
    tf.addfile(readme_info, readme_obj)
