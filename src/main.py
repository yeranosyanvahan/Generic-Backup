import docker
import tarfile

CONTAINER_NAME="srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

import tarfile
import gzip

# function that generates output
def generate_output():
    return "This is the output of my function"

# open the existing tar file for writing
with tarfile.open('output.tar', 'a') as tf:
    
    # create a GzipFile object for writing compressed data
    with gzip.open('output.gz', 'wb') as gz:
        
        # write the output to the GzipFile
        gz.write(output.encode('utf-8'))
        
        # create a TarInfo object for the output file
        info = tarfile.TarInfo('output.gz')
        info.size = len(output)
        
        # add the output file to the tar file
        tf.addfile(info, gz)
        
    # create a TarInfo object for the Readme file
    readme_info = tarfile.TarInfo('Readme.md')
    readme_info.size = len('hello world')
    
    # add the Readme file to the tar file
    with tf.extractfile(readme_info) as f:
        f.write('hello world'.encode('utf-8'))
        tf.addfile(readme_info, f)
