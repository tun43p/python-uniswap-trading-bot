import os
from docker import DockerClient
import dotenv
from telethon import events, TelegramClient
from web3 import Web3

from helpers import environment


dotenv.load_dotenv(dotenv_path=".env")

is_env_variables_set = environment.check_env_variables()

if not is_env_variables_set:
    raise Exception("Failed to set environment variables")

telegram_client = TelegramClient(
    "limencello",
    environment.get_telegram_api_id(),
    environment.get_telegram_api_hash(),
)

docker_image_tag = "tun43p/limoncello"
docker_client_url = os.environ.get("DOCKER_CLIENT")
docker_client = DockerClient(
    base_url=docker_client_url if docker_client_url else "unix://var/run/docker.sock"
)


async def log_info(event: events.NewMessage.Event, message: str):
    print(message)
    await telegram_client.send_message(
        entity=event.message.chat_id,
        message=message,
    )


async def _start_command(event: events.NewMessage.Event):
    token = f"0x{event.message.message.split('0x')[1]}"

    try:
        if not Web3.is_address(token):
            await log_info(event, "Invalid token address!")

        containers = docker_client.containers.list(all=True)

        if any(token in container.name for container in containers):
            await log_info(event, f"Already trading this token {token}.")
            return

        environment = os.environ.copy()
        environment["TOKEN_ADDRESS"] = token

        await log_info(event, f"Starting container {token}...")

        container = docker_client.containers.run(
            docker_image_tag,
            name=token,
            environment=environment,
            detach=True,
            stdout=True,
            stderr=True,
        )

        if not container:
            raise Exception(f"Failed to start container {token}")

        await log_info(event, f"Container {token} started!")
    except Exception as error:
        log_info(event, f"Failed to start trading with token {token}: {error}")


async def _stop_command(event: events.NewMessage.Event):
    token = f"0x{event.message.message.split('0x')[1]}"

    try:
        if not Web3.is_address(token):
            log_info(event, "Invalid token address!")
            return

        containers = docker_client.containers.list(all=True)

        if not any(token in container.name for container in containers):
            await log_info(event, f"Trading with token {token} is not running.")

        for container in containers:
            if token in container.name:
                await log_info(event, f"Stopping container {token}...")
                container.stop()

                await log_info(event, f"Removing container {token}...")
                container.remove()

        await log_info(event, f"Trading with token {token} deleted!")

    except Exception as error:
        await log_info(event, f"Failed to stop trading with token {token}: {error}")


async def _status_command(event: events.NewMessage.Event):
    containers = docker_client.containers.list(all=True)

    if not containers:
        await log_info(event, "No containers are running!")
        return

    for container in containers:
        await log_info(event, f"Container {container.name} is running!")


async def _new_message_handler(event: events.NewMessage.Event):
    message = event.message.message

    try:
        if message.startswith("/trade") and "0x" in message:
            await _start_command(event)
        elif message.startswith("/stop") and "0x" in message:
            await _stop_command(event)
        elif message.startswith("/status"):
            await _status_command(event)
    except Exception as error:
        await log_info(event, f"Failed to process command: {error}")


async def _limoncello():
    try:
        await telegram_client.start()

        if not telegram_client.is_connected():
            raise ConnectionError(
                "Failed to connect to Telegram with API_ID={}".format(
                    environment.get_telegram_api_id()
                )
            )

        if len(docker_client.images.list(name=docker_image_tag)) > 0:
            print("Removing existing Docker containers...")

            for container in docker_client.containers.list(all=True):
                if docker_image_tag not in container.image.tags:
                    container.stop()
                    container.remove()

                    print(f"Container {container.name} removed!")

            print("Removing existing Docker image...")

            for image in docker_client.images.list(name=docker_image_tag):
                docker_client.images.remove(image.id, force=True)

                print(f"Image {image.id} removed!")

        print("Building Docker image...")

        docker_client.images.build(
            path=".",
            tag=docker_image_tag,
            nocache=True,
            rm=True,
        )

        print("Docker image built!")
        print("Limoncello started!")

        # TODO: Listen only for SMART ETH SIGNALS
        telegram_client.add_event_handler(
            _new_message_handler,
            events.NewMessage(),
        )

        await telegram_client.run_until_disconnected()
    except Exception as error:
        print(f"Failed to start Limoncello: {error}")


telegram_client.loop.run_until_complete(_limoncello())
