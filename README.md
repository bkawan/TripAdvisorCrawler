# TripAdvisorCrawler

# tripadvisor.py

### to save extracted data into json

$ scrapy crawl tripadvisor -o first_attraction_list_all_location.json

### to save extracted data into csv

$ scrapy crawl tripadvisor -o first_attraction_list_all_location.csv


# TripAdvisorAllLocation.py

### To extract all the location link into csv

$ scrapy crawl tripAllLocation -o all_location_link.csv

### To extract all the location link into json

$ scrapy crawl tripAllLocation -o all_location_link.json



# TripAdvisorAllLocationAllAttraction.py

### To extract all the location link into csv

$ scrapy crawl tripAllLocation -o all-attraction-list-only-first-pagi.csv

### To extract all the location link into json

$ scrapy crawl tripAllLocation -o all-attraction-list-only-first-pagi.json
