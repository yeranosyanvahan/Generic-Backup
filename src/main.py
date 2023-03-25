import docker

CONTAINER_NAME="srv-mysql2-1"

client = docker.from_env()

container = client.containers.get(CONTAINER_NAME)

output = container.exec_run('echo "hello world"')

print(output.output.decode('utf-8'))
