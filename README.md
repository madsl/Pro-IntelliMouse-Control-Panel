# intellimouse-ctl
![black](https://img.shields.io/badge/code%20style-black-000000.svg)
![pylint](https://img.shields.io/badge/linter-pylint-00D000.svg)
---
A cross-platform command line tool and library for Microsoft's IntelliMouse devices.

It supports the following models:
* Pro IntelliMouse (2019)
* Classic IntelliMouse (2017)

## Usage
### CLI
![intellimouse-ctl demo](https://user-images.githubusercontent.com/13816979/155191134-e2c7222f-0395-48af-824a-92003c9dadfc.gif)

```bash
intellimouse-ctl --help
usage: intellimouse-ctl [-h] [--json] {get,set,list} ...

positional arguments:
  {get,set,list}
    get           get the value of a setting
    set           set the value of a setting
    list          lists the connected devices and their indices

options:
  -h, --help      show this help message and exit
  --json          output JSON
```
Commands passed to a device that doesn't support the given commands will ignore them.
### Library
```python
from intellimouse import ClassicIntelliMouse
from intellimouse import ProIntelliMouse

with ClassicIntelliMouse.enumerate()[0] as mouse:
    print(mouse)


with ProIntelliMouse.enumerate()[0] as mouse:
    print(mouse)
```

## Features

### Pro IntelliMouse
- [x] DPI
- [x] LOD
- [x] LED
- [x] Polling Rate
- [ ] Custom Button Mapping
- [ ] Custom LOD Calibration

### Classic IntelliMouse
- [x] DPI
- [ ] Custom Button Mapping

## Install

### PyPI
```bash
pip install intellimouse-ctl
```

### Local
```bash
git clone https://github.com/k-visscher/intellimouse-ctl.git
cd intellimouse-ctl
pip install .
```

## Development
To set up a virtual environment to further develop this tool/library, use the following commands:
```bash
python -m venv venv
source venv/bin/activate
pip install --editable .
```

## Documentation

### View
```bash
pdoc ./src/intellimouse/
```

### Generate
```bash
pdoc ./src/intellimouse/ -o ./docs
```

## Sponsors
* [@madsl](https://github.com/madsl) for donating the Classic IntelliMouse to this project.

## License
This application is licensed under the the [MIT license](./LICENSE).

## Disclaimer
All company, product and service names used in this project are for identification purposes only.<br/>
Use of these names, trademarks and brands does not imply endorsement.<br/>
In no way is this project published by, affiliated with, or sponsorsed, or endorsed, or approved by Microsoft.<br/>

All product names, trademarks and registered trademarks are property of their respective owners.<br/>
Microsoft Pro IntelliMouse is a registered trademark or trademark of Microsoft Corporation in the United States and/or other countries.<br/>
Microsoft Classic IntelliMouse is a registered trademark or trademark of Microsoft Corporation in the United States and/or other countries.<br/>
All other trademarks cited herein are the property of their respective owners.
