from datetime import datetime
from base64 import b64encode
from PIL import Image
from io import BytesIO
import requests

_current_timestamp = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Content(object):
    IMAGE_MAX_WIDTH = 384

    def __init__(self):
        self.parts = []

    def add_text(self, text):
        self.parts.append(("T", text))

    def add_image(self, fp_or_file_path):
        image = Image.open(fp_or_file_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        width, height = image.size
        if width > self.IMAGE_MAX_WIDTH:
            image = image.resize((self.IMAGE_MAX_WIDTH, height * 384 // width),
                                 Image.ANTIALIAS)
        image = image.convert("1")
        p = BytesIO()
        image.save(p, "BMP")
        self.parts.append(("P", p.getvalue()))

    def to_string(self):
        encoded = []
        last = len(self.parts) - 1
        for index, (content_type, data) in enumerate(self.parts):
            if content_type == "T":
                if not index == last and not data.endswith("\n"):
                    data += "\n"
                encoded.append("T:"+b64encode(data.encode("GBK")).decode("ascii"))
            elif content_type == "P":
                encoded.append("P:"+b64encode(data).decode("ascii"))
        return "|".join(encoded)


class Pymobird(object):
    BASE_URL = "http://open.memobird.cn/home"
    _headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, ak):
        if not ak:
            print("ak not provided")
        self._ak = ak
        self._session = requests.session()

    def _url(self, path):
        return self.BASE_URL + path

    def get_user_id(self, device_id, user_identifying):
        path = "/setuserbind"
        data = {
            "ak": self._ak,
            "timestamp": _current_timestamp(),
            "memobirdID": device_id,
            "useridentifying": user_identifying,
        }
        resp = self._session.get(self._url(path), params=data, headers=self._headers)
        resp.raise_for_status()
        user_id = resp.json()["showapi_userid"]
        return user_id

    def _print(self, device_id, user_id, content):
        path = "/printpaper"
        data = {
            "ak": self._ak,
            "timestamp": _current_timestamp(),
            "printcontent": content.to_string(),
            "memobirdID": device_id,
            "userID": user_id,
        }
        resp = self._session.post(self._url(path), json=data, headers=self._headers)
        resp.raise_for_status()
        content_id = resp.json()["printcontentid"]
        return content_id

    def print_text(self, device_id, user_id, text):
        content = Content()
        content.add_text(text)
        return self._print(device_id, user_id, content)

    def print_image(self, device_id, user_id, image):
        content = Content()
        content.add_image(image)
        return self._print(device_id, user_id, content)

    def print_multi_part_content(self, device_id, user_id, content):
        return self._print(device_id, user_id, content)

    def check_printed(self, content_id):
        path = "/getprintstatus"
        resp = self._session.get(self._url(path),
                                 params={"ak": self._ak,
                                         "timestamp": _current_timestamp(),
                                         "printcontentid": content_id},
                                 headers=self._headers)
        resp.raise_for_status()
        return resp.json()["printflag"] == 1


class SimplePymobird(object):
    """for single device"""

    def __init__(self, ak, device_id, user_identifying):
        self._bird = Pymobird(ak)
        self.device_id = device_id
        self.user_id = self._bird.get_user_id(self.device_id, user_identifying)

    def print_text(self, text):
        return self._bird.print_text(self.device_id, self.user_id, text)

    def print_image(self, image):
        return self._bird.print_image(self.device_id, self.user_id, image)

    def print_multi_part_content(self, content):
        return self._bird.print_multi_part_content(self.device_id, self.user_id, content)

    def check_printed(self, content_id):
        return self._bird.check_printed(content_id)

