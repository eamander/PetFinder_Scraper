# PetFinder_Scraper
A simple Python image scraper for PetFinder using Selenium and requests. The goal is to enable simple, automated collection of images from PetFinder. I chose Selenium because PetFinder uses a lot of JS which made other libraries difficult. Selenium gives us access to the page as the user sees it which includes links to the source images and important features like the "next" button.

## Getting Started
You will need a few things on your system to get this working:

1. Python 3.4+
2. Selenium 3.8.0 and requests 2.18.4 (I'm sure earlier versions work too, but I have not tested)
3. Chrome web driver (currently I've got it coded exclusively for Chrome, that's an easy fix of course)

### Python 3.4+
Many tutorials exist on installing Python, e.g. [Anaconda3] (https://conda.io/docs/user-guide/install/download.html).

### Selenium 
Here's the easiest way:
From [pypi.python.org] (https://pypi.python.org/pypi/selenium).
> If you have pip on your system, you can simply install or upgrade the Python bindings:
```
pip install -U selenium==3.8.0
```

### Requests
Just as with Selenium
```
pip intall requests==2.18.4
```

### Chrome web driver
A comprehensive installation guide for ChromeDriver is available here:
[SeleniumHQ github](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver)

## Running the scraper
Using an existing Python distribution, navigate to the folder in which you would like to store a subfolder containing your scraped images.

Since this is a quick and dirty scraper for another project, it currently defaults to scraping cat images and requires chromedriver.exe to be discoverable. The command-line scraper does not currently have an option for scraping other types of animal.

The program takes a single optional positional argument:
1. subfolder name [.\petfinder_image_data]
```
python petfinder_scraper.py [1]
```

You should then be on your way to collecting images! 

## Prospects for improvement
Additional command-line arguments to improve functionality:
1. different search terms
2. different chromedriver locations
3. special search terms (e.g. breed, color, age, location)
4. proper navigation to deeper search pages

## Outstanding issues
1. (from 4 above) Selenium and PetFinder do not yet cooperate to allow navigation directly from the 1st search page to an arbitrary search page. Instead, we just hit "next page" a sufficient number of times until we arrive at a deeper page of the search
2. Occasionally, the scraper gets hung up on the first search page. This is likely a matter of checking the refresh loop to make sure it continues properly, but the scraper works well enough as is. A user can manually reload the first search page to get it going again.

## Additional Info
This was designed in support of machine learning projects involving common animals. We are clearly leaving out what might appear to be some valuable information about the animals in question, namely breeds of cat and color for instance. However, there is a significant amount of disagreement regarding both the existence of some breeds and their presentation. Therefore, any supervised learning algorithm will require proper standardization by an expert.

