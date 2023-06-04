import shutil
import zipfile

import requests
from json2xml import json2xml
from langcodes import Language
from PIL import Image
from pathlib import Path

from pycbzhelper.comicinfo import KEYS_STRING, KEYS_INT, KEYS_SPECIAL, KEYS_AGE, KEYS_FORMAT, KEYS_PAGE_TYPE
from pycbzhelper.exceptions import InvalidKeyValue, MissingPageFile, FileNotFound, InvalidFileExtension
from pycbzhelper.utils import get_key_value, delete_none

TMP = Path.home().resolve() / ".cbzhelper"


class Helper:

    def __init__(self, kwargs):
        self._pages = []
        self.comic_info = self._comic_info(kwargs)

    def _comic_info(self, kwargs) -> str:
        for key in KEYS_STRING:
            value = kwargs.get(key)
            if value is not None and not isinstance(value, str):
                raise InvalidKeyValue(f"Key must be string: {key}")

        for key in KEYS_INT:
            value = kwargs.get(key)
            if value is not None and not isinstance(value, int):
                raise InvalidKeyValue(f"Key must be integer: {key}")

        for key in KEYS_SPECIAL:
            value = kwargs.get(key)
            if value is not None:
                if key == "BlackAndWhite" and get_key_value(value) not in ["Yes", "No"]:
                    raise InvalidKeyValue(f"Key must be boolean: {key}")
                elif key == "Manga" and get_key_value(value) not in ["YesAndRightToLeft", "Yes", "No"]:
                    raise InvalidKeyValue(f"Key must be boolean or special boolean: {key}")
                elif key == "AgeRating" and value not in KEYS_AGE:
                    raise InvalidKeyValue(f"Key must be special age: {key}")
                elif key == "LanguageISO" and not Language.get(value).is_valid():
                    raise InvalidKeyValue(f"Key must be ISO language: {key}")
                elif key == "Format" and value not in KEYS_FORMAT:
                    raise InvalidKeyValue(f"Key must be special format: {key}")
                elif key == "Pages":
                    if isinstance(value, list):
                        for file in value:
                            page_file = file.get("File")
                            if isinstance(page_file, Path):
                                if not page_file.is_file():
                                    raise FileNotFound("File does not exist.")
                            elif isinstance(page_file, str):
                                if not page_file.startswith("http"):
                                    raise InvalidKeyValue(f"Key must be an existing file path: {key}")
                            else:
                                raise InvalidKeyValue(f"Key must be an existing file path: {key}")

                            page_type = file.get("Type")
                            if page_type and page_type not in KEYS_PAGE_TYPE:
                                raise InvalidKeyValue("Key must be special type: Type")
                            page_double = file.get("DoublePage")
                            if page_double and get_key_value(page_double) not in ["Yes", "No"]:
                                raise InvalidKeyValue("Key must be boolean: DoublePage")
                    else:
                        raise InvalidKeyValue(f"Key must be a list: {key}")

        xml_pages = []
        pages = kwargs.get("Pages") or []
        if len(pages) > 0:
            # [{"File": "FILE_PATH", "Type": "FrontCover", "DoublePage": False, "Bookmark": "", "Key": ""}]
            kwargs["PageCount"] = len(pages)
            xml_pages.append("	<Pages>")

            for i, file in enumerate(pages):
                page_file = file["File"]
                if isinstance(page_file, str):
                    r = requests.get(page_file)
                    r.raise_for_status()
                    content = r.content
                else:
                    content = page_file.read_bytes()

                page_file = TMP / f"page-{i:03d}.jpg"
                page_file.parent.mkdir(parents=True, exist_ok=True)
                page_file.write_bytes(content)
                self._pages.append(page_file)

                properties = Image.open(page_file)
                page_type = file.get("Type") or "FrontCover" if i == 0 else "Story"

                items = ["		<Page"]
                page_double = get_key_value(file.get("DoublePage", False))
                if page_double == "Yes":
                    items.append('DoublePage="True"')

                page_bookmark = file.get("Bookmark")
                if page_bookmark:
                    items.append(f'Bookmark="{page_bookmark}"')

                page_key = file.get("Key")
                if page_key:
                    items.append(f'Key="{page_key}"')

                xml_pages.append(
                    " ".join(
                        items) + ' Image="{image}" ImageHeight="{height}" ImageSize="{size}" ImageWidth="{width}" Type="{type}"/>'.format(
                        double=str(page_double == "Yes"),
                        image=i,
                        height=properties.height,
                        size=len(properties.fp.read()),
                        width=properties.width,
                        type=page_type
                    ))
            xml_pages.append("	</Pages>")
        xml_pages.append("</ComicInfo>")
        kwargs.pop("Pages", None)

        dict_data = {}
        for key in KEYS_STRING + KEYS_INT + KEYS_SPECIAL:
            dict_data[key] = get_key_value(kwargs.get(key))

        xml_data = json2xml.Json2xml(delete_none(dict_data), wrapper="ComicInfo", pretty=True, attr_type=False, item_wrap=False).to_xml()

        if not xml_data:
            xml_data = "\n".join(['<?xml version="1.0" ?>', "<ComicInfo>", "</ComicInfo>"])
            print("WARNING: No metadata to create.")
        xml_data = xml_data.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="utf-8"?>')
        xml_data = xml_data.replace("</ComicInfo>", "\n".join(xml_pages))
        return xml_data.strip()

    def create_cbz(self, path: Path) -> None:
        if not len(self._pages) > 0:
            raise MissingPageFile("No pages available.")
        if path.suffix != ".cbz":
            raise InvalidFileExtension("Invalid file extension.")

        path.parent.mkdir(parents=True, exist_ok=True)
        cbz = zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED)
        clear_path = []

        for i, page in enumerate(self._pages):
            clear_path.append(page)
            cbz.writestr(f"page-{i + 1:03d}{page.suffix}", data=page.read_bytes())

        cbz.writestr("ComicInfo.xml", data=self.comic_info.encode("utf-8"))
        cbz.close()

        self._pages = []
        shutil.rmtree(TMP)
