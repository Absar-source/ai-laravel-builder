import os, subprocess, asyncio
from fastapi import WebSocket

async def create_laravel_project(project_name: str, websocket: WebSocket):
    base_path = "./storage/projects"
    os.makedirs(base_path, exist_ok=True)
    project_path = os.path.join(base_path, project_name)

    if os.path.exists(project_path):
        await websocket.send_text(f"Project {project_name} already exists.")
        return project_path

    try:
        # Step 1: Send progress message
        await websocket.send_text("Starting Laravel project creation...")

        # Step 2: Run composer
        process = await asyncio.create_subprocess_exec(
            "composer", "create-project", "laravel/laravel", project_name,
            cwd=base_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Step 3: Stream real-time logs to frontend
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            await websocket.send_text(line.decode().strip())

        await process.wait()
        await websocket.send_text("✅ Laravel project created successfully!")
        return project_path

    except Exception as e:
        await websocket.send_text(f"❌ Error: {str(e)}")
        return None
