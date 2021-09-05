#!/home/petersolo427/solomonidis-flask/myprojectenv/bin/python3
import pandas as pd
from .flask_dir.database_store import add_our_world, add_john_covid
import datetime as dt

val = []


def clean_john(df):
    df.fillna("null", inplace=True)
    df.rename(columns={'Country/Region': 'Country', 'Province/State': 'Province'}, inplace=True)
    df["Country"].replace({"United Kingdom": "UK", "US": "USA", "Taiwan*": "Taiwan", "Korea, South": "S. Korea"},
                          inplace=True)
    return df


def grab_john():
    df_cases = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
        "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        error_bad_lines=False, na_values="-")
    df_cases = clean_john(df_cases)

    df_cases_1 = (df_cases.set_index(["Country", "Province", "Lat", "Long"])
                  .stack()
                  .reset_index(name='Cases')
                  .rename(columns={'level_4': 'Date'}))

    df_cases_1['Date'] = pd.to_datetime(df_cases_1['Date'])

    df_cases_1 = pd.pivot_table(df_cases_1, index=['Country', 'Date'], aggfunc='sum')

    df_deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                            "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
                            error_bad_lines=False, na_values="-")
    df_deaths = clean_john(df_deaths)

    df_deaths_1 = (df_deaths.set_index(["Country", "Province", "Lat", "Long"])
                   .stack()
                   .reset_index(name='Deaths')
                   .rename(columns={'level_4': 'Date'}))

    df_deaths_1['Date'] = pd.to_datetime(df_deaths_1['Date'])
    df_deaths_1 = pd.pivot_table(df_deaths_1, index=['Country', 'Date'], aggfunc='sum')

    df_all = df_cases_1.join(df_deaths_1['Deaths'])

    print(df_all.tail(5))
    add_john_covid(df_all, 'john_covid')


def go_back_time(time_back, days=0):
    yesterday = time_back + dt.timedelta(days=days)
    yesterday_fixed = yesterday.strftime('%d_%m_%y')
    return yesterday_fixed


def get_oecd():
    df1 = pd.read_excel(
        'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/xlsx',
        engine='openpyxl')
    add_our_world(df1, 'ecdc')


def get_our_world():
    df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",)
    add_our_world(df, 'our_world')
    return df


def get_tests_our_world():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all"
        "-observations.csv", na_values="")

    df.rename(columns={'Entity': 'Country'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Country'] = df['Country'].str.split('-').str[0].str.strip('Country ')
    df["Country"].replace(
        {"United Kingdom": "UK", "United States": "USA", "Taiwan*": "Taiwan", "Korea, South": "S. Korea"},
        inplace=True)
    print(df.tail())
    add_john_covid(df, 'our_world_tests')


if __name__ == '__main__':
    print("Running from within")
    grab_john()
    get_tests_our_world()
    get_our_world()