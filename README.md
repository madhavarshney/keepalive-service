# Keepalive Service

A service to monitor servers and keep 'em alive, such as repl.it projects.

## Setup

Clone the repo:

```sh
git clone https://github.com/madhavarshney/keepalive-service
cd keepalive-service
```

Install Python 3 and pip, and then install the required packages:

```sh
python3 -m pip install -r requirements.txt
```

## Usage

Create a file `config.yaml` with the following options:

```yaml
interval: 60 # time in seconds to recheck the services
discord_webhook_url: https://discordapp.com/api/webhooks/... # Discord Webhook URL to send notifications to
services:
  - name: Cool New Thing
    check:
      type: REPL_HTTP_SERVICE # Check an HTTP service on repl.it
      url: https://coolnewthing.someone.repl.co # URL to fetch
      data: Service is working. # The exact data that would be returned if the service is up.
  - name: My Webpage
    check:
      type: HTML_TITLE # Check an HTML page
      url: https://webpage.someone.repl.co # URL to fetch
      data: UC Transfer Stats # The expected content of the HTML <title> element.
```

Start the monitoring script with:

```sh
python3 -m keepalive
```

## License

The [MIT License](LICENSE.md).
