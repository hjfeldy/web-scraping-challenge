from flask import Flask, render_template, redirect, jsonify
from scrape_mars import scrape
from pymongo import MongoClient


app = Flask(__name__)



@app.route('/')
def home():
    client = MongoClient('localhost', 27017)
    col = client.marsdb.info.find_one()

    title = col['newsTitle']
    paragraph = col['newsParagraph']
    table = col['tableString']
    hemispheres = col['hemispheres']
    image = col['featuredImg']

    
    return render_template('index.html', 
                            title= title,
                            paragraph= paragraph,
                            table= table,
                            hemispheres= hemispheres,
                            image = image
                            )

@app.route('/scrape')
def callScrape():
    scrape()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug= True)