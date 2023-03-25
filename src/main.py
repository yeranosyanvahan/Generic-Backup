import docker
import tarfile
import gzip

CONTAINER_NAME = "srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"').output.decode('utf-8')

# function that generates output
def generate_output():
    return "This is the output of my function"

# open the existing tar file for writing
with tarfile.open('output.tar', 'w:gz') as tf:
    
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
    with tf.fileobj as tar_file:
        with gzip.open('Readme.md.gz', 'wb') as gz:
            gz.write('hello world'.encode('utf-8'))
            gz.seek(0)
            tar_file.write(readme_info.tobuf())
            tar_file.write(gz.read())
