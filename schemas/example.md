This is an example of a research model expressed using CodeMeta. This also follows the guidelines established by CUAHSI at https://github.com/CUAHSI/catalog/blob/develop/schema/core.md. 

The following is a CodeMeta representation of the TOPMODEL program that has a landing page located in the CSDMS model repository: https://csdms.colorado.edu/wiki/Model:TOPMODEL


```json
{
  "@type": "CreativeWork",
  "name": "TOPMODEL",
  "description": "TOPMODEL is a physically based, distributed watershed model that simulates hydrologic fluxes of water (infiltration-excess overland flow, saturation overland flow, infiltration, exfiltration, subsurface flow, evapotranspiration, and channel routing) through a watershed. The model simulates explicit groundwater/surface water interactions by predicting the movement of the water table, which determines where saturated land-surface areas develop and have the potential to produce saturation overland flow.",
  "identifier": "https://csdms.colorado.edu/wiki/Model:TOPMODEL",
  "keywords": ["basin", "hydrological"], 
  "developmentStatus": "Active",

  "creator":{
    "@type": "Organization",
    "name": "CSDMS Integration Facility",
    "email": "CSDMS@colorado.edu",
    "url": "https://csdms.github.io/help-desk"
    "address": "4001 Discovery Dr. Office N141C, Boulder, CO 80303 USA",
    "phone": "+44 (0)1524 593892"
  },
  "hasSourceCode": {
    "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
    "@type": "SoftwareSourceCode",
    "name": "TOPMODEL",
    "description": "Physically based, distributed watershed model that simulates hydrologic fluxes of water through a watershed".,
    "programmingLanguage": "R",
    "fileFormat": "application/zip",
    "installUrl": "https://cran.r-project.org/package=topmodel",
    "url": "https://cran.r-project.org/package=topmodel",
    "operatingSystem": "Windows",
    "author": {
      "@type": "Keith Beven",
      "name": "K.Beven@lancaster.ac.uk",
      "email": "jane.doe@example.com"
      "affiliation": {
        "@type": "Organization",
        "name": "Lancaster University, Department of Environmental Science, Institute of Environmental and Natural Sciences",
        "phone": "+44 (0)1524 593892"
      },
    },
    "supportingData": {
    "@type": "DataFeed",
    "distribution": {
      "@type": "DataDownload",
      "contentUrl": "https://csdms.colorado.edu/csdms_wiki/images/TOPMODEL_Example.zip"
    }
  },
  "referencePublication": [
      {
        "@type": "ScholarlyArticle",
      },
      {
        "@type": "ScholarlyArticle",
      },
      {
       "@type": "ScholarlyArticle",
      }
    ]
  }
}

```
