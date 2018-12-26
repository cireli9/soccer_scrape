# soccer_scrape

Utilized to scrape data from the Premier League website. A very rough program that currently does not include red cards and will swap Yellow Cards/Fouls if there are 0 Yellow Cards during a match. Can be easily edited to scrape data from years besides 2017-2018. Depending on speed of internet connection, SCROLL_PAUSE_TIME may need to be changed.

Note also that the program requires more memory than available to python, and thus will fail to execute around the 360th match. With this in mind, the program must be run twice, once at the beginning and again after changing the range of n in the for loop to begin at around 350.

Raw data from 2017-2018 is included that was produced from the program. Along with that is a macro-enabled excel sheet used to correct the Yellows/Fouls error as well as a python program used to scrape all data for Liverpool.

A similar program was utilized to scrape La Liga and Serie A data (included as soccer_goalvar_scrape).
