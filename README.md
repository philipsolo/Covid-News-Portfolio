# [Solomonidis.me](https://solomonidis.me) 🌐 

---

(Currently 🏗️ as React implemented) First website I built to learn the full stack web development process. Started out as I was annoyed by the newsreaders I
found online containing adds and paywalls, wanted to customize my data intake as I pleased. The Covid-19 dashboard
was another requirement as no app I found had all the data in my customized preference.

## Notes 🎶

---

- To assist  the learning process I decided to break a core SWE principal and use different methods for duplicate
  functionality. I find that testing all possible scenarios is a good way of learning. For example as I wanted to find
  the optimal python SQL API (and revise mySQL) I used multiple different libraries and methods.


- Sentiment analysis performed on every news article is important not only as a quick warning of an articles potential
  bias but, as more and more articles are collected a 'scientific' conclusion can be made regarding the publisher.

## Table of Contents

---

* [Notes 🎶](#notes---)
* [Demo & Functionality 🎥](#demo-functionality)
    + [Covid-19 Dashboard](#covid-19-dashboard)
    + [News Page](#news-page)
* [Structure 🏗️](#structure-)
    + [Data Aggregation](#Data-Aggregation)
    + [Data Transit](#Data-Transit)
    + [Frontend](#Frontend)
    + [Web-Framework & management](#Web-Framework-&-management)
* [Build & Deployment 🚀](#build-deployment)
    + [Local Run](#local-run)
    + [GCP Run](#gcp-run)

## Demo & Functionality 🎥

---

### `Covid-19 Dashboard` (Legacy JS/HTML dark mode)

![Covid Dashboard Gif](./demo_material/covid_dashboard.gif)

### `News Page` (React Version)

![News Example Gif](./demo_material/news-dash.gif)

## Structure 🏗️

---

### **Data Aggregation**

| File | Description |
| ----------- | ----------- |
| [corona_db.py](backend/data_scrape/corona_db.py) | Retrieves Covid data from John's Hopkins, Our World in Data, OECD and adds to database.
| [news_db.py](backend/data_scrape/news_db.py) | Retrieves news stories adds links, description and image to database.
| [scraper.py](backend/data_scrape/scraper.py) | Queries database for `Unscraped stories` performs sentiment analysis and appends result to db.
| [sentiment.py](data_scraping(legacy)/sentiment.py) | wrapper file called by scraper file, provides the sentiment data and categories.
| [twitter.py](data_scraping(legacy)/twitter.py) | Scrapes twitter posts from predefined persons, trending topics etc. and adds to db.
| [news_image_db.py](data_scraping(legacy)/news_image_db.py) | Grabs pre-defined unencrypted images, adds them to google storage bucket for use on website (To avoid XSS issues).
| [rss.json](backend/data_scrape/rss.json) | all news sources archived and organized.

### **Data Transit**

| File | Description |
| ----------- | ----------- |
|[database_store.py](backend/flask_dir/database_store.py) | All database requests pass from here (insertion, deletion etc.) Most functions are now deprecated but kept as a personal reminder for potential use
|[covid_grab.py](backend/flask_dir/covid_grab.py) | Prettify and jsonify Covid data for proper transit to frontend|
|[news_grab.py](backend/flask_dir/news_grab.py) | Prettify and jsonify News data for proper transit to frontend|
|[email_send.py](backend/flask_dir/email_send.py) | Sends email to user upon registration to news feed using the solomonidis domain interfaces with Twilio free email delivery API sending pre-defined template|

### **Frontend**

### `Non-React`

| File | Description |
| ----------- | ----------- |
|[covid_data.js](backend/flask_dir/static/js/covid_data.js)| Javascript API Request/Response for Covid dashboard also chart rendering etc.|
|[covid.html (LEGACY)](backend/flask_dir/templates/covid.html) | html page for Covid dashboard|
|[news.html (LEGACY)](backend/flask_dir/templates/news.html) | html page for News (also contains some javascript mostly written in Jinja)|
|[sentiment_info.html](backend/flask_dir/templates/sentiment_info.html) | Extra page displaying Iframes from google studio (connected to DB displaying all sentiment data collected and categorized)|
|[base.html](backend/flask_dir/templates/base.html) | Entry Point for React (babel stored in static)|

### `React 🏗️`

| File | Description |
| ----------- | ----------- |
|[NewsArticles.js](frontend/components/news/NewsArticles.js)|Main display component for news page |
|[NewsCard.js](frontend/components/news/NewsCard.js) |Individual card component|
|[NewsFilter.js](frontend/components/news/NewsFilter.js) |Filter component for side bar|
|[CovidDash.js](frontend/components/covid/CovidDash.js) |Renders graphs to page using helper functions from [base.html](backend/flask_dir/static/js/covid_data.js)|

### **Web-Framework & management**

| File | Description |
| ----------- | ----------- |
| [main.py](backend/main.py) | Flask file, all routes handled here|
| [app.yaml](backend/app.yaml) | GCP configuration file for app engine upload|
| [requirements.txt](backend/requirements.txt) | all required libraries for project to run.|

## Build & Deployment 🚀

---

### Local Run 💻

1. Clone The Repository:

    ```bash
    git clone https://github.com/philipsolo/solomonidis-flask.git
    ```

2. If Mysql server is already installed simply dump the tables using the [data.sql](/db/data.sql) provided else use
   the [docker](docker-compose.yml) file provided
   ```bash
   docker-compose up
   ```

3. Install dependencies and requirements.

    ```bash
    python3 -m venv myprojectenv
    ```

    ```bash
    source myprojectenv/bin/activate
    ```

    ```bash
    pip install -r requirements.txt
    ```


4. Each file in data_scraping folder retrieves different data, as an example for the all Covid-19 data run
   ```bash
   python data_scraping(legacy)/corona_db.py
   ```

5. Run the file
    ```bash
    python -m flask run
    ```

## GCP Run ☁

- Create [Cloud SQL](https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard) and connect to App engine


- Enable and start [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3/runtime)


- The [app.yaml](app.yaml) Included contains the setup needed for Mysql to interface with Cloud Sql (Remember to give
  necessary **permissions** to app engine service account from IAM page)


- After installing [gcloud sdk](https://cloud.google.com/sdk/docs/install)
  simply run
  ```bash
  gcloud init
  ```
  Login with gcloud account
  ```bash
  gcloud app deploy
  ```
