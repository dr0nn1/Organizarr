# Organizarr

## Config:

Add a config like this:

```
sonarr:
  host: "xxx.xxx.x.xxx"
  port: "8989"
  api_key: "xxxxxxxxxxxxxxx"
qbit:
  host: "xxx.xxx.x.xxx"
  port: "8090"
  interval: 120 # Minute. Scans every x minute
schedule:
  time: "hh:mm" # Example 16:38
  sleep: 300 # Seconds. Example, if you schedule the task at 14:00 and your script happens to be sleeping at 13:59:59, the task will execute closer to 14:05.
```

## Docker compose:

```
services:
  organizarr:
    image: dr0nn1/organizarr
    container_name: organizarr
    environment:
      - TZ=Europe/Oslo
    volumes:
      - "path/to/config.yaml:/home/myuser/code/config.yaml"
    restart: unless-stopped
```

## Build docker:

docker build -t organizarr .

## TODO:

Add Radarr?
