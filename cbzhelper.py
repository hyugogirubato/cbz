"""
Project: cbzhelper
File: cbzhelper.py
Author: hyuogirubato
Date: 2022.08.30
"""

import os.path
import re
import shutil
import zipfile
from PIL import Image


def clear(value):
    return re.sub('[^\w\-_\.\(\)\[\] ]', '_', value)


class Helper:

    def __init__(self, path, file, replace=True):
        self.path = path
        self.file = f"{clear(file)}.cbz"
        self.output = os.path.join(self.path, self.file)
        self.tmp = os.path.join(self.path, 'tmp')
        self.pages = []
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(self.output) and replace:
            os.remove(self.output)


    # https://github.com/Kussie/ComicInfoStandard/blob/main/ComicInfo.xsd
    def addMetadata(self, metadata):
        metadata['Pages'] = self.pages

        comic_config = {
            'str': ['Title', 'Series', 'Number', 'AlternateSeries', 'AlternateNumber',
                  'Summary', 'Notes', 'Writer', 'Penciller', 'Inker', 'Colorist',
                  'Letterer', 'CoverArtist', 'Editor', 'Publisher', 'Imprint',
                  'Genre', 'Web', 'LanguageISO', 'Characters', 'Teams',
                  'Locations', 'ScanInformation', 'StoryArc', 'SeriesGroup'],
            'int': ['Count', 'Volume', 'AlternateCount', 'Year', 'Month', 'PageCount'],
            'float': ['CommunityRating', 'BookPrice'],
            'YesNo': ['BlackAndWhite'],
            'Manga': ['Manga'],
            'AgeRating': ['AgeRating'],
            'ArrayOfComicPageInfo': ['Pages'],
            'Format': ['Format']
        }

        page_config = {
            'int': ['Image', 'ImageWidth', 'ImageHeight'],
            'bool': ['DoublePage'],
            'long': ['ImageSize'],
            'str': ['Key'],
            'ComicPageType': ['Type']
        }

        comic_info = []
        comic_info.append("<?xml version='1.0' encoding='utf-8'?>")
        comic_info.append('<ComicInfo>')

        metadata_keys = metadata.keys()

        # default
        if not 'BlackAndWhite' in metadata_keys:
            metadata['BlackAndWhite'] = 'Unknown'
        if not 'Manga' in metadata_keys:
            metadata['Manga'] = 'Unknown'
        if not 'AgeRating' in metadata_keys:
            metadata['AgeRating'] = 'Unknown'

        for key in metadata_keys:
            if key in comic_config['YesNo'] and metadata[key] in ['No', 'Yes']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['Manga'] and metadata[key] in ['No', 'Yes', 'YesAndRightToLeft']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['AgeRating'] and metadata[key] in ['Everyone', 'G', 'Early Childhood', 'Everyone 10+', 'PG',
                                                                        'Kids to Adults', 'Teen', 'M', 'MA15+', 'Mature 17+',
                                                                        'R18+', 'X18+', 'Adults Only 18+', 'Rating Pending']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['str']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['int']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['float']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['Format'] and metadata[key] in ['.1', '-1', '1 Shot', '1/2', '1-Shot', 'Annotation', 'Annotations',
                                                                     'Annual', 'Anthology', 'B&W', 'B/W', 'B&&W', 'Black & White', 'Box Set',
                                                                     'Box-Set', 'Crossover', 'Director\'s Cut', 'Epilogue', 'Event', 'FCBD',
                                                                     'Flyer', 'Giant', 'Giant Size', 'Graphic Novel', 'Hardcover', 'Hard-Cover',
                                                                     'King', 'King Size', 'King-Size', 'Limited Series', 'Magazine', 'NSFW',
                                                                     'One Shot', 'One-Shot', 'Point 1', 'Preview', 'Prologue', 'Reference', 'Review',
                                                                     'Reviewed', 'Scanlation', 'Script', 'Series', 'Sketch', 'Special', 'TPB',
                                                                     'Trade Paper Back', 'WebComic', 'Web Comic', 'Year 1', 'Year One']:
                comic_info.append(f'  <{key}>{metadata[key]}</{key}>')
            elif key in comic_config['ArrayOfComicPageInfo']:
                comic_info.append('  <Pages>')
                for item in metadata[key]:
                    item_keys =item.keys()
                    line = []

                    line.append('    <Page')

                    # default
                    if not 'Type' in item_keys:
                        metadata[key]['Type'] = 'Story'
                    if not 'DoublePage' in item_keys:
                        metadata[key]['DoublePage'] = False

                    for item_key in item_keys:
                        if item_key in page_config['int']:
                            line.append(f'{item_key}="{metadata[key][item_key]}"')
                        elif item_key in page_config['bool']:
                            value = 'true' if metadata[key][item_key] else 'false'
                            line.append(f'{item_key}="{value}"')
                        elif item_key in page_config['long']:
                            line.append(f'{item_key}="{metadata[key][item_key]}"')
                        elif item_key in page_config['str']:
                            line.append(f'{item_key}="{metadata[key][item_key]}"')
                        elif item_key in page_config['ComicPageType'] and metadata[key][item_key] in ['FrontCover', 'InnerCover', 'Roundup', 'Story',
                                                                                                      'Advertisment', 'Editorial', 'Letters', 'Preview',
                                                                                                      'BackCover', 'Other', 'Deleted']:
                            line.append(f'{item_key}="{metadata[key][item_key]}"')
                    line.append('/>')
                    comic_info.append(' '.join(line))

                comic_info.append('  </Pages>')
        comic_info.append('</ComicInfo>')

        with open(os.path.join(self.tmp, 'ComicInfo.xml'), mode='w', encoding='utf-8') as f:
            f.write('\n'.join(comic_info))


    def addPage(self, image, content, double_page=False, page_type='DEFAULT', extension='jpg'):
        page = os.path.join(self.tmp, f"page-{image:03d}.{extension}")
        if not os.path.exists(page):
            with open(page, mode='wb') as f:
                f.write(content)

        properties = Image.open(page)
        if page_type == 'DEFAULT' or not page_type in ['FrontCover', 'InnerCover', 'Roundup', 'Story',
                                                       'Advertisment', 'Editorial', 'Letters', 'Preview',
                                                       'BackCover', 'Other', 'Deleted']:
            page_type = 'FrontCover' if image == 1 else 'Story'

        self.pages.append({
            'Image': image,
            'Type': page_type,
            'DoublePage': double_page,
            'ImageSize': properties.size,
            'ImageWidth': properties.width,
            'ImageHeight': properties.height
        })

    def saveCBZ(self):
        if os.path.exists(self.tmp):
            if not os.path.exists(self.output):
                cbz = zipfile.ZipFile(f"{self.output}.cbz", 'w', compression=zipfile.ZIP_STORED)
                for file in sorted(os.listdir(self.tmp), key=len):
                    with open(os.path.join(self.tmp, file), mode='rb') as f:
                        cbz.writestr(file, data=f.read())
                cbz.close()
            shutil.rmtree(self.tmp)
