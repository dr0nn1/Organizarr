import requests

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
