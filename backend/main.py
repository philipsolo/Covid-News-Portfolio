import json
import time
import sentry_sdk
from flask import render_template, request, session, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_dir.news_grab import grab_all_recent, article_by_org
from flask_dir import create_app
from flask_dir.covid_grab import grab_our_world, check_country, grab_john_hop, get_countries, grab_our_world_tests
# from database_store import insert_newsletter
from flask_dir.email_send import send_dynamic

# sentry_sdk.init(
#     dsn="<SENTRY_URL>",
#     integrations=[FlaskIntegration()])

app = create_app()

default_countries = ('World', 'Greece', 'UK')
all_countries = get_countries()


def confirm_countries():
    if 'countries' not in session:
        session['countries'] = default_countries
    return session['countries']


@app.route('/', methods=['GET', 'POST'])
def covid_update():
    return render_template('covid.html')

@app.route('/news', methods=['GET', 'POST'])
def react_base():
    return render_template('base.html')


@app.route("/covid/get_our_world", methods=['GET', 'POST'])
def get_our_world():
    countries = confirm_countries()
    our_world = grab_our_world(countries)
    if request.method == 'GET':
        return jsonify(our_world)
    if request.method == 'POST':
        return 'Success', 200


@app.route("/covid/get_our_world_tests", methods=['GET', 'POST'])
def get_our_world_tests():
    countries = confirm_countries()
    if 'date_range' not in session:
        our_world_tests = grab_our_world_tests(countries)
    else:
        dates_dict = session['date_range']
        our_world_tests = grab_our_world_tests(countries, dates_dict['from'], dates_dict['to'])

    if request.method == 'GET':
        return jsonify(our_world_tests)
    if request.method == 'POST':
        return 'Success', 200


@app.route("/covid/get_daily", methods=['GET', 'POST'])
def get_john_hop():
    countries = confirm_countries()
    if 'date_range' not in session:
        john_dict = grab_john_hop(countries)
    else:
        dates_dict = session['date_range']
        john_dict = grab_john_hop(countries, dates_dict['from'], dates_dict['to'])
    if request.method == 'GET':
        return jsonify(john_dict)
    if request.method == 'POST':
        return 'Success', 200


@app.route('/covid/change_dates', methods=['GET', 'POST'])
def change_dates():
    if request.method == 'POST':
        form_json = request.get_json()
        session['date_range'] = {'from': form_json[0]['value'], 'to': form_json[1]['value']}
        return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})


@app.route('/covid/add_country', methods=['GET', 'POST'])
def create_chat():
    countries = list(confirm_countries())
    if request.method == 'POST':
        form_json = request.get_json()
        def_country = check_country(form_json)
        if def_country in countries:
            return json.dumps({'status': 'already_in'})
        elif def_country not in all_countries:
            return json.dumps({'status': 'missing'})
        else:
            countries.append(def_country)
        session['countries'] = tuple(countries)
        return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})


@app.route('/covid/remove_country', methods=['GET', 'POST'])
def remove_country():
    countries = list(confirm_countries())
    if request.method == 'POST':
        form_json = request.get_json()
        if form_json in countries:
            countries.remove(form_json)
            session['countries'] = tuple(countries)
            return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})


@app.route('/<country>', methods=['GET', 'POST'])
def query_country(country):
    def_country = check_country(country)
    if def_country in all_countries:
        session['countries'] = ('World', def_country)
    return covid_update()


@app.route('/news/get_articles', methods=['GET', 'POST'])
def news_update():
    form_json = request.get_json()
    if 'query' in form_json:
        if form_json['query'] == 'all':
            articles = grab_all_recent(200, 20)
        else:
            articles = article_by_org(form_json['page'], 6)
        return json.dumps(articles)
    else:
        return json.dumps({'status': 'ERROR'})


@app.route('/sentiment_info')
def sentiment_info():
    return render_template('sentiment_info.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def change_sources():
    return render_template('sign_up.html')


@app.route('/coming_soon', methods=['GET', 'POST'])
def coming_soon():
    already_in = 'Request'
    email_dict = {}
    if request.method == 'GET':
        print(request.form, "GET")
    elif request.method == 'POST':
        email = request.form.get('email')
        email_dict.update(
            {
                "email": email, 'time_added': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        already_in = insert_newsletter(email_dict)
        if not already_in:
            send_dynamic(email)
    return render_template('coming_soon.html', gotit=already_in)


@app.errorhandler(404)
def error_404(e):
    print(e)
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    print(e)
    return render_template('404.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0',        port='6000')
