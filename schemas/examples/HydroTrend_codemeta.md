The following is an example of a research model expressed using CodeMeta properties, as shown [here](https://github.com/CUAHSI/FAIRRS-Evaluation/blob/develop/schemas/codemeta_properties.md). It presents a **CodeMeta**- and **Schema.org**-based representation of the [HydroTrend](https://csdms.colorado.edu/wiki/Model:HydroTrend) model, which has a dedicated landing page in the CSDMS model repository.

```json
{
    "@context": [
        "https://doi.org/10.5063/schema/codemeta-2.0",
        "https://schema.org/"
    ],
    "@type": "SoftwareSourceCode",
    "applicationCategory": ["Terrestrial", "Hydrology"],
    "applicationSubCategory": "",
    "author": [
        {
        "@type": "Person",
        "affiliation": "Institute of Arctic and Alpine Research, University of Colorado Boulder",
        "email": "kettner@colorado.edu",
        "name": "Albert Kettner",
        "address": "4001 Discovery Drive, Boulder, CO, USA, 80309",
        "sameAs": "https://csdms.colorado.edu/wiki/User:WikiSysop"
        }
    ],
    "buildInstructions": "https://csdms.colorado.edu/pub/users/huttone/build_notes/BUILD_NOTES-hydrotrend-3.0.html",
    "citation": "Kettner, A.J., and Syvitski, J.P.M., 2008. HydroTrend version 3.0: a Climate-Driven Hydrological Transport Model that Simulates Discharge and Sediment Load leaving a River System. Computers & Geosciences, 34(10), 1170-1183",
    "codeRepository": "https://github.com/kettner/hydrotrend",
    "contributor": [
        {
        "@type": "Person",
        "affiliation": "University of Colorado Boulder",
        "name": "James Syvitski"
        }
    ],
    "copyrightHolder": "",
    "copyrightYear": "",
    "dateCreated": "2011",
    "dateModified": "2020",
    "datePublished": "",
    "description": "HydroTrend v.3.0 is a climate-driven hydrological water balance and transport model that simulates water discharge and sediment load at a river outlet.",
    "developmentStatus": "Active",
    "downloadUrl": "https://csdms.colorado.edu/pub/models/doi-source-code/hydrotrend-10.1594.IEDA.100135-3.0.2.tar.gz",
    "editor": "",
    "embargoDate": "",
    "encodingFormat": [
        "application/x-c",
        "text/plain",
        "application/octet-stream"
    ],
    "endDate": "",
    "fileSize": "",
    "funder": "",
    "funding": "",
    "hasPart": "",
    "identifier": [
        "https://csdms.colorado.edu/wiki/Model:HydroTrend",
        "https://doi.org/10.1594/IEDA/100135"
    ],
    "installUrl": "https://csdms.colorado.edu/pub/models/doi-source-code/hydrotrend-10.1594.IEDA.100135-3.0.2.tar.gz",
    "isAccessibleForFree": "",
    "isPartOf": "",
    "isSourceCodeOf": "",
    "issueTracker": "https://github.com/kettner/hydrotrend/issues",
    "keywords": ["basins", "Hydrological model", "Sediment Transport", "river", "hydrological", "transport"],
    "license": "GPL v2",
    "maintainer": "",
    "memoryRequirements": "1Gb at the most",
    "name": "HydroTrend",
    "operatingSystem": ["Unix", "Linux", "Mac OS", "Windows"],
    "permissions": "",
    "processorRequirements": "",
    "producer": "",
    "programmingLanguage": "C",
    "provider": "",
    "publisher": "",
    "readme": "https://csdms.colorado.edu/wiki/Model_help:HydroTrend",
    "referencePublication": "https://csdms.colorado.edu/wiki/HydroTrend-Publications",
    "relatedLink": ["https://anaconda.org/conda-forge/hydrotrend", "https://github.com/mdpiper/hydrotrend-docker"],
    "releaseNotes": "",
    "review": "",
    "reviewAspect": "",
    "reviewBody": "",
    "sameAs": "",
    "softwareHelp": "",
    "softwareRequirements": "",
    "softwareVersion": "3.0.2",
    "sponsor": "",
    "storageRequirements": [
        "Pre-processing software needed: No",
        "Post-processing software needed: No",
        "Visualization software needed: No"
    ],
    "supportingData": [
        {
            "@type": "DataFeed",
            "about": "Calibration Datasets",
            "author": "",
            "description": "Long term sediment routine",
            "url": "https://doi.org/10.1086/509246",
            "distribution": ""
        },
        {
            "@type": "DataFeed",
            "about": "Available Calibration Datasets",
            "author": "",
            "description": "Short term sediment routine",
            "url": "https://doi.org/10.1016/S0921-8181(03)00019-5",
            "distribution": ""
        },
        {
            "@type": "DataFeed",
            "about": "Available Test Datasets",
            "author": "",
            "description": "Water & sediment discharge of Eel river; Waipaoa river, Po River, Rhone River, Lanyang river, etc.",
            "url": "",
            "distribution": ""
        },
        {
            "@type": "DataFeed",
            "about": "Ideal data for testing",
            "author": "",
            "description": "Test data would be daily water and sediment discharges over many years together with climate data.",
            "url": "",
            "distribution": ""
        }
    ],
    "targetProduct": "",
    "url": "https://csdms.colorado.edu/wiki/Model:HydroTrend"
}
```