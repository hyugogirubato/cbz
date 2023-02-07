import os
import pathlib
import shutil
import zipfile

from json2xml import json2xml
from langcodes import Language
from PIL import Image

from pycbzhelper.comicinfo import KEYS_STRING, KEYS_INT, KEYS_SPECIAL, KEYS_AGE, KEYS_FORMAT, KEYS_PAGE_TYPE
from pycbzhelper.exceptions import InvalidKeyValue, MissingPageFile, InvalidFilePermission
from pycbzhelper.utils import get_key_value, delete_none, slugify


class Helper:

    def __init__(self, kwargs):
        self._files = []
        self.metadata = self._get_metadata(kwargs)

    def _get_metadata(self, kwargs) -> str:
        # NOTE: Check metadata
        for key in KEYS_STRING:
            if kwargs.get(key) and not isinstance(kwargs.get(key), str):
                raise InvalidKeyValue(f"ERROR: Key must be string: {key}")

        for key in KEYS_INT:
            if kwargs.get(key) and not isinstance(kwargs.get(key), int):
                raise InvalidKeyValue(f"ERROR: Key must be integer: {key}")

        for key in KEYS_SPECIAL:
            if kwargs.get(key):
                if key == 'BlackAndWhite' and get_key_value(kwargs.get(key)) not in ['Yes', 'No']:
                    raise InvalidKeyValue(f"ERROR: Key must be boolean: {key}")
                elif key == 'Manga' and get_key_value(kwargs.get(key)) not in ['YesAndRightToLeft', 'Yes', 'No']:
                    raise InvalidKeyValue(f"ERROR: Key must be boolean or special boolean: {key}")
                elif key == 'AgeRating' and kwargs.get(key) not in KEYS_AGE:
                    raise InvalidKeyValue(f"ERROR: Key must be special age: {key}")
                elif key == 'LanguageISO' and not Language.get(kwargs.get(key)).is_valid():
                    raise InvalidKeyValue(f"ERROR: Key must be ISO language: {key}")
                elif key == 'Format' and kwargs.get(key) not in KEYS_FORMAT:
                    raise InvalidKeyValue(f"ERROR: Key must be special format: {key}")
                elif key == 'Pages':
                    if isinstance(kwargs.get(key), list):
                        for page in kwargs.get(key):
                            if not page.get('File') or not isinstance(page.get('File'), str) or not os.path.exists(page.get('File')):
                                raise InvalidKeyValue(f"ERROR: Key must be existing string path: {key}")
                            if page.get('Type') and not page.get('Type') in KEYS_PAGE_TYPE:
                                raise InvalidKeyValue("ERROR: Key must be special type: Type")
                            if page.get('DoublePage') and get_key_value(page.get('DoublePage')) not in ['Yes', 'No']:
                                raise InvalidKeyValue("ERROR: Key must be boolean: DoublePage")
                    else:
                        raise InvalidKeyValue(f"ERROR: Key must be a list: {key}")

        # NOTE: Set metadata
        pages = []
        if kwargs.get('Pages'):
            # [{'File': 'FILE_PATH', 'Type': 'FrontCover', 'DoublePage': False}]
            pages.append("	<Pages>")
            kwargs['PageCount'] = len(kwargs.get('Pages'))
            for i in range(kwargs.get('PageCount')):
                page = kwargs.get('Pages')[i]
                properties = Image.open(page['File'])
                self._files.append(page['File'])
                if not page.get('Type'):
                    page['Type'] = 'FrontCover' if i == 0 else 'Story'

                item = '		<Page DoublePage="True"' if get_key_value(page.get('DoublePage', False)) == 'Yes' else '		<Page'
                pages.append(
                    item + ' Image="{image}" ImageHeight="{height}" ImageSize="{size}" ImageWidth="{width}" Type="{type}" />'.format(
                        double="False" if get_key_value(page.get('DoublePage', False)) == 'No' else "True",
                        image=i,
                        height=properties.height,
                        size=len(properties.fp.read()),
                        width=properties.width,
                        type=page['Type']
                    )
                )
            pages.append("	</Pages>")
            del kwargs['Pages']
        pages.append("</ComicInfo>")

        json_data = {}
        for key in KEYS_STRING + KEYS_INT + KEYS_SPECIAL:
            json_data[key] = get_key_value(kwargs.get(key))

        xml_data = json2xml.Json2xml(delete_none(json_data), wrapper="ComicInfo", pretty=True, attr_type=False).to_xml()
        if not xml_data:
            xml_data = '\n'.join(['<?xml version="1.0" ?>', '<ComicInfo>', '</ComicInfo>'])
            print('WARNING: No metadata to create.')
        xml_data = xml_data.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="utf-8"?>')
        xml_data = xml_data.replace('</ComicInfo>', '\n'.join(pages))
        return xml_data.strip()

    def save_cbz(self, path: str, file: str, clear: bool = False, replace: bool = True) -> None:
        if len(self._files) == 0:
            raise MissingPageFile('ERROR: No pages available.')

        output = os.path.join(path, f"{slugify(file, allow_unicode=False)}.cbz")
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(output) and not replace:
            raise InvalidFilePermission('ERROR: File already exists. The replace option is not enabled.')
        elif os.path.exists(output):
            os.remove(output)

        clear_path = []
        cbz = zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED)
        for i in range(len(self._files)):
            if os.path.dirname(self._files[i]) not in clear_path:
                clear_path.append(os.path.dirname(self._files[i]))
            with open(self._files[i], mode='rb') as f:
                extension = pathlib.Path(self._files[i]).suffix
                cbz.writestr(f"page-{i + 1:03d}.{'.jpg' if extension == '' else extension}", data=f.read())
                f.close()
        cbz.writestr('ComicInfo.xml', data=self.metadata.encode('utf-8'))
        cbz.close()
        print(f"INFO: File create: {output}")
        if clear:
            for path in clear_path:
                shutil.rmtree(path)
                print(f"INFO: Folder deleted: {path}")
