import os
from docker import DockerClient
import dotenv
from telethon import events, TelegramClient
from web3 import Web3

from helpers import env


dotenv.load_dotenv(dotenv_path=".env")

is_env_variables_set = env.check_env_variables()

if not is_env_variables_set:
    raise Exception("Failed to set environment variables")

telegram = TelegramClient(
    "limencello",
    env.get_telegram_api_id(),
    env.get_telegram_api_hash(),
)

# TODO: Pass to env variables
docker_client = DockerClient(base_url="unix:///Users/tun43p/.docker/run/docker.sock")


async def log_info(event: events.NewMessage.Event, message: str):
    print(message)
    await telegram.send_message(
        entity=event.message.chat_id,
        message=message,
    )


async def start_process(event: events.NewMessage.Event):
    token = f"0x{event.message.message.split('0x')[1]}"

    try:
        if not Web3.is_address(token):
            await log_info(event, "Invalid token address!")

        containers = docker_client.containers.list(all=True)

        if any(token in container.name for container in containers):
            await log_info(event, f"Already trading this token {token}.")
            return

        tag = "tun43p/limoncello"

        if len(docker_client.images.list(name=tag)) == 0:
            await log_info(event, f"Building image {tag}...")

            docker_client.images.build(
                path=".",
                tag=tag,
                nocache=True,
                rm=True,
            )

        environment = os.environ.copy()
        environment["TOKEN_ADDRESS"] = token

        await log_info(event, f"Starting container {token}...")

        container = docker_client.containers.run(
            tag,
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


async def stop_process(event: events.NewMessage.Event):
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


async def get_status(event: events.NewMessage.Event):
    containers = docker_client.containers.list(all=True)

    if not containers:
        await log_info(event, "No containers are running!")
        return

    for container in containers:
        await log_info(event, f"Container {container.name} is running!")


async def handler(event: events.NewMessage.Event):
    message = event.message.message

    try:
        if message.startswith("/trade") and "0x" in message:
            await start_process(event)
        elif message.startswith("/stop") and "0x" in message:
            await stop_process(event)
        elif message.startswith("/status"):
            await get_status(event)
    except Exception as error:
        await log_info(event, f"Failed to process command: {error}")


async def limoncello():
    await telegram.start()

    if not telegram.is_connected():
        raise ConnectionError(
            "Failed to connect to Telegram with API_ID={}".format(
                env.get_telegram_api_id()
            )
        )

    print("Limoncello started!")

    # TODO: Listen only for SMART ETH SIGNALS
    telegram.add_event_handler(handler, events.NewMessage())

    await telegram.run_until_disconnected()


telegram.loop.run_until_complete(limoncello())
