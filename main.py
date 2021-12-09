"""Main module that run the covid dashboard"""
import covid_news_handling
import covid_data_handler
import logging
from flask import Flask, render_template, request
from covid_news_handling import delete_news_articles
from covid_data_handler import delete_schedule, schedule_covid_updates, \
    UPDATE, s
from time_conversion import sched_time


logging.basicConfig(filename='dashboard.log', level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(module)s '
                           '%(message)s')

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello():
    """Main function that run the dashboard. """
    update_name = request.args.get('two')
    if update_name:
        UPDATE_TIME = request.args.get('update')
        schedule_time = sched_time(UPDATE_TIME)
        schedule_covid_updates(schedule_time, update_name)
    delete_news_articles()
    delete_schedule()
    s.run(blocking=False)
    return render_template('index.html',
                           title='Daily update',
                           news_articles=covid_news_handling.ARTICLES,
                           location=covid_data_handler.location,
                           nation_location=covid_data_handler.nation_location,
                           local_7day_infections=
                           covid_data_handler.local_7day_infections,
                           national_7day_infections=
                           covid_data_handler.national_7day_infections,
                           hospital_cases=covid_data_handler.hospital_cases,
                           deaths_total=covid_data_handler.deaths_total,
                           updates=UPDATE,
                           faviacon='static/pictures/faviacon.jpg',
                           image='static/pictures/covid_pic.jpg'
                           )


if __name__ == '__main__':
    logging.debug(app.run())
