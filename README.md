# Amazon-Shopping-Bot
A simple discord bot written in Python that helps someone organize their shopping on Amazon. Web scraping can also be used to gather information on someone's search on Amazon.

## Dependencies Needed to be Installed
#### 1. Install Discord.py
```bash
pip3 install -U discord.py
```
#### 2. Install Dotenv  
```bash
pip3 install -U python-dotenv
```
#### 3. Install SelectorLib package and Python Requests
```bash
pip3 install requests requests selectorlib
```
#### 4. Update .env  
> Edit env template.md with bot's token and guild name (steps detailed in the link below)
https://realpython.com/how-to-make-a-discord-bot-python/

## Run bot.py   
```bash
python3 bot.py
```
## COMMANDS

#### 1. Add an item to the Shopping List
add <item>
  
#### 2. Remove an item to the Shopping List 
remove <item>

#### 3. Print out the current list of items
list

#### 4. Recommend a random item category
random

#### 5. Write the current list to another text file
write

#### 6. Help Command
help

## Run the Amazon Scraper after the write command
```bash
python3 searchresults.py
```
The results should be visible in search_results_output.jsonl. 

## Resources Used
https://realpython.com/how-to-make-a-discord-bot-python/

https://stackoverflow.com/questions/14885907/scraping-product-names-using-beautifulsoup

https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python-and-selectorlib/
