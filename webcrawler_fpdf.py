from fpdf import FPDF
from fpdf.enums import XPos, YPos
import requests
from bs4 import BeautifulSoup
from datetime import date

print("Loading...")
title = 'Tech News'
date_today = date.today().strftime('%d-%m-%Y')

class PDF(FPDF):

    def __init__(self, **kwargs):
        super(PDF, self).__init__(**kwargs)
        #adding unicode font family
        self.add_font('DejaVu', '', './fonts/DejaVuSansCondensed.ttf')
        self.add_font('DejaVu', 'B', './fonts/DejaVuSansCondensed-Bold.ttf')
        self.add_font('DejaVu', 'I', './fonts/DejaVuSansCondensed-Oblique.ttf')

    def header(self):
        self.set_font('Times', 'B', 20)
        #Calculate width of the words in title + a bit of padding
        title_w = self.get_string_width(title) + 6
        doc_w = self.w #Calculate document width
        #To set title at center of the page 
        self.set_x((doc_w - title_w) / 2)
        self.set_line_width(0.5) #thickness of frame/border: 1mm
        #Create a cell for the title
        self.cell(title_w, 10, title, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=0)
        #line break
        self.ln(10)

    def footer(self):
        #15mm from the bottom, +ve means from the top
        self.set_y(-15)
        self.set_font('Times', 'I', 10)
        self.set_text_color(169, 169, 169) #footer color = gray
        #nb is total number of pages in the document
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    #Adding News Source Links
    def news_source_header(self, news_source, link):
        self.add_page()
        #Set link location
        self.set_link(link)
        self.set_font('Times', 'B', 15)
        self.set_fill_color(200, 220, 255)
        chapter_title = f'{news_source}'
        self.cell(0, 10, chapter_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=1, align='C')
        self.ln(10)

    def article_headline(self, headline):
        self.set_font('DejaVu', 'U', 12)
        self.multi_cell(0, 15, headline, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def article_author(self, author):
        self.set_font('DejaVu', 'I', 10)
        self.set_text_color(128,128,128)
        self.multi_cell(0, -5, f'Written By: {author}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(8)

    def article_summary(self, summary):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, summary, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

    def article_link(self, link):
        self.set_font('DejaVu', 'I', 10)
        link_text = 'To find out more: '
        link_text_width = self.get_string_width(link_text)
        self.cell(link_text_width, 4, link_text)
        self.set_font('DejaVu', 'UI', 10)
        self.multi_cell(0, 4, link, new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=link)
        self.ln(10)

#Initialise the pdf document
pdf = PDF(orientation = 'P', unit = 'mm', format='A4')
document_width = pdf.w

#set metadata
pdf.set_title(title)
pdf.set_author('Jun Han')

#Adding links
cnbc_link = pdf.add_link()
bbc_link = pdf.add_link()
nyt_link = pdf.add_link()

#get total number of pages
pdf.alias_nb_pages()

#auto page break starts 15mm from the bottom of the page
pdf.set_auto_page_break(auto=True, margin=15)

#PDF COVER PAGE

pdf.add_page()
pdf.set_font('DejaVu', 'B', 30)
pdf.set_fill_color(200, 220, 255)
pdf.cell(0, 30, 'Content Page', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=1)

pdf.set_font('DejaVu', 'I', 15)
pdf.cell(0, 20, f'Generated on {date_today}', align='C')
pdf.ln(25)

pdf.set_x((document_width - 180) / 2)
pdf.set_font('DejaVu', '', 12)
welcome_message = 'Welcome! This is Tech News, where the latest news related to the tech'\
    'industry are compiled succintly into this PDF. '\
    'The content in this PDF is entirely extracted from the following '\
    'news sources. If you are interested in any of these articles, do click on '\
    'the article link. Happy reading!'
pdf.multi_cell(170, 8, welcome_message, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(5)
pdf.set_x(15)

pdf.cell(0, 15, 'Contact me via my email: hojunhan49@gmail.com', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(5)
pdf.set_x(15)

#NEWS LINKS
pdf.cell(0, 15, 'Click on the following news sources: ', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(25)
pdf.set_font('DejaVu', 'BU', 12)
pdf.cell(0, 15, 'CNBC News', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=cnbc_link)
pdf.set_x(25)
pdf.cell(0, 15, 'BBC News', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=bbc_link)
pdf.set_x(25)
pdf.cell(0, 15, 'New York Times', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=nyt_link)
pdf.set_x(25)
pdf.set_font('DejaVu', 'I', 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, -2, 'To access articles on the New York Times, a NYT account is required.')
pdf.set_text_color(0, 0, 0)

#CNBC NEWS SECTION
pdf.news_source_header('CNBC News', cnbc_link)

#Creating a session to access CNBC Tech
url_cnbc = 'https://www.cnbc.com/technology/'
session = requests.Session()
cnbc_news = session.get(url_cnbc)

#Initialise BeautifulSoup to access news headlines
soup = BeautifulSoup(cnbc_news.content, 'lxml')
cnbc_headlines_div = soup.select('.Card-title')
num = 0

#For each of the news headlines:
for i in cnbc_headlines_div:
    if i.string:
        num += 1

        #Get the news headline text
        cnbc_headline = i.string.strip()

        #Follow the headline link to a news webpage
        cnbc_content_link = i['href'].strip()
        cnbc_article_f = requests.get(cnbc_content_link)
        cnbc_article_soup = BeautifulSoup(cnbc_article_f.content, 'lxml')

        #Get the author of the article
        try:
            cnbc_article_author_list = cnbc_article_soup.find('a', {'class':'Author-authorName'})
            cnbc_article_author = cnbc_article_author_list.text
        except AttributeError:
            cnbc_article_author = 'Unknown'

        #Get the summary of the news article
        try:
            cnbc_article_content = cnbc_article_soup.find('div', {'class':'RenderKeyPoints-list'})
            cnbc_article_content_list = cnbc_article_content.findAll('li')
            cnbc_key_points = ''
            for i in cnbc_article_content_list:

                #Clean up between different list points
                if cnbc_key_points != '':
                    cnbc_key_points += ' '
                cnbc_key_points += i.string.strip()
        #If no list is present, return the first paragraph of the article
        except:
            cnbc_key_points_list = cnbc_article_soup.select('.ArticleBody-articleBody > .group p:first-child')
            cnbc_key_points = cnbc_key_points_list[0].text

        #Write the relevant article information onto the pdf for each headline found
        pdf.article_headline(cnbc_headline)
        pdf.article_author(cnbc_article_author)
        pdf.article_summary(cnbc_key_points)
        pdf.article_link(cnbc_content_link)
    
print("The CNBC News Section is consolidated.")

#BBC NEWS SECTION
pdf.news_source_header('BBC News', bbc_link)

#Accessing BBC website's Tech News
url_bbc = 'https://www.bbc.com/news/technology'
session = requests.Session()
bbc_news = session.get(url_bbc)

#Initialising BeautifulSoup and finding news headlines
soup = BeautifulSoup(bbc_news.content, 'lxml')
bbc_headlines_div = soup.findAll('a', {'class':'gs-c-promo-heading'})
num = 0

#For each news headline:
for i in set(bbc_headlines_div):
    if i.string:

        #Getting the news headline
        bbc_headline = i.string.strip()

        #Getting the specific news webpage link
        bbc_content_link = i['href'].strip()

        #Excluding unwanted pages like Watch/Listen section by using the fact
        #that they have links that start with https://www.bbc.com
        try:
            bbc_article_f = requests.get(f'https://www.bbc.com{bbc_content_link}')
        except:
            #Errors that arise from inexistent links
            continue

        #For valid articles:
        bbc_article_soup = BeautifulSoup(bbc_article_f.content, 'lxml')

        #Finding the author of the article
        bbc_article_author_list = bbc_article_soup.select('.ssrcss-ugte5s-Contributor span strong')
        if not bbc_article_author_list:
            bbc_article_author = 'Unknown'
        else:
            for i in bbc_article_author_list:
                #Excluding 'By '
                bbc_article_author = i.string[3:]

        #Finding the key points of the article which are in bold
        bbc_article_content = bbc_article_soup.find('b', {'class':'ssrcss-hmf8ql-BoldText'})
        bbc_key_points = bbc_article_content.string.strip()

        #Write the relevant article information onto the pdf for each headline found
        pdf.article_headline(bbc_headline)
        pdf.article_author(bbc_article_author)
        pdf.article_summary(bbc_key_points)
        pdf.article_link('https://www.bbc.com'+bbc_content_link)

print("The BBC News Section is consolidated.")
        
#NEW YORK TIMES SECTION
pdf.news_source_header('New York Times', nyt_link)

#Creating a session to access nyt Tech
url_nyt = 'https://www.nytimes.com/international/section/technology'
session = requests.Session()
nyt_news = session.get(url_nyt)

#Initialise BeautifulSoup to access news headlines in two different areas
soup = BeautifulSoup(nyt_news.content, 'lxml')
nyt_headlines_div = soup.findAll('div', class_=['css-10wtrbd', 'css-1l4spti'])
num = 0
news_headlines_list = []

#For each of the news headlines:
for i in nyt_headlines_div:
    #if i.string:
        num += 1

        #Get the news headline text
        nyt_headline = i.h2.text.strip()
        #Ensure no repeating of news articles
        if nyt_headline not in news_headlines_list:
            news_headlines_list.append(nyt_headline)
        else:
            continue

        #Getting the link for the article webpage
        nyt_content_link = i.a['href'].strip()

        #Get the author of articles of the two different news areas
        try:
            nyt_article_author = i.find('span', {'class':'css-1baulvz'}).text
        except:
            nyt_article_author = i.find('span', {'class':'css-1n7hynb'}).text

        #Get the summary of the news article
        #If summary is not found, return a default string
        try:
            nyt_article_summary = i.find('p', {'class':'css-tskdi9'}).string
        except:
            nyt_article_summary_item = i.find('p', {'class':'css-1pga48a'})
            nyt_article_summary = 'Click on the news link to find out more'
            if nyt_article_summary_item != None:
                nyt_article_summary = nyt_article_summary_item.string
                
        ##Write the relevant article information onto the pdf for each headline found
        pdf.article_headline(nyt_headline)
        pdf.article_author(nyt_article_author)
        pdf.article_summary(nyt_article_summary)
        pdf.article_link('https://www.nytimes.com'+nyt_content_link)

print("The New York Times section is consolidated.")

#Save the pdf
pdf.output('tech_news.pdf')
print('The pdf is consolidated!')