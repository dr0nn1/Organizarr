from sonarr import Sonarr
import schedule
import logging
import time
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def loadConfig(filePath="config.yaml") -> dict:
    with open(filePath, "r") as file:
        return yaml.safe_load(file)


def getDictOfSeries() -> dict:
    series = sonarr.getAllSeries()
    if series.status_code == 200:
        data = series.json()
        return {
            series["id"]: [
                season["seasonNumber"]
                for season in series["seasons"]
                if season.get("statistics", {}).get("episodeFileCount", 0) > 0
            ]
            for series in data
        }
    return {}


def getRename(serieId: int, seasonNumber: int) -> list[str]:
    response = sonarr.getRename(serieId, seasonNumber)
    if response.status_code == 200:
        data = response.json()
        return [item["episodeFileId"] for item in data]
    return []


def start():
    data = getDictOfSeries()
    for index, (seriesId, seasons) in enumerate(data.items(), start=1):
        for season in seasons:
            renameEpisodes = getRename(seriesId, season)
            if len(renameEpisodes) > 0:
                sonarr.renameCommand(seriesId, renameEpisodes)
                logging.info(
                    f"Checked {index} of {len(data)} series - Renaming serie = {seriesId}, episodes = {renameEpisodes}"
                )
                time.sleep(60)  # 1 min, prevent flooding of sonarr
    logging.info("Finished cleanup")


if __name__ == "__main__":
    config = loadConfig()
    sonarrConfig = config["sonarr"]
    sonarr = Sonarr(sonarrConfig["host"], sonarrConfig["port"], sonarrConfig["api_key"])

    scheduleTime = config["schedule"]["time"]
    schedule.every().day.at(scheduleTime).do(start)

    sleepTime = config["schedule"]["sleep"]

    logging.info(f"Scheduler set to run daily at {scheduleTime}. Waiting for tasks...")

    while True:
        try:
            schedule.run_pending()
            time.sleep(sleepTime)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
