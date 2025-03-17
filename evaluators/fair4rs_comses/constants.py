SOFTWARE_REGISTRIES =  [
    'https://www.comses.net/',      # CoMSES model library
    'https://csdms.colorado.edu/',  # CSDMS model repo
    'https://hydroshare.org/'       # HydroShare
]   

# Recommended highly permissive licenses
PERMISSIVE_LICENSES = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "CC0-1.0",
    "Unlicense"
]

# Less permissive but widely used licenses
RESTRICTIVE_LICENSES = [
    "EPL-2.0",
    "MPL-2.0",
    "GPL-3.0",
    "LGPL-3.0"
]

# Combined list of acceptable open-source licenses
APPROVED_LICENSES = PERMISSIVE_LICENSES + RESTRICTIVE_LICENSES