# Keepalive Service

A tool to monitor servers and keep 'em alive by periodically pinging them. This tool is useful for monitoring servers like repl.it projects and also has notifications built-in. Discord webhooks currently supported.

## Setup

Currently, there are two ways to setup and run `keepalive-service`:

1. [Clone, setup, and run this repo directly](#direct-installation)
2. [Use the prebuilt docker container](#using-docker)

The following sections describe how to use both approaches.

### Direct Installation

Clone the repo:

```sh
git clone https://github.com/madhavarshney/keepalive-service
cd keepalive-service
```

Install Python 3 and pip, and then install the required packages:

```sh
python3 -m pip install -r requirements.txt
```

Create a file called `config.yaml` with your configuration [(see below)](#configuration) and then start the monitoring script:

```sh
python3 -m keepalive
```

### Using Docker

This service can also be run as a docker container. Prebuilt images are available at [ghcr.io/madhavarshney/keepalive-service](https://ghcr.io/madhavarshney/keepalive-service). The config file should be bind-mounted as a volume to `/keepalive-service/config.yaml`, and `--init` should be enabled.

Running with Docker:

```sh
docker run --init \
  -v "$(pwd)"/config.yaml:/keepalive-service/config.yaml \
  ghcr.io/madhavarshney/keepalive-service:latest
```

Using Docker Compose:

```yaml
version: "3.9"

services:
  keepalive:
    image: ghcr.io/madhavarshney/keepalive-service:latest

    restart: always
    init: true

    volumes:
      - ./config.yaml:/keepalive-service/config.yaml:ro
```

## Configuration

The configuration file `config.yaml` should follow the following format:


```yaml
# Time in seconds to recheck the services
interval: 60

# Discord Webhook URL to send notifications to
discord_webhook_url: https://discordapp.com/api/webhooks/...

# Service definitions
services:
  - name: Repl.it HTTP Project
    check:
      # Check a generic HTTP service hosted on repl.it
      # This fetches the specified URL and verifies that the returned content matches "data".
      type: REPL_HTTP_SERVICE
      url: https://coolnewthing.someone.repl.co
      data: Service is working.

  - name: My Webpage
    check:
      # Check a generic webpage with HTML content.
      # This verifies that the HTML <title> element matches "data".
      type: HTML_TITLE
      url: https://webpage.someone.repl.co
      data: The Daily News
```

## License

The [MIT License](LICENSE).
