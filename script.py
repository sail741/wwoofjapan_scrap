"""
This project is used to scrap data on www.wwoofjapan.com.
As there is a lot of wwoofing host and it's hard to see all of them, this can be used to search the good host

__author__ = "Léo Mullot aka Sail"
__version__ = "1.0.1"
__date__ = 26/03/2019
"""

import tools
import params

# Select your params type from the params file and start scraping
tools.scrap(params.params_couple_with_restriction)
