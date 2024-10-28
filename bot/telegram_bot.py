import logging
import os
import colorama
from docker import DockerClient
import dotenv
from telethon import events, TelegramClient
from web3 import Web3
import websockets

# This is a global variable, which is not a good practice, but it is used for
# simplicity. It is used to store the connected clients to the WebSocket server.
# The key is the token address and the value is the WebSocket client.
connected_clients = {}

BOT_NAME = os.environ.get("BOT_NAME") if os.environ.get("BOT_NAME") else "smart"

if os.path.exists(f"env/{BOT_NAME}.env"):
    dotenv.load_dotenv(dotenv_path=f"env/{BOT_NAME}.env")
else:
    raise ValueError(f"env/{BOT_NAME}.env is not found")

docker_context = os.environ.get("DOCKER_CONTEXT")
if not docker_context:
    raise ValueError("DOCKER_CONTEXT is not set")

telegram_api_id = os.environ.get("TELEGRAM_API_ID")
if not telegram_api_id:
    raise ValueError("TELEGRAM_API_ID is not set")

telegram_api_hash = os.environ.get("TELEGRAM_API_HASH")
if not telegram_api_hash:
    raise ValueError("TELEGRAM_API_HASH is not set")

telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not telegram_bot_token:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

telegram_channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
if not telegram_channel_id:
    raise ValueError("TELEGRAM_CHANNEL_ID is not set")

if os.environ.get("TOKEN_ADDRESS"):
    del os.environ["TOKEN_ADDRESS"]

if not os.environ.get("WEBSOCKET_URI"):
    os.environ["WEBSOCKET_URI"] = "ws://0.0.0.0:8765"

docker_image_tag = f"tun43p/{BOT_NAME}"

docker_client = DockerClient(base_url=docker_context)
telegram_client = TelegramClient(BOT_NAME, telegram_api_id, telegram_api_hash)


async def _log(
    event: events.NewMessage.Event, message: str, without_print: bool = False
):
    if not without_print:
        print(message)

    await telegram_client.send_message(
        entity=event.message.chat_id,
        message=message,
    )


async def _start_command(event: events.NewMessage.Event):
    token = f"0x{event.message.message.split('0x')[1]}"

    try:
        if not Web3.is_address(token):
            await _log(event, "Invalid token address!")

        containers = docker_client.containers.list(all=True)

        if any(token in container.name for container in containers):
            await _log(event, f"Already trading this token {token}.")
            return

        envron = os.environ.copy()
        envron["TOKEN_ADDRESS"] = token
        envron["WEBSOCKET_URI"] = "ws://host.docker.internal:8765"

        await _log(event, f"Starting container {token}...")

        container = docker_client.containers.run(
            docker_image_tag,
            name=token,
            environment=envron,
            detach=True,
            stdout=True,
            stderr=True,
        )

        if not container:
            raise Exception(f"Failed to start container {token}")

        await _log(event, f"Container {token} started!")
    except Exception as error:
        _log(event, f"Failed to start trading with token {token}: {error}")


async def _stop_command(event: events.NewMessage.Event):
    token = f"0x{event.message.message.split('0x')[1]}"

    try:
        if not Web3.is_address(token):
            _log(event, "Invalid token address!")
            return

        containers = docker_client.containers.list(all=True)

        if not any(token in container.name for container in containers):
            await _log(event, f"Trading with token {token} is not running.")

        for container in containers:
            if token in container.name:
                await _log(event, f"Deleting container {token}...")

                container.stop()
                container.remove()

                await _log(event, f"Trading with token {token} deleted!")

    except Exception as error:
        await _log(event, f"Failed to stop trading with token {token}: {error}")


async def _stop_all_command(event: events.NewMessage.Event):
    containers = docker_client.containers.list(all=True)

    if not any("0x" in container.name for container in containers):
        await _log(event, "No containers are running!")
        return

    for container in containers:
        if "0x" in container.name:
            await _log(event, f"Deleting container {container.name}...")

            container.stop()
            container.remove()

            await _log(event, f"Container {container.name} is deleted!")


async def _status_command(event: events.NewMessage.Event):
    containers = docker_client.containers.list(all=True)

    if not containers:
        await _log(event, "No containers are running!")
        return

    for container in containers:
        await _log(event, f"Container {container.name} is running!")


async def _new_message_handler(event: events.NewMessage.Event):
    message = event.message.message

    try:
        if message.startswith("/trade") and "0x" in message:
            await _start_command(event)
        elif message.startswith("/stop") and "0x" in message:
            await _stop_command(event)
        elif message.startswith("/stop_all"):
            await _stop_all_command(event)
        elif message.startswith("/status"):
            await _status_command(event)
        elif message.startswith("/help"):
            await _log(
                event,
                "/trade 0x...: Start trading with the token\n"
                "/stop 0x...: Stop trading with the token\n"
                "/stop_all: Stop trading with all tokens\n"
                "/status: Get the status of the trading\n",
                without_print=True,
            )

    except Exception as error:
        await _log(event, f"Failed to process command: {error}")


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

            # TODO: Check if the message send works
            if "[BUY]" in log_message or "[SELL]" in log_message:
                try:
                    _log(
                        events.NewMessage.Event(
                            message_id=0,
                            chat_id=telegram_channel_id,
                            message=log_message,
                        ),
                        log_message,
                        without_print=True,
                    )
                except Exception as error:
                    print(f"Failed to send message to Telegram: {error}")

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


async def _main():
    try:
        await telegram_client.start(bot_token=telegram_bot_token)

        if not telegram_client.is_connected():
            raise ConnectionError(
                "Failed to connect to Telegram with API_ID={}".format(telegram_api_id)
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

        telegram_client.add_event_handler(
            _new_message_handler,
            events.NewMessage(),
        )

        websocket_logger = logging.getLogger("websockets")
        websocket_logger.disabled = True

        websocket_uri_informations = (
            os.environ.get("WEBSOCKET_URI").split("://")[1].split(":")
        )

        websocket_server = websockets.serve(
            _handle_websocket_connection,
            websocket_uri_informations[0],
            websocket_uri_informations[1],
            logger=websocket_logger,
        )

        async with websocket_server:
            print(f"Bot {BOT_NAME} started!")
            await telegram_client.run_until_disconnected()
    except Exception as error:
        print(f"Failed to start {BOT_NAME} bot: {error}")


telegram_client.loop.run_until_complete(_main())
