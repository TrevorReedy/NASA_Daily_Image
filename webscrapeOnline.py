from bs4 import BeautifulSoup 
from flask import Flask, render_template, request #Render template allows http interaction
import requests 
import json
from datetime import datetime,date



app = Flask(__name__)
 

def get_archive_nasa():
        archiveDate = request.form["archive_search"]
        formatArchiveDate = archiveDate
        for i in range(0,formatArchiveDate.count('/')):
              formatArchiveDate = formatArchiveDate.replace('/','')



        url = f'https://apod.nasa.gov/apod/'+'ap'+formatArchiveDate+'.html'
        results = requests.get(url)
        doc = BeautifulSoup(results.text, "html.parser")
        img = (doc.find('img'))
        img_src = img["src"]
        img_url = requests.compat.urljoin(url, img_src)
        today = date.today()
        dateTodayText = today.strftime("%b/%d/%Y")
       
        
        return(img_url,archiveDate,dateTodayText, url)


        
def get_nasa():
        url = 'https://apod.nasa.gov/apod/astropix.html'
        results = requests.get(url)
        doc = BeautifulSoup(results.text, "html.parser")
        img = (doc.find('img'))
        img_src = img['src']
        img_url = requests.compat.urljoin(url, img_src)
        today = date.today()
        dateToday = today.strftime("%y /%m /%d")
        dateTodayText = today.strftime("%b %d %Y")
        return(img_url, dateToday,dateTodayText, url)




@app.route("/") #Routes data to the app, aka website
def index():
    nasa_pic,dateToday,dateTodayText,url = get_nasa()
    return render_template("home.html", nasa_pic=nasa_pic, dateToday=dateToday, dateTodayText =dateTodayText, img_url = url)

@app.route("/<string:archiveDate>", methods=["POST","GET"]) 
def archive_search(archiveDate):
#     archiveDate = request.form["archive_search"]
    nasa_pic,archiveDate,dateTodayText,url= get_archive_nasa()

    return render_template("home.html", nasa_pic=nasa_pic, dateToday=archiveDate, dateTodayText =dateTodayText, img_url = url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)





