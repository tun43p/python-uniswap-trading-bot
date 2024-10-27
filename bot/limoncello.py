import logging
import os
import colorama
from docker import DockerClient
import dotenv
from telethon import events, TelegramClient
from web3 import Web3
import websockets

from helpers import environment

# This is a global variable, which is not a good practice, but it is used for
# simplicity. It is used to store the connected clients to the WebSocket server.
# The key is the token address and the value is the WebSocket client.
connected_clients = {}

if os.path.exists(".env"):
    dotenv.load_dotenv(dotenv_path=".env")

BOT_NAME = "limoncello"

os.environ["TOKEN_ADDRESS"] = ""
os.environ["WEBSOCKET_URL"] = "ws://0.0.0.0:8765"

telegram_client = TelegramClient(
    BOT_NAME,
    environment.get_telegram_api_id(),
    environment.get_telegram_api_hash(),
)

docker_image_tag = f"tun43p/{BOT_NAME}"
docker_client = DockerClient(
    base_url=environment.get_docker_context(),
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

        docker_environment = os.environ.copy()
        docker_environment["TOKEN_ADDRESS"] = token
        docker_environment["WEBSOCKET_URI"] = "ws://host.docker.internal:8765"

        await log_info(event, f"Starting container {token}...")

        container = docker_client.containers.run(
            docker_image_tag,
            name=token,
            environment=docker_environment,
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
                await log_info(event, f"Deleting container {token}...")

                container.stop()
                container.remove()

                await log_info(event, f"Trading with token {token} deleted!")

    except Exception as error:
        await log_info(event, f"Failed to stop trading with token {token}: {error}")


async def _stop_all_command(event: events.NewMessage.Event):
    containers = docker_client.containers.list(all=True)

    if not any("0x" in container.name for container in containers):
        await log_info(event, "No containers are running!")
        return

    for container in containers:
        if "0x" in container.name:
            await log_info(event, f"Deleting container {container.name}...")

            container.stop()
            container.remove()

            await log_info(event, f"Container {container.name} is deleted!")


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
        elif message.startswith("/stop-all"):
            await _stop_all_command(event)
        elif message.startswith("/status"):
            await _status_command(event)

    except Exception as error:
        await log_info(event, f"Failed to process command: {error}")


async def _handle_websocket_connection(
    websocket: websockets.WebSocketServerProtocol,
    path: str,
):
    global connected_clients
    connected_clients[path] = websocket

    try:
        async for message in websocket:
            data = message.split("::")
            _, token, level, message = data

            log_message = f"{token} {message}"

            if level == "ERROR" or level == "CRITICAL" or level == "FATAL":
                log_message = (
                    f"{colorama.Fore.RED}{log_message}{colorama.Style.RESET_ALL}"
                )
            elif level == "WARNING":
                log_message = (
                    f"{colorama.Fore.YELLOW}{log_message}{colorama.Style.RESET_ALL}"
                )
            elif level == "DEBUG":
                log_message = (
                    f"{colorama.Fore.BLUE}{log_message}{colorama.Style.RESET_ALL}"
                )

            print(log_message)

            await websocket.send(log_message)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    except Exception as error:
        print(f"Error in WebSocket connection: {error}")
    finally:
        connected_clients.pop(path, None)


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

        # TODO: Listen only for SMART ETH SIGNALS
        telegram_client.add_event_handler(
            _new_message_handler,
            events.NewMessage(),
        )

        websocket_logger = logging.getLogger("websockets")
        websocket_logger.disabled = True

        websocket_server = websockets.serve(
            _handle_websocket_connection, "0.0.0.0", 8765, logger=websocket_logger
        )

        async with websocket_server:
            print("Limoncello started!")
            await telegram_client.run_until_disconnected()
    except Exception as error:
        print(f"Failed to start Limoncello: {error}")


telegram_client.loop.run_until_complete(_limoncello())
