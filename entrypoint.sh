#!/bin/sh
current_date_time=$(date +'%Y-%m-%d_%H-%M-%S')
scrapy crawl rongbay -O "/app/data/${current_date_time}_rongbay_output.json"