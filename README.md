# hcloud-tg

<p align="center">
	<img alt="License" src="https://img.shields.io/github/license/Navid2zp/hcloud-tg?style=flat-square" />
	<img alt="Docker size" src="https://img.shields.io/docker/image-size/navid2zp/hcloud-tg?style=flat-square" />
	<img alt="Docker build" src="https://img.shields.io/docker/cloud/build/navid2zp/hcloud-tg?style=flat-square" />
	<img alt="Docker build" src="https://img.shields.io/docker/cloud/automated/navid2zp/hcloud-tg?style=flat-square" />
	<img alt="Docker pulls" src="https://img.shields.io/docker/pulls/navid2zp/hcloud-tg?style=flat-square" />
</p>

Telegram bot for managing Hetzner cloud servers.

<p align="center">
	<img alt="dups" src="https://raw.githubusercontent.com/Navid2zp/hcloud-tg/main/Screenshot.png" />
</p>


## Running

hcloud-tg requires some environment variables to work.

`BOT_TOKEN`: 
Your bot token which you got from @BotFather.

`ALLOWED_USERS`: 
A list of users telegram id that are allowed to use the bot. IDs should be separated using '-' (12345678-3215477). You can either get your id by messaging `@get_id_bot` bot or you can run the bot without any allowed users and send `/me` command to get a reply containing your telegram id.

`HETZNER_API_KEY`:
An API key generated from Hetzner cloud console. Note that only servers that are in the API project will be available to manage.

### Docker:

**Using `docker run`:**

```
docker run -e BOT_TOKEN=<BOT_TOKEN> -e ALLOWED_USERS=<ALLOWED_USERS> -e HETZNER_API_KEY=<HETZNER_CLOUD_API> navid2zp/hcloud-tg
```

**Using `docker-compose`:**

create a `docker-compose.yml` file:

```
version: "3.9"

services:
  hcloud-tg:
    container_name: hcloud-tgbot
    image: navid2zp/hcloud-tg
    env_file: ./env.list
    restart: always
```

create a file containing environment variables named `env.list` next to `docker-compose.yml`:

```
BOT_TOKEN=<YOUR_BOT_TOKEN>
ALLOWED_USERS=<ALLOWED_USERS>
HETZNER_API_KEY=<YOUR_HETZNER_API_KEY>
```
and then run: `docker-compose up`

### Python:

Add the required environment variables and then:

```
git clone https://github.com/Navid2zp/hcloud-tg.git
cd hcloud-tg
pip install -r requirements.txt
python bot.py
```

## Supported actions:

- reset
- reboot
- shutdown
- power on
- power off
- root password reset

### Docker hub:

https://hub.docker.com/r/navid2zp/hcloud-tg


License
----
MIT
