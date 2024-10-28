# Smart

A smart and simple trading bot.

## Table of contents

- [Smart](#smart)
  - [Table of contents](#table-of-contents)
  - [Getting started](#getting-started)
    - [Download](#download)
    - [Install dependencies](#install-dependencies)
    - [Setup the environment variables](#setup-the-environment-variables)
    - [Start a single job](#start-a-single-job)
    - [Start a bot](#start-a-bot)
      - [Example](#example)
  - [Authors](#authors)
  - [License](#license)

## Getting started

### Download

To download this project, please do: `git clone https://github.com/tun43p/smart.git`.

### Install dependencies

To install the dependencies, please do: `pip3 install -r requirements.txt`.

### Setup the environment variables

To setup the environment variables, please do: `cp .env.example env/local.env`.

Then, please fill the `local.env` file with the correct values.

### Start a single job

To start a single job, please do: `python3 main.py`.

**Don't forget to set the environment variables**.

### Start a bot

To start a bot, please do: `BOT_NAME="YOUR_BOT_NAME" python3 -m bot.bot_file bot/bot_file.py`.

**Don't forget to set the environment variables for your bot**.

#### Example

```bash
cp .env.example env/smart.env
BOT_NAME="smart" python3 -m bot.telegram_bot bot/telegram_bot.py
```

## Authors

- **tun43p** - _Initial work_ - [tun43p](https://github.com/tun43p).

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.
