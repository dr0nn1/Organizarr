import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Sonarr:
    def __init__(self, baseUrl: str, port: str, apiKey: str):
        self.baseUrl = baseUrl
        self.port = port
        self.apiKey = apiKey

    def getAllSeries(self) -> requests.Response:
        return self.getRequest("series")

    def getRename(self, seriesId: int, seasonNumber: int) -> requests.Response:
        return self.getRequest(
            "rename", f"&seriesId={seriesId}&seasonNumber={seasonNumber}"
        )
    
    def getSeriesName(self, seriesId: int) -> str:
        try:
            response = self.getRequest(f"series/{seriesId}", f"&includeSeasonImages=false")
            response_json = response.json()
        except Exception as e:
            logging.error(f"An error occurred while getting series name: {e}")
            return "no name"
            
        if response.status_code == 200 and "title" in response_json:
            return response_json["title"]
        return "no name"

    def getRequest(self, path: str, variables: str = "") -> requests.Response:
        return requests.get(
            f"http://{self.baseUrl}:{self.port}/api/v3/{path}?apikey={self.apiKey}{variables}"
        )

    def postRequest(self, path: str, body: dict) -> requests.Response:
        requests.post(
            f"http://{self.baseUrl}:{self.port}/api/v3/{path}?apikey={self.apiKey}",
            json=body,
        )

    def renameCommand(self, seriesId: int, files: list[int]) -> bool:
        body = {"name": "RenameFiles", "seriesId": seriesId, "files": files}
        self.postRequest("command", body)
