# Installation

### Dependencies
Requires Python 3.8+ or later

```bash
pip install Scrapy
```

### Run
in root directory of project

```bash
scrapy crawl rongbay -o output.json
```

or use Docker
```bash
docker build -t rongbay .
docker run --name rongbay_c1 rongbay
```