import requests


class AppCenterAPI:
    def __init__(self, x_api_token, owner_name, app_name, ipa):
        self.base_url = "https://api.appcenter.ms/v0.1"
        self.headers = {"X-API-Token": x_api_token}
        self.owner_name = owner_name
        self.app_name = app_name
        self.ipa = ipa

    @property
    def apps_uri(self):
        return f"apps/{self.owner_name}/{self.app_name}"

    def get(self, url):
        req = requests.get(f"{self.base_url}/{url}",
                           headers=self.headers)
        try:
            return req.json()
        except:
            return req

    def post(self, url, file_data=None, json_data=None):
        req = requests.post(url=f"{self.base_url}/{url}",
                            data=file_data,
                            json=json_data,
                            headers=self.headers)
        try:
            return req.json()
        except:
            return req

    def get_app_info(self):
        return self.get(f"apps/{self.owner_name}/{self.app_name}/")

    def get_app_releases(self):
        return self.get(f'apps/{self.owner_name}/{self.app_name}/releases')

    def get_latest_release(self):
        releases = self.get_app_releases()
        all_branches = [release['id'] for release in releases]
        uitest = [release['id'] for release in releases if release['build']['branchName'] == 'uitest']

        if uitest:
            return max(uitest)

        return max(all_branches)

    def get_download_uri(self, release_number=None):
        if not release_number:
            release_number = self.get_latest_release()

        res = self.get(f"apps/{self.owner_name}/{self.app_name}/"
                       f"builds/{release_number}/downloads/build")

        return res['uri']

    def get_test_runs(self, test_run_id=None):
        if test_run_id:
            return self.get(f"apps/{self.owner_name}/{self.app_name}/test_runs/{test_run_id}")
        else:
            return self.get(f"apps/{self.owner_name}/{self.app_name}/test_runs")
