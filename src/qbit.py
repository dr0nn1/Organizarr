import requests


class Qbit:
    def __init__(self, baseUrl: str, port: str):
        self.baseUrl = baseUrl
        self.port = port

    def getTorrents(self) -> list[str]:
        response = requests.get(
            f"http://{self.baseUrl}:{self.port}/api/v2/torrents/info"
        )
        if response.status_code == 200:
            data = response.json()
            return [item["hash"] for item in data]
        return []

    def getFiles(self, hash: str) -> list[str]:
        response = requests.get(
            f"http://{self.baseUrl}:{self.port}/api/v2/torrents/files?hash={hash}"
        )
        if response.status_code == 200:
            data = response.json()
            return [item["name"] for item in data]
        return []

    def deleteTorrent(self, hash: str) -> bool:
        form_data = {"hashes": hash, "deleteFiles": "true"}
        response = requests.post(
            f"http://{self.baseUrl}:{self.port}/api/v2/torrents/delete", data=form_data
        )
        if response.status_code == 200:
            return True
        return False

    def checkForInvalidFiles(self):
        try:
            hashes = self.getTorrents()
            for hash in hashes:
                files = self.getFiles(hash)
                if self.invalidFileType(files):
                    print(f"Deleting hash: {hash}")
                    self.deleteTorrent(hash)
        except Exception as e:
            print(f"Error occurred when deleting torrents", e)

    def invalidFileType(self, files: list[str]) -> bool:
        invalidTypes = ["lnk"]
        for file in files:
            ext = file.split(".")[-1]
            if ext in invalidTypes:
                return True
        return False


if __name__ == "__main__":
    # pass
    qbit = Qbit("xxx.xxx.x.xxx", "8090")
    qbit.checkForInvalidFiles()
