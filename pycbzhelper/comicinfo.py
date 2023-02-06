"""
Refer:
- https://github.com/comictagger/comictagger
- https://github.com/Kussie/ComicInfoStandard
- https://github.com/anansi-project/comicinfo
"""

KEYS_STRING = [
    'Title', 'Series', 'Number', 'AlternateSeries', 'AlternateNumber',
    'Summary', 'Notes', 'Writer', 'Penciller', 'Inker', 'Colorist',
    'Letterer', 'CoverArtist', 'Editor', 'Publisher', 'Imprint', 'Genre',
    'Web', 'Characters', 'Teams', 'Locations', 'ScanInformation',
    'StoryArc', 'SeriesGroup', 'CommunityRating'
]

KEYS_INT = [
    'Count', 'Volume', 'AlternateCount', 'Year', 'Month', 'Day', 'PageCount'
]

KEYS_SPECIAL = [
    'BlackAndWhite', 'Manga', 'AgeRating', 'Pages', 'LanguageISO', 'Format', 'ESN'
]

KEYS_AGE = [
    'Adults Only 18+', 'Early Childhood', 'Everyone', 'Everyone 10+',
    'G', 'Kids to Adults', 'M', 'MA 15+', 'Mature 17+', 'PG', 'R18+',
    'Rating Pending', 'Teen', 'X18+', 'Rating Pending'
]

KEYS_FORMAT = [
    '1 Shot', '1/2', '1-Shot', 'Annotation', 'Annotations',
    'Annual', 'Anthology', 'B&W', 'B/W', 'B&&W', 'Black & White', 'Box Set',
    'Box-Set', 'Crossover', "Director's Cut", 'Epilogue', 'Event', 'FCBD',
    'Flyer', 'Giant', 'Giant Size', 'Giant-Size', 'Graphic Novel', 'Hardcover',
    'Hard-Cover', 'King', 'King Size', 'King-Size', 'Limited Series', 'Magazine',
    'NSFW', 'One Shot', 'One-Shot', 'Point 1', 'Preview', 'Prologue', 'Reference',
    'Review', 'Reviewed', 'Scanlation', 'Script', 'Series', 'Sketch', 'Special',
    'TPB', 'Trade Paper Back', 'WebComic', 'Web Comic', 'Year 1', 'Year One'
]

KEYS_PAGE_TYPE = [
    'FrontCover', 'InnerCover', 'Roundup', 'Story', 'Advertisment',
    'Editorial', 'Letters', 'Preview', 'BackCover', 'Other', 'Deleted'
]
