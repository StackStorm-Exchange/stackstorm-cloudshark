import requests
from st2common.runners.base_action import Action


class UploadPcap(Action):

    def __init__(self, config=None):
        super(UploadPcap, self).__init__(config=config)

        self.host = self.config['host']
        self.apikey = self.config['apikey']

    def run(self, file_path, tags=None):

        url = self.host + 'api/v1/' + self.apikey + '/upload'

        params = {}

        if tags is not None:
            params = {'additional_tags': tags}

        with open(file_path, 'rb') as fp:
            files = {'file': fp}
            resp = requests.post(url, files=files, params=params)

            if resp.status_code != 200:
                raise Exception("Failed to upload PCAP." +
                                "Result: {}, {}".format(resp.status_code, resp.text))

            data = resp.json()
            filename = data['filename']
            pcap_id = data['id']

            link = self.host + 'captures/' + pcap_id

        result = {
            "status_code": resp.status_code,
            "link": link,
            "filename": filename,
            "text": resp.text
        }

        return result
