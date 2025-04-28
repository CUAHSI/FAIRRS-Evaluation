# Codemeta and CSDMS Crosswalks

The following table presents a crosswalk between [CodeMeta](https://codemeta.github.io/terms/) terms and the [CSDMS model metadata](https://csdms.colorado.edu/wiki/Available_model_questionnaire_conditions), primarily based on Leslie Hsu's [previous work](https://github.com/hsu000001/codemeta/blob/csdms/crosswalks/csdms.csv) in mapping this alignment. 

**Table 1. CSDMS metadata associated with Codemeta properties.**
| Property            | CSDMS Model Metadata                                    | Short Description | Notes |
|---------------------|--------------------------------------------------|------------------|--------|
| `address`           | `Postal address1` and/or `Postal address2`  | Provides the address of the contact person, including any additional address details. |
| `affiliation`       | `Institute` | Affiliated institute of contact person |
| `applicationCategory` | `Model Type`? | Describe if a model is more like a tool, build out of multiple modules or is just a single model. |
| `applicationSubCategory` |  |  | Not found|
| `author`           | `First name` && `Last name` | Given name and family name of contact person |
| `buildInstructions` |  |  | Not found. Possibly inferred from `Model manual`|
| `citation`         |  |  | Not found. However, the [examples](https://github.com/CUAHSI/FAIRRS-Evaluation/blob/develop/schemas/csdms/raw_model_metadata/WBM-WTM.json) include `Citations`, which appears to relate to the number of times the model's source code has been cited. This differs from the definition that we have in the [codemeta_properties.md](https://github.com/CUAHSI/FAIRRS-Evaluation/blob/develop/schemas/codemeta_properties.md). |
| `codeRepository`   | `Source web address` | URL to source code from which it can be downloaded | Similar to `downloadUrl` |
| ~~`contIntegration`~~  |  |  | Not considered in our project|
| `contributor`      | `Current future collaborators` and\or `Current future collaborators` | Indicates current or future collaboration plans with other researchers, including any additional anticipated partnerships. |
| `copyrightHolder`  |        |  | Not found|
| `copyrightYear`    |      |  | Not found|
| `dateCreated`    | `Start year development` | The first year the model was developed |
| `dateModified`   | `End year development` | The year model development ended |
| `datePublished`  |  |  | Not found.|
| `description`    | `One-line model description` and\or `Extended model description` | Short and extended description of the model |
| `developmentStatus` | `Development still active` | Indicates if model development is still ongoing |
| `downloadUrl`    | `Source web address` and/or `Source csdms web address` | Provides the URL where the source code can be downloaded, including links to both external repositories and the CSDMS-hosted source code. |  |
| `editor`      |     |  | Not found.|
| `email`       | `Email address` | Email address of contact person |
| ~~`embargoDate`~~ |     |  | Not considered in our project|
| `encoding`    | `Input format model` and/or `Input format model other` and/or `Output format model` and/or `Output format model other` | Describes the input and output formats supported by the model, including any alternative formats that may be used. | Should this refer to the encoding of the source code itself, or to that of its inputs and outputs?|
| `endDate`     |     |  | Similar to the `dateModified` for which `End year development` is used.|
| ~~`familyName`~~  |  |  | Not considered in our project|
| ~~`fileFormat`~~  |    |  | Not considered in our project|
| `fileSize`    |      |  | Not found.|
| `funder`      |  |  | Not found.|
| `funding`     |     |  | Not found.|
| ~~`givenName`~~         |    |  | Not considered in our project|
| `hasPart`          | `Incorporated modules` and/or `Animation model name` | Indicates the names of modules or components incorporated by the model and, if applicable, identifies other modules with which the model can be coupled. | An example can be found for [WRF-Hydro](https://github.com/CUAHSI/FAIRRS-Evaluation/blob/develop/schemas/csdms/raw_model_metadata/WRF-Hydro.json)|
| `identifier`       | `DOI model` or `DOI-filelink` | Provides DOI information for the model's source code and includes a DOI link corresponding to the specific released version. |
| `installUrl`       |  |  | This could be same as the `codeRepository`, `downloadUrl`, or `url` |
| `isAccessibleForFree` | `Model availability`? | How the model is made available to the community |
| `isPartOf`        | `ModelFramework` | Describe the model framework, if the model is part of a larger framework. |
| `issueTracker`      |    |  | Not found.|
| `keywords`          | `ModelKeywords` and\or `ModelDomain` and\or `IncorporatedModules` | Provides keywords describing the model, the domains it simulates (e.g., marine, terrestrial, hydrological), and the names of any modules or components it incorporates. |
| `license`          | `Program license type` | Source code license |
| `maintainer`       |      |  | Not found.|
| `memoryRequirements` | `Memory requirements` | Memory requirements to run model |
| `name`             | `Model also known as` | Additional field to hold an alternative name for a model, for if the model is also known under an other name. | [CSDMS metadata](https://csdms.colorado.edu/wiki/Available_model_questionnaire_conditions) does not specifically present the model name. Leslie Hsu's [work](https://github.com/hsu000001/codemeta/blob/csdms/crosswalks/csdms.csv) identified *Model also known as* for `sameAs`, which is not correct as `sameAs` only accepts URL. | 
| `operatingSystem`   | `Supported platforms` and\or `Supported platforms other` | Indicates the computer platforms supported by the model (e.g., Mac, Windows) and specifies any additional platforms not covered by the standard options. |
| `permissions`       |  |  | Not found.|
| ~~`position`~~         |      |  | Not considered in our project.|
| `processorRequirements` | `Multiple processors implemented` and/or `Nr of distributed processors` and/or `Nr of shared processors` | Describes how the model utilizes multiple processors, including the implementation approach and the maximum number of distributed and shared processors it can support. |
| `producer`         |     |  | Not found.|
| `programmingLanguage` | `Programming language` and/or `Program language other` | Identifies the programming language used by the model and, if applicable, specifies any additional languages not covered under the standard programming language options. |
| `provider`         |    |  | Not found.|
| `publisher`        |  |  | Not found. Possibly CSDMS?|
| `readme`            |       |  | Not found.|
| `referencePublication` | Describe key physical parameters and equations | Describe key physical parameters and equations | Based on this [example](https://github.com/CUAHSI/FAIRRS-Evaluation/blob/develop/schemas/csdms/raw_model_metadata/HydroTrend.json) |
| `relatedLink`       | `Model forum` | URL to module forum/discussion board |
| `releaseNotes`      |      |  | Not found.|
| ~~`roleName`~~         |     |  | Not considered in our project. |
| ~~`runtimePlatform`~~  |     |  | Not considered in our project.|
| `sameAs`            | | | Not found.|
| `softwareHelp`      | `Manual model available` and/or `Model manual` | Indicates whether a model manual is available, and, if so, provides the option to upload the manual. |
| `softwareRequirements` | `Pre processing software` and/or `Describe pre-processing software` and\or `Post processing software` and/or `Describe post-processing software` and/or `Visualization software needed` and/or `Visualization software` and/or `Visualization software other` | Indicate whether pre-processing, post-processing, or visualization software is needed, and, if so, specifies which packages are used or recommended. |
| ~~`softwareSuggestions`~~ |   |  | Not considered in our project. |
| `softwareVersion`  | `DOI assigned to model version` | Version of model to which a DOI is assigned |
| `sponsor`          |    |   |  Not found. |
| `startDate`        |    |   |  Same as `dateCreated` |
| `storageRequirements` |    |   | Not found. |
| `supportingData`   | `Model calibration data` and/or `Describe available calibration data` and/or `Model test data` and/or `Describe available test data` and/or `Describe ideal data` | Indicates whether calibration or test data sets are available, and, if so, provides descriptions of the available calibration and test data, along with a description of the ideal data recommended for model evaluation. |
| `targetProduct`    |        |  | Not found. |
| `url`             | `Model website`  | URL of external model website | Leslie Hsu's [work](https://github.com/hsu000001/codemeta/blob/csdms/crosswalks/csdms.csv) used *Module website*, but that doesn't seem to be a term in the [CSDMS metadata](https://csdms.colorado.edu/wiki/Available_model_questionnaire_conditions)|
| ~~`version`~~         |  |  | Same as `softwareVersion`. Not considered in our project. |

---

These CSDMS metadata terms do not have direct equivalents in the current CodeMeta vocabulary. We recommend representing them using the `additionalProperty` to preserve their value. While SchemaOrg's `additionalProperty` can only accept a single `PropertyValue` (not a list), we can use the [`StructuredValue`](https://schema.org/StructuredValue) type from Schema.org to group multiple additional properties together in a structured and extensible way.

**Table 2. Proposed mapping for CSDMS metadata terms that do not directly map to existing CodeMeta**
| Property            | CSDMS Model Metadata                                    | Short Description | Notes |
|---------------------|--------------------------------------------------|------------------|--------|
| `additionalProperty` | `Additional comments model` | Field to include additional comments|
| `additionalProperty` | `Code reviewed or not` | If source code is reviewed through e.g. JOSS publication or not|
| `additionalProperty` | `Code openmi compliant or not` | If module is openmi compliant |
| `additionalProperty` | `Code_IRF_or_not` | If module is BMI compliant |
| `additionalProperty` | `Code_CMT_compliant_or_not` | If module is WMT compliant |
| `additionalProperty` | `Describe length scale and resolution` | Describe length scale and resolution constraints|
| `additionalProperty` | `Describe time scale and resolution` | Describe time scale and resolution constraints |
| `additionalProperty` | `Describe numerical limitations` | Describe any numerical limitations and issues |
| `additionalProperty` | `Code optimized` | Indicate if the model uses single or multiple processors |
| `additionalProperty` | `Spatial dimensions` | Range or specific spatial dimensions a model operates under (1D, 2D, etc). |
| `additionalProperty` | `Spatialscale` | Spatial extent of simulated domain |