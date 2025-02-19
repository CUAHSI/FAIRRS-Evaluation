# CodeMeta Properties

The following table is based on the [CodeMeta](https://codemeta.github.io/terms/) terms. We have added a Notes column to explain why certain properties were excluded from our project.

| Property                 | Type                     | Description | Notes |
|--------------------------|--------------------------|-------------|-------------|
| `address`               | PostalAddress or Text    | Physical address of the item. | |
| `affiliation`           | Organization             | An organization that this person is affiliated with. For example, a school/university. | |
| `applicationCategory`    | Text or URL              | Type of software application, e.g., 'Game, Multimedia'. | |
| `applicationSubCategory` | Text or URL              | Subcategory of the application, e.g., 'Arcade Game'. | |
| `author`                | Organization or Person   | The author of this content or rating. Note that 'author' is special in that HTML5 provides a special mechanism for indicating authorship via the 'rel' tag, which is equivalent to this and may be used interchangeably. | |
| `buildInstructions`      | URL                      | Link to installation instructions/documentation. | |
| `citation`              | CreativeWork or URL      | A citation or reference to another creative work, such as another publication, web page, scholarly article, etc. | |
| `codeRepository`        | URL                      | Link to the repository where the uncompiled, human-readable code and related code is located (e.g., SVN, GitHub, CodePlex, institutional GitLab instance). | |
| ~~`contIntegration`~~    | ~~URL~~                  | ~~Link to continuous integration service.~~ | Similar to `developmentStatus`, so only `developmentStatus` is kept. |
| `contributor`           | Organization or Person   | A secondary contributor to the CreativeWork or Event. | |
| `copyrightHolder`       | Organization or Person   | The party holding the legal copyright to the CreativeWork. | |
| `copyrightYear`         | Number                   | The year during which the claimed copyright for the CreativeWork was first asserted. | |
| `dateCreated`           | Date                     | The date on which the CreativeWork was created or the item was added to a DataFeed. | |
| `dateModified`          | Date                     | The date on which the CreativeWork was most recently modified or when the item's entry was modified within a DataFeed. | |
| `datePublished`         | Date                     | Date of first broadcast/publication. | |
| `description`           | Text                     | A description of the item. | |
| `developmentStatus`     | Text                     | Description of development status, e.g., Active, inactive, suspended. See repostatus.org. | |
| `downloadUrl`          | URL                      | If the file can be downloaded, URL to download the binary. | |
| `editor`               | Person                   | Specifies the Person who edited the CreativeWork. | |
| `email`                | Text                     | Email address. | |
| ~~`embargoDate`~~       | ~~Date~~                 | ~~Software may be embargoed from public access until a specified date (e.g., pending publication, 1 year from publication).~~ | Not considered for this project. |
| `encoding`             | MediaObject              | A media object that encodes this CreativeWork. This property is a synonym for associatedMedia. Supersedes 'encodings'. | |
| `endDate`              | Date or Datetime         | The end date and time of the item. | |
| ~~`familyName`~~       | ~~Text~~                 | ~~Family name. In the U.S., the last name of a Person.~~ | Not considered for this project. |
| ~~`fileFormat`~~       | ~~Text or URL~~          | ~~Media type, typically MIME format (see IANA site) of the content.~~ | Superseded by `encodingFormat`, so only `encodingFormat` is kept. |
| `fileSize`             | Text                     | Size of the application/package (e.g., '18MB'). | |
| `funder`               | Organization or Person   | A person or organization that supports (sponsors) something through some kind of financial contribution. | |
| `funding`              | Text                     | Funding source (e.g., specific grant). | |
| ~~`givenName`~~       | ~~Text~~                 | ~~Given name. In the U.S., the first name of a Person.~~ | Not considered for this project. |
| `hasPart`              | CreativeWork             | Indicates a CreativeWork that is (in some sense) a part of this CreativeWork. Reverse property: 'isPartOf'. | |
| ~~`hasSourceCode`~~     | ~~SoftwareSourceCode~~   | ~~Link that states where the software code is for a given software.~~ | Similar to `codeRepository`, applies more to `SoftwareApplication`, and is excluded for this project. |
| `identifier`           | PropertyValue or URL     | The identifier property represents any kind of identifier for any kind of Thing. | |
| `installUrl`           | URL                      | URL at which the app may be installed, if different from the URL of the item. | |
| `isAccessibleForFree`  | Boolean                  | A flag to signal that the publication is accessible for free. | |
| `isPartOf`             | CreativeWork             | Indicates a CreativeWork that this CreativeWork is (in some sense) part of. | |
| `isSourceCodeOf`       | SoftwareApplication      | Link that states where software application is built from a given source code. | |
| `issueTracker`         | URL                      | Link to software bug reporting or issue tracking system. | |
| `keywords`             | Text                     | Keywords or tags used to describe this content. | |
| `license`              | CreativeWork or URL      | A license document that applies to this content. | |
| `maintainer`           | Person                   | Individual responsible for maintaining the software. | |
| `memoryRequirements`   | Text or URL              | Minimum memory requirements. | |
| `name`                 | Text                     | The name of an item (e.g., software, organization). | |
| `operatingSystem`      | Text                     | Operating systems supported (e.g., 'Windows 7', 'OSX 10.6'). | |
| `permissions`          | Text                     | Permission(s) required to run the app. | |
| ~~`position`~~         | ~~Integer or Text~~      | ~~The position of an item in a series or sequence of items.~~ | Not considered for this project. |
| `processorRequirements` | Text                    | Processor architecture required to run the application. | |
| `producer`             | Organization or Person   | The person or organization who produced the work. | |
| `programmingLanguage`  | ComputerLanguage or Text | The computer programming language. | |
| `provider`             | Organization or Person   | The service provider or producer. | |
| `publisher`            | Organization or Person   | The publisher of the creative work. | |
| `readme`              | URL                      | Link to software Readme file. | |
| `referencePublication` | ScholarlyArticle        | An academic publication related to the software. | |
| `relatedLink`          | URL                      | A link related to this object. | |
| ~~`roleName`~~         | ~~Text~~                 | ~~Name of the role played in an entity.~~ | Not considered for this project. |
| ~~`runtimePlatform`~~  | ~~Text~~                 | ~~Runtime platform or script interpreter dependencies.~~ | Similar to `softwareRequirements`, so only `softwareRequirements` is kept. |
| `sameAs`               | URL                      | URL of a reference Web page that unambiguously indicates the item's identity. | |
| ~~`softwareSuggestions`~~ | ~~SoftwareSourceCode~~ | ~~Optional dependencies, e.g., for optional features, code development.~~ | Excluded for this project. |
| `softwareRequirements`  | SoftwareSourceCode       | Required software dependencies. | |
| `softwareVersion`       | Text                     | Version of the software instance. | |
| `sponsor`              | Organization or Person   | A person or organization that supports a thing through a financial contribution. | |
| `startDate`           | Date or Datetime         | The start date and time of the item. | |
| `storageRequirements`   | Text or URL              | Storage requirements (free space required). | |
| `supportingData`        | DataFeed                 | Supporting data for a SoftwareApplication. | |
| `targetProduct`         | SoftwareApplication      | Target Operating System / Product to which the code applies. | |
| `url`                 | URL                      | URL of the item. | |
