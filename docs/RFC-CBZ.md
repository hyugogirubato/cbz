# RFC: CBZ (Comic Book ZIP) Format Specification

**Version:** 1.0  
**Status:** Informational  
**Date:** 2026-04-06  
**Authors:** hyugogirubato, contributors  

---

## 1. Abstract

This document specifies the CBZ (Comic Book ZIP) file format, a widely-adopted standard for packaging and distributing digital comic books, manga, and graphic novels. CBZ files are ZIP archives containing sequential image files and an optional XML metadata descriptor (`ComicInfo.xml`). This RFC consolidates existing community practices, the ComicInfo XML schema (versions 1.0 through 2.1), and implementation experience into a single authoritative reference.

## 2. Status of This Document

This document is an informational specification. It describes the CBZ format as implemented by major comic book readers and management tools including ComicRack, Kavita, Komga, Calibre, YACReader, and others. The format originated from the ComicRack application and has been extended by the community through the anansi-project.

## 3. Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

| Term              | Definition                                                                      |
|-------------------|---------------------------------------------------------------------------------|
| **CBZ**           | Comic Book ZIP - A ZIP archive containing comic book pages as images            |
| **CBR**           | Comic Book RAR - Similar format using RAR compression (read-only in most tools) |
| **ComicInfo.xml** | XML metadata descriptor file embedded in the archive                            |
| **Page**          | A single image representing one page of the comic                               |
| **Double Page**   | A single image representing a two-page spread                                   |

## 4. File Format Overview

### 4.1 MIME Type

```
application/vnd.comicbook+zip
```

The file extension is `.cbz` (case-insensitive).

### 4.2 Archive Structure

A CBZ file is a standard ZIP archive (as defined in PKWARE APPNOTE) with the following structure:

```
archive.cbz (ZIP)
+-- ComicInfo.xml          (OPTIONAL - metadata descriptor)
+-- page-001.jpg           (image file)
+-- page-002.jpg           (image file)
+-- page-003.png           (image file)
+-- ...
```

### 4.3 Archive Requirements

1. The archive MUST be a valid ZIP file conforming to PKWARE's ZIP Application Note.
2. The archive SHOULD use `ZIP_STORED` (no compression) as the compression method, since image formats already employ their own compression. Using `ZIP_DEFLATED` is permitted but offers negligible size reduction at a performance cost.
3. The archive MUST contain at least one image file.
4. The archive MAY contain a `ComicInfo.xml` metadata file at the root level.
5. The archive MUST NOT contain executable files, scripts, or other non-image/non-metadata content at the root level. Subdirectories (e.g., `__MACOSX/`) SHOULD be ignored by readers.

### 4.4 File Naming

1. Image files SHOULD be named to sort in reading order using standard lexicographic (alphabetical) sorting.
2. The RECOMMENDED naming convention is zero-padded sequential names: `page-001.ext`, `page-002.ext`, etc.
3. Readers MUST sort image files alphabetically (case-insensitive) to determine page order when no `ComicInfo.xml` page index is present.
4. The metadata file MUST be named exactly `ComicInfo.xml` (case-sensitive).

## 5. Supported Image Formats

### 5.1 Required Support

Conforming readers MUST support the following image formats:

| Format | Extensions      | MIME Type    |
|--------|-----------------|--------------|
| JPEG   | `.jpg`, `.jpeg` | `image/jpeg` |
| PNG    | `.png`          | `image/png`  |

### 5.2 Recommended Support

Conforming readers SHOULD support:

| Format | Extensions      | MIME Type    |
|--------|-----------------|--------------|
| GIF    | `.gif`          | `image/gif`  |
| BMP    | `.bmp`          | `image/bmp`  |
| WebP   | `.webp`         | `image/webp` |
| TIFF   | `.tiff`, `.tif` | `image/tiff` |

### 5.3 Optional Support

Conforming readers MAY support:

| Format  | Extensions | MIME Type    |
|---------|------------|--------------|
| JPEG XL | `.jxl`     | `image/jxl`  |
| AVIF    | `.avif`    | `image/avif` |

### 5.4 Image Guidelines

1. All image files within a single archive SHOULD use the same format for consistency.
2. Images SHOULD be stored in their original resolution without additional compression artifacts.
3. For optimal compatibility, JPEG is RECOMMENDED for photographic/scanned content, and PNG for digitally-produced content with sharp edges or transparency.
4. Readers MUST determine page dimensions from the actual image data, not from metadata alone.

## 6. ComicInfo.xml Metadata Specification

### 6.1 Overview

The `ComicInfo.xml` file is an XML document that describes the comic book's metadata and page structure. It follows the ComicInfo schema originally developed for the ComicRack application.

### 6.2 XML Declaration

```xml
<?xml version="1.0" encoding="utf-8"?>
```

The file MUST use UTF-8 encoding.

### 6.3 Root Element

```xml

<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    ...
</ComicInfo>
```

The root element MUST be `<ComicInfo>`. The XML namespace declarations are RECOMMENDED for schema validation but not strictly required for parsing.

### 6.4 Comic Metadata Elements

All metadata elements are OPTIONAL. They appear as child elements of `<ComicInfo>` in the order specified below. Absent elements indicate unknown or unset values.

#### 6.4.1 Identification

| Element           | Type        | Default | Description                                                                |
|-------------------|-------------|---------|----------------------------------------------------------------------------|
| `Title`           | `xs:string` | `""`    | Title of the comic issue                                                   |
| `Series`          | `xs:string` | `""`    | Name of the comic series                                                   |
| `Number`          | `xs:string` | `""`    | Issue number within the series (string to support "1.5", "Annual 1", etc.) |
| `Count`           | `xs:int`    | `-1`    | Total number of issues in the series (-1 = unknown)                        |
| `Volume`          | `xs:int`    | `-1`    | Volume number (-1 = unknown)                                               |
| `AlternateSeries` | `xs:string` | `""`    | Alternate series name (for crossovers, reprints)                           |
| `AlternateNumber` | `xs:string` | `""`    | Issue number in the alternate series                                       |
| `AlternateCount`  | `xs:int`    | `-1`    | Total issues in the alternate series                                       |

**Notes:**

- `Number` is typed as string in the schema to accommodate non-integer issue numbers (e.g., "0.5", "Annual 3", "#1/2").
- When `Count` is -1, the series is ongoing or the total is unknown.

#### 6.4.2 Descriptive

| Element     | Type        | Default | Description                                   |
|-------------|-------------|---------|-----------------------------------------------|
| `Summary`   | `xs:string` | `""`    | Synopsis or description of the issue          |
| `Notes`     | `xs:string` | `""`    | Free-form notes (scan quality, source, etc.)  |
| `Genre`     | `xs:string` | `""`    | Genre(s), comma-separated                     |
| `Tags`      | `xs:string` | `""`    | Tags/keywords, comma-separated                |
| `Web`       | `xs:string` | `""`    | URL to the comic's web page or source         |
| `EAN`       | `xs:string` | `""`    | European Article Number (ISBN/barcode)        |
| `BookPrice` | `xs:string` | `""`    | Cover price (free-form string, e.g., "$3.99") |

**Notes:**

- `Genre` and `Tags` use comma-separated values. Readers SHOULD trim whitespace around each value.
- `Web` SHOULD contain a valid URL but no validation is required.

#### 6.4.3 Publication Date

| Element | Type     | Default | Description                 |
|---------|----------|---------|-----------------------------|
| `Year`  | `xs:int` | `-1`    | Publication year (4 digits) |
| `Month` | `xs:int` | `-1`    | Publication month (1-12)    |
| `Day`   | `xs:int` | `-1`    | Publication day (1-31)      |

**Notes:**

- A value of -1 indicates the date component is unknown.
- Readers SHOULD NOT assume Month and Day are present when Year is set.

#### 6.4.4 Credits

| Element       | Type        | Default | Description                       |
|---------------|-------------|---------|-----------------------------------|
| `Writer`      | `xs:string` | `""`    | Writer(s), comma-separated        |
| `Penciller`   | `xs:string` | `""`    | Pencil artist(s), comma-separated |
| `Inker`       | `xs:string` | `""`    | Inker(s), comma-separated         |
| `Colorist`    | `xs:string` | `""`    | Colorist(s), comma-separated      |
| `Letterer`    | `xs:string` | `""`    | Letterer(s), comma-separated      |
| `CoverArtist` | `xs:string` | `""`    | Cover artist(s), comma-separated  |
| `Editor`      | `xs:string` | `""`    | Editor(s), comma-separated        |
| `Translator`  | `xs:string` | `""`    | Translator(s), comma-separated    |

**Notes:**

- All credit fields support multiple names as comma-separated values.
- The `Translator` field was added in schema v2.1.

#### 6.4.5 Publisher

| Element     | Type        | Default | Description                      |
|-------------|-------------|---------|----------------------------------|
| `Publisher` | `xs:string` | `""`    | Publisher name                   |
| `Imprint`   | `xs:string` | `""`    | Publisher's imprint or sub-label |

#### 6.4.6 Classification

| Element         | Type        | Allowed Values                              | Default   | Description                                        |
|-----------------|-------------|---------------------------------------------|-----------|----------------------------------------------------|
| `Format`        | `xs:string` | (see section 6.5)                           | `""`      | Publication format                                 |
| `BlackAndWhite` | `YesNo`     | `Unknown`, `No`, `Yes`                      | `Unknown` | Whether the comic is black and white               |
| `Manga`         | `Manga`     | `Unknown`, `No`, `Yes`, `YesAndRightToLeft` | `Unknown` | Whether the comic is manga (and reading direction) |
| `AgeRating`     | `AgeRating` | (see section 6.7)                           | `Unknown` | Content age rating                                 |
| `LanguageISO`   | `xs:string` | ISO 639 codes                               | `""`      | Language code (e.g., "en", "fr", "ja")             |

#### 6.4.7 Characters and Story

| Element               | Type        | Default | Description                      |
|-----------------------|-------------|---------|----------------------------------|
| `Characters`          | `xs:string` | `""`    | Character names, comma-separated |
| `Teams`               | `xs:string` | `""`    | Team names, comma-separated      |
| `Locations`           | `xs:string` | `""`    | Location names, comma-separated  |
| `MainCharacterOrTeam` | `xs:string` | `""`    | Primary character or team        |
| `StoryArc`            | `xs:string` | `""`    | Story arc name                   |
| `StoryArcNumber`      | `xs:string` | `""`    | Position within the story arc    |
| `SeriesGroup`         | `xs:string` | `""`    | Series grouping or universe      |

#### 6.4.8 Community

| Element           | Type        | Default | Description                                     |
|-------------------|-------------|---------|-------------------------------------------------|
| `CommunityRating` | `Rating`    | (none)  | Community rating (0.0-5.0, single decimal)      |
| `Review`          | `xs:string` | `""`    | Review text                                     |
| `ScanInformation` | `xs:string` | `""`    | Information about the scan/digitization process |

#### 6.4.9 File Metadata

| Element            | Type        | Default | Description                               |
|--------------------|-------------|---------|-------------------------------------------|
| `PageCount`        | `xs:int`    | `0`     | Number of pages in the archive            |
| `FileSize`         | `xs:int`    | `""`    | Total size of image files in bytes        |
| `FileCreationTime` | `xs:string` | `""`    | Archive creation timestamp (ISO 8601)     |
| `FileModifiedTime` | `xs:string` | `""`    | Archive modification timestamp (ISO 8601) |
| `Added`            | `xs:string` | `""`    | Date added to library                     |
| `Released`         | `xs:string` | `""`    | Release/publication date                  |

**Notes:**

- Timestamps SHOULD use ISO 8601 format: `YYYY-MM-DDThh:mm:ss.sssZ`
- `PageCount` MUST match the actual number of image files in the archive.
- `FileSize` represents the total uncompressed size of all image files, NOT the archive size.

#### 6.4.10 Custom Data

| Element             | Type        | Default | Description                                      |
|---------------------|-------------|---------|--------------------------------------------------|
| `CustomValuesStore` | `xs:string` | `""`    | Application-specific custom data (opaque string) |

### 6.5 Format Enumeration

The `Format` element accepts any string value, but the following are the recognized standard values:

```
Annotation, Annual, Anthology, Black & White, Box-Set, Crossover,
Director's Cut, Epilogue, Event, FCBD, Flyer, Giant-Size, Graphic Novel,
Hard-Cover, King-Size, Limited Series, Magazine, NSFW, One-Shot, Point 1,
Preview, Prologue, Reference, Review, Reviewed, Scanlation, Script,
Series, Sketch, Special, Trade Paper Back, Web Comic, Year One
```

Readers SHOULD accept these values case-insensitively. Alternative spellings exist in the wild (e.g., "TPB" for "Trade Paper Back", "WebComic" for "Web Comic") and readers SHOULD handle them gracefully.

### 6.6 Manga Enumeration

| Value               | Description                                         |
|---------------------|-----------------------------------------------------|
| `Unknown`           | Reading direction not specified                     |
| `No`                | Western-style left-to-right reading                 |
| `Yes`               | Manga-style (may be left-to-right or right-to-left) |
| `YesAndRightToLeft` | Manga with explicit right-to-left reading order     |

Readers SHOULD use this value to determine the reading direction for page navigation and double-page spread orientation.

### 6.7 AgeRating Enumeration

| Value             | Description                      |
|-------------------|----------------------------------|
| `Unknown`         | Not rated                        |
| `Adults Only 18+` | Adult content only               |
| `Early Childhood` | Suitable for very young children |
| `Everyone`        | Suitable for all ages            |
| `Everyone 10+`    | Suitable for ages 10 and up      |
| `G`               | General audiences                |
| `Kids to Adults`  | Suitable for children to adults  |
| `M`               | Mature content                   |
| `MA15+`           | Mature audiences 15+             |
| `Mature 17+`      | Mature audiences 17+             |
| `PG`              | Parental guidance suggested      |
| `R18+`            | Restricted 18+                   |
| `Rating Pending`  | Rating has not been assigned     |
| `Teen`            | Suitable for teens               |
| `X18+`            | Explicit content 18+             |

### 6.8 Rating Type

The `CommunityRating` element uses a decimal type:

- Minimum value: `0.0`
- Maximum value: `5.0`
- Precision: 1 decimal place (schema v2.1) or 2 decimal places (schema v2.0)

### 6.9 Pages Element

The `<Pages>` element contains an ordered list of `<Page>` elements describing each page in the archive.

```xml

<Pages>
    <Page Image="0" Type="FrontCover" ImageSize="245760" ImageWidth="800" ImageHeight="1200"/>
    <Page Image="1" Type="Story" DoublePage="false" ImageSize="198432" ImageWidth="800" ImageHeight="1200"/>
    <Page Image="2" Type="BackCover" ImageSize="210944" ImageWidth="800" ImageHeight="1200"/>
</Pages>
```

#### 6.9.1 Page Attributes

| Attribute     | Type            | Required | Default | Description                                          |
|---------------|-----------------|----------|---------|------------------------------------------------------|
| `Image`       | `xs:int`        | **YES**  | -       | Zero-based index of the page in the sorted file list |
| `Type`        | `ComicPageType` | No       | `Story` | Type/role of the page                                |
| `DoublePage`  | `xs:boolean`    | No       | `false` | Whether this is a double-page spread                 |
| `ImageSize`   | `xs:long`       | No       | `0`     | Image file size in bytes                             |
| `Key`         | `xs:string`     | No       | `""`    | Unique key for the page                              |
| `Bookmark`    | `xs:string`     | No       | `""`    | Bookmark/chapter name for this page                  |
| `ImageWidth`  | `xs:int`        | No       | `-1`    | Image width in pixels                                |
| `ImageHeight` | `xs:int`        | No       | `-1`    | Image height in pixels                               |

**Notes:**

- `Image` is the ONLY required attribute. It MUST be a zero-based index corresponding to the page's position in the alphabetically-sorted list of image files.
- `Bookmark` was added in schema v2.0.
- Readers SHOULD use actual image dimensions from the file rather than relying solely on `ImageWidth`/`ImageHeight` metadata.

#### 6.9.2 ComicPageType Enumeration

| Value           | Description                                |
|-----------------|--------------------------------------------|
| `FrontCover`    | Front cover image                          |
| `InnerCover`    | Inner cover or dust jacket                 |
| `Roundup`       | Recap or summary page                      |
| `Story`         | Regular story page (default)               |
| `Advertisement` | Advertisement page                         |
| `Editorial`     | Editorial or credits page                  |
| `Letters`       | Letters to the editor page                 |
| `Preview`       | Preview of upcoming issues                 |
| `BackCover`     | Back cover image                           |
| `Other`         | Other content not fitting above categories |
| `Deleted`       | Page marked for deletion (not displayed)   |

**Notes:**

- The `FrontCover` page is typically used by readers as the thumbnail/cover image for the comic.
- Pages of type `Deleted` SHOULD NOT be displayed to the user but MAY be retained in the archive.

## 7. Schema Evolution

### 7.1 Version History

| Version | Key Changes                                                                                                                                                                                                                                                                                                         |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1.0** | Initial schema. Core metadata fields, basic page info. `Manga` typed as `YesNo`. No `Bookmark`, `Tags`, `Translator`, `StoryArcNumber`, `AgeRating`, `CommunityRating`, `MainCharacterOrTeam`, `Review`, `Added`, `Released`, `FileSize`, `FileModifiedTime`, `FileCreationTime`, `BookPrice`, `CustomValuesStore`. |
| **2.0** | Added `Characters`, `Teams`, `Locations`, `ScanInformation`, `StoryArc`, `SeriesGroup`, `AgeRating`, `CommunityRating`, `MainCharacterOrTeam`, `Review`. `Manga` gets its own type with `YesAndRightToLeft`. `Bookmark` added to pages. `Rating` type has 2 decimal places.                                         |
| **2.1** | Added `Translator`, `Tags`, `StoryArcNumber`, `Added`, `Released`, `FileSize`, `FileModifiedTime`, `FileCreationTime`, `BookPrice`, `CustomValuesStore`. `Rating` precision reduced to 1 decimal place. `Day` field added to date.                                                                                  |

### 7.2 Compatibility Guidelines

1. Writers SHOULD generate metadata conforming to the latest schema version (2.1).
2. Readers MUST gracefully handle unknown elements by ignoring them (forward compatibility).
3. Readers MUST handle missing optional elements by using specified defaults (backward compatibility).
4. Writers SHOULD NOT include elements with default/empty values to minimize file size.

## 8. Related Formats

### 8.1 CBR (Comic Book RAR)

- Extension: `.cbr`
- MIME Type: `application/vnd.comicbook-rar`
- Identical internal structure but using RAR archive format instead of ZIP.
- Requires external RAR extraction tools (e.g., `unrar`, `7zip`).
- CBZ is RECOMMENDED over CBR for new archives due to the ubiquity of ZIP support.

### 8.2 CB7 (Comic Book 7z)

- Extension: `.cb7`
- MIME Type: `application/x-cb7`
- Uses 7-Zip archive format. Less common.

### 8.3 CBT (Comic Book TAR)

- Extension: `.cbt`
- MIME Type: `application/x-cbt`
- Uses TAR archive format. No compression. Rare.

### 8.4 PDF

- PDF files can contain embedded images and are sometimes used for digital comics.
- PDF does not natively support ComicInfo metadata.
- Conversion from PDF to CBZ involves extracting images; metadata must be added separately.

## 9. Implementation Considerations

### 9.1 Reading a CBZ File

A conforming reader MUST implement the following algorithm:

1. Open the file as a ZIP archive.
2. List all entries and sort them alphabetically (case-insensitive).
3. Check for `ComicInfo.xml` at the root level:
   - If present, parse it and extract metadata.
   - If absent or malformed, proceed with image-only mode.
4. Filter entries to include only files with supported image extensions.
5. Ignore directories, hidden files (starting with `.`), and OS-specific metadata folders (e.g., `__MACOSX/`).
6. Load images in sorted order as the page sequence.
7. If `ComicInfo.xml` contains a `<Pages>` section, use the `Image` attribute to map metadata to pages.

### 9.2 Writing a CBZ File

A conforming writer MUST implement the following:

1. Create a new ZIP archive with `ZIP_STORED` compression (RECOMMENDED).
2. Add `ComicInfo.xml` as the first entry (RECOMMENDED for fast metadata access).
3. Add image files in reading order with sequential, zero-padded names.
4. Ensure `PageCount` matches the number of image files.
5. Set `Image` attributes in `<Page>` elements as zero-based indices matching the sorted file order.
6. Use UTF-8 encoding for the XML file.
7. Self-close `<Page>` elements: use `<Page ... />` not `<Page ...></Page>`.

### 9.3 Character Encoding

1. `ComicInfo.xml` MUST use UTF-8 encoding.
2. File names within the archive SHOULD use UTF-8 encoding.
3. All text content in metadata fields MUST be valid UTF-8.

### 9.4 Error Handling

1. Readers SHOULD be lenient in parsing: accept minor deviations from the schema.
2. Unknown XML elements SHOULD be silently ignored.
3. Malformed `ComicInfo.xml` SHOULD NOT prevent reading the images.
4. Unsupported image formats SHOULD be skipped with a warning.

## 10. Security Considerations

1. Readers MUST validate ZIP entries to prevent path traversal attacks (e.g., entries with `../` in their names).
2. Readers SHOULD impose reasonable limits on image dimensions and file sizes to prevent resource exhaustion.
3. Readers MUST NOT execute any content from the archive, even if it appears to be a script or executable.
4. `CustomValuesStore` content MUST be treated as opaque and untrusted.
5. URLs in the `Web` field SHOULD NOT be automatically fetched without user consent.

## 11. Complete Example

### 11.1 Minimal ComicInfo.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Title>Example Issue #1</Title>
    <Series>Example Series</Series>
    <Number>1</Number>
    <PageCount>3</PageCount>
    <Pages>
        <Page Image="0" Type="FrontCover"/>
        <Page Image="1" Type="Story"/>
        <Page Image="2" Type="BackCover"/>
    </Pages>
</ComicInfo>
```

### 11.2 Full ComicInfo.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Title>The Amazing Adventure #1</Title>
    <Series>The Amazing Adventure</Series>
    <Number>1</Number>
    <Count>12</Count>
    <Volume>1</Volume>
    <Summary>The hero embarks on an incredible journey through uncharted territory.</Summary>
    <Notes>Scanned from first printing</Notes>
    <Year>2024</Year>
    <Month>6</Month>
    <Day>15</Day>
    <Writer>Jane Smith</Writer>
    <Penciller>John Doe</Penciller>
    <Inker>John Doe</Inker>
    <Colorist>Alice Johnson</Colorist>
    <Letterer>Bob Williams</Letterer>
    <CoverArtist>John Doe</CoverArtist>
    <Editor>Carol Brown</Editor>
    <Translator>Pierre Dupont</Translator>
    <Publisher>Example Comics</Publisher>
    <Imprint>Example Prestige</Imprint>
    <Genre>Adventure, Fantasy</Genre>
    <Tags>hero, quest, dragons</Tags>
    <Web>https://example.com/amazing-adventure-1</Web>
    <Format>Series</Format>
    <EAN>9781234567890</EAN>
    <BlackAndWhite>No</BlackAndWhite>
    <Manga>No</Manga>
    <Characters>Hero, Sidekick, Villain</Characters>
    <Teams>The Adventurers</Teams>
    <Locations>The Kingdom, Dragon Mountain</Locations>
    <ScanInformation>600dpi scan, cleaned and leveled</ScanInformation>
    <StoryArc>The Dragon Wars</StoryArc>
    <StoryArcNumber>1</StoryArcNumber>
    <SeriesGroup>Example Universe</SeriesGroup>
    <AgeRating>Teen</AgeRating>
    <CommunityRating>4.5</CommunityRating>
    <MainCharacterOrTeam>Hero</MainCharacterOrTeam>
    <Review>Excellent start to a new series</Review>
    <LanguageISO>en</LanguageISO>
    <Added>2024-06-20T10:30:00.000Z</Added>
    <Released>2024-06-15T00:00:00.000Z</Released>
    <FileSize>15728640</FileSize>
    <FileCreationTime>2024-06-20T10:30:00.000Z</FileCreationTime>
    <FileModifiedTime>2024-06-20T10:30:00.000Z</FileModifiedTime>
    <PageCount>24</PageCount>
    <Pages>
        <Page Image="0" Type="FrontCover" ImageSize="524288" ImageWidth="1600" ImageHeight="2400" Bookmark="Cover"/>
        <Page Image="1" Type="Story" ImageSize="491520" ImageWidth="1600" ImageHeight="2400" Bookmark="Chapter 1"/>
        <Page Image="2" Type="Story" DoublePage="true" ImageSize="983040" ImageWidth="3200" ImageHeight="2400"/>
        <!-- ... pages 3-22 ... -->
        <Page Image="23" Type="BackCover" ImageSize="458752" ImageWidth="1600" ImageHeight="2400"/>
    </Pages>
</ComicInfo>
```

## 12. XSD Schema Reference (v2.1)

The normative XML Schema Definition for version 2.1 is provided in `docs/schema/v2.1/ComicInfo.xsd`.

Key type definitions:

```xml
<!-- YesNo enumeration -->
<xs:simpleType name="YesNo">
    <xs:restriction base="xs:string">
        <xs:enumeration value="Unknown"/>
        <xs:enumeration value="No"/>
        <xs:enumeration value="Yes"/>
    </xs:restriction>
</xs:simpleType>

        <!-- Manga enumeration -->
<xs:simpleType name="Manga">
<xs:restriction base="xs:string">
    <xs:enumeration value="Unknown"/>
    <xs:enumeration value="No"/>
    <xs:enumeration value="Yes"/>
    <xs:enumeration value="YesAndRightToLeft"/>
</xs:restriction>
</xs:simpleType>

        <!-- Rating type (0.0 to 5.0) -->
<xs:simpleType name="Rating">
<xs:restriction base="xs:decimal">
    <xs:minInclusive value="0"/>
    <xs:maxInclusive value="5"/>
    <xs:fractionDigits value="1"/>
</xs:restriction>
</xs:simpleType>

        <!-- Page type enumeration -->
<xs:simpleType name="ComicPageType">
<xs:list>
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="FrontCover"/>
            <xs:enumeration value="InnerCover"/>
            <xs:enumeration value="Roundup"/>
            <xs:enumeration value="Story"/>
            <xs:enumeration value="Advertisement"/>
            <xs:enumeration value="Editorial"/>
            <xs:enumeration value="Letters"/>
            <xs:enumeration value="Preview"/>
            <xs:enumeration value="BackCover"/>
            <xs:enumeration value="Other"/>
            <xs:enumeration value="Deleted"/>
        </xs:restriction>
    </xs:simpleType>
</xs:list>
</xs:simpleType>
```

## 13. References

- **PKWARE ZIP Application Note** - ZIP file format specification
- **ComicRack** - Original creator of the ComicInfo.xml format
- **anansi-project** - Community maintenance of the ComicInfo schema (https://anansi-project.github.io)
- **RFC 2119** - Key words for use in RFCs
- **ISO 639** - Language code standards
- **ISO 8601** - Date and time format

## 14. Acknowledgments

This specification was compiled from the collective work of the comic book reader community, including the original ComicRack application by cYo Soft, the anansi-project contributors, and the numerous developers who have implemented CBZ support in their applications.

---

*This document is provided as-is for informational purposes. The CBZ format is a community standard without a formal standards body. Implementers should prioritize interoperability with existing tools over strict schema conformance.*
