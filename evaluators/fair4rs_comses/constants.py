SOFTWARE_REGISTRIES =  [
    'https://www.comses.net/',      # CoMSES model library
    'https://csdms.colorado.edu/',  # CSDMS model repo
    'https://www.hydroshare.org/'       # HydroShare
]   

# Recommended highly permissive licenses
PERMISSIVE_LICENSES = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "CC0-1.0",
    "Unlicense",
    "Creative Commons Attribution CC BY"
]

# Less permissive but widely used licenses
RESTRICTIVE_LICENSES = [
    "EPL-2.0",
    "MPL-2.0",
    "GPL-3.0",
    "LGPL-3.0",
]

COMSES_APPROVED_LICENSES = [
    "BSD or MIT X11",
    "CPL",
    "GPL v3",
    "LGPL",
]

# Combined list of acceptable open-source licenses
APPROVED_LICENSES = PERMISSIVE_LICENSES + RESTRICTIVE_LICENSES + COMSES_APPROVED_LICENSES

# Community defined standards for data exchanged
ACCEPTED_DATA_FORMATS = [
    "csv", 
    "json", 
    "xml", 
    "netcdf", 
    "hdf5", 
    "yaml", 
    "geojson",
    "txt"
    ]

# Add keywords for API links
API_KEYWORDS = [
    "api", 
    "swagger", 
    "openapi", 
    "endpoint", 
    "rest", 
    "graphql"
    ]

# Add FAIR-aligned repositories
ACCEPTED_FAIR_REPOSITORIES = [
    'Zenodo',
    'HydroShare',
    'IEDA',
    ]

# Add software repositories
ACCEPTED_SOFTWARE_REPOSITORIES = [
    'https://github.com',
    'https://gitlab.com'
    ]
