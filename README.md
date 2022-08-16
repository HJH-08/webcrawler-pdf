<img src="https://github.com/HJH-08/webcrawler-pdf/blob/main/%E2%9C%89_Webcrawler.png" width='1200' height = '300'>

<br>
<p align="center">
    <img src="https://img.shields.io/github/last-commit/hjh-08/webcrawler-pdf" />
    <img src="https://img.shields.io/github/repo-size/hjh-08/webcrawler-pdf">
<p>


<p align="center">
  <a href="#tech-news">About</a> •
  <a href="#prerequisities">Prerequisites</a> •
  <a href="#how-to-run-the-script">Instructions</a> •
  <a href="#potential-errors">Potential Errors</a>
  
</p>

# Tech News

## Brought to you by a webcrawler, finding the latesttech news

This project is written in `Python`. The webcrawler
* Goes through the tech news websites of the **CNBC**, **BBC** and **NYT** (in that order)
* Follows the link of news articles
* Finds details like the article's **author**, **headline** and **summary**
* Consolidates the information neatly and presents it in a pdf called `tech_news.pdf`

<br>
___

     
## Prerequisites
       
`Python` should be installed locally. Check [here](https://www.python.org/downloads/) to install depending on your OS. Your computer should be able to access the Internet too.

### Required Modules and Fonts
- `fpdf`
- `requests`
- `bs4`
- `DejaVu fonts`


To install `fpdf`:
```
$ pip install fpdf2
```

To install `requests`: 
```
$ pip install requests
```

To install `bs4`: 
```
$ pip install requests
```

To import the `DejaVu fonts`:
Check [here](https://www.fontsquirrel.com/fonts/dejavu-sans), and click **download ttf** to download the zip file containing the DejaVu font family. Move the folder to the **same** directory from which this code is run, and unzip the contents. This folder should be similar to the `fonts` folder found in this repository.
<br>

## How to run the script
<br>

Run this code:
``` bash
$ python webcrawler-pdf.py
```
<br>
If there are no errors, the following should be printed out:

```
Loading...
The CNBC News Section is consolidated.
The BBC News Section is consolidated.
The New York Times section is consolidated.
The pdf is consolidated!
```

There will be a `pdf` file named `tech_news.pdf` that is downloaded onto the same directory from which this code has been run. Open it to view the tech news.

## Potential Errors
<br>
The code works as of when it is last edited. However, the webcrawler uses html classes and ids from the news websites to find information. The functionality of the code is subject to change from the third party news websites. Thus if the code does not work as intended, there's a good chance that I'm already editing the code. ㋡ Thanks for understanding!

