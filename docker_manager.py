import docker
import os

client = docker.from_env()

def create_laravel_container(project_path, container_name="laravel_app"):
    """Create and run Laravel app in Docker."""
    abs_path = os.path.abspath(project_path)
    
    print(f"Starting Docker container for {abs_path}...")

    container = client.containers.run(
        image="bitnami/laravel:latest",
        name=container_name,
        volumes={abs_path: {'bind': '/app', 'mode': 'rw'}},
        ports={'8000/tcp': 8000},
        detach=True
    )

    print(f"Container {container_name} is running at http://localhost:8000")
    return container
