import time
import pymysql
import sqlalchemy
from dotenv import dotenv_values
import os
from sshtunnel import SSHTunnelForwarder


def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,  # 30 seconds
        "pool_recycle": 1800,  # 30 minutes
    }
    return init_unix_connection_engine(db_config)


def connect_ssh(ssh_user, ssh_pass):
    with SSHTunnelForwarder(('<TUNNEL_URL>', 22),
                            ssh_password=ssh_pass,
                            ssh_username=ssh_user,
                            remote_bind_address=('<BIND_ADDRESS>', 3306)
                            ) as tunnel:
        return tunnel


def init_unix_connection_engine(db_config):
    top_dir = os.getcwd().split('/')

    if 'backend' in top_dir:
        env_dir = "../.env"
    else:
        env_dir = "../.env"
    config = dotenv_values(env_dir)

    tunnel = connect_ssh(config["SSH_USER"], config["SSH_PASS"])
    tunnel.start()

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=config["SQL_USER"],  # e.g. "my-database-user"
            password=config["SQL_PASS"],  # e.g. "my-database-password"
            database=config["SQL_DB_NAME"],
            port=tunnel.local_bind_port,
            # e.g. "my-database-name",
        ),
        **db_config
    )

    return pool


def old_cursor(engine):
    connection = engine.raw_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return cursor, connection


def delete_table(table):
    engine = init_connection_engine()
    deletion = "DELETE  from {}".format(table)
    engine.execute(deletion)


def insert_newsletter(email):
    already_in = False
    engine = init_connection_engine()
    sql = "INSERT INTO update_newsletter (email, time_added) VALUES (%(email)s, %(time_added)s)"
    try:
        engine.execute(sql, email)
    except sqlalchemy.exc.IntegrityError as er:
        already_in = True
        print(email['email'], 'Already in', er)
    return already_in


def insert_twitter(tweet_dict):
    engine = init_connection_engine()

    sql = ("INSERT INTO twitter "
           "(name, tweet_id, html_content, articleLink, tweet_created,Time_accessed) "
           "VALUES (%(name)s, %(tweet_id)s, %(html_content)s, %(articleLink)s, %(tweet_created)s, %(Time_accessed)s)")
    try:
        engine.execute(sql, tweet_dict)
    except sqlalchemy.exc.IntegrityError as er:
        print(tweet_dict['name'], 'Already in')


# noinspection PyUnresolvedReferences
def add_article(table, rss_feed):
    engine = init_connection_engine()

    add_art = ("INSERT INTO {} "
               "(name, url, image, title, articleLink, summary, author, Time_accessed, Scrape) "
               "VALUES (%(name)s, %(url)s, %(image)s, %(title)s, %(articleLink)s, %(summary)s, %(author)s, "
               "%(Time_accessed)s, "
               "%(Scrape)s)".format(table))
    try:
        resp = engine.execute(add_art, rss_feed)
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.DataError) as error:
        print(error, 'second')
        resp = None
    return resp


def fetch_article_recent(table, limit):
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT name, url, image, title,articleLink, summary, Time_accessed, sentiment, author FROM {} " \
          "where sentiment != 'Empty' ORDER BY Time_accessed DESC LIMIT {}".format(table, limit)

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    cursor.close()
    return result


def fetch_article_org(db, what, query):
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT * FROM {} where {}='{}' AND Scrape is not NULL ORDER BY Time_accessed DESC LIMIT 10 OFFSET 10".format(
        db, what, query)
    cursor.execute(sql)
    head_rows = cursor.fetchall()
    connection.close()
    cursor.close()
    return head_rows


def fetch_urls():
    org_dict = {}
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT name, articleLink, Scrape FROM newsdb  ORDER BY Time_accessed DESC LIMIT 200"
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    cursor.close()

    for item in result:
        if item['name'] in org_dict:
            org_dict[item['name']].add(item['articleLink'])
        else:
            org_dict[item['name']] = {item['articleLink'], item['Scrape']}

    return org_dict


def fetch_unescaped():
    org_dict = {}
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT name, articleLink, Scrape FROM newsdb WHERE article IS NULL ORDER BY Time_accessed DESC LIMIT 200"
    cursor.execute(sql)
    result = cursor.fetchall()
    for item in result:
        if item['name'] in org_dict:
            org_dict[item['name']]['urls'].append(item['articleLink'])
        else:
            org_dict[item['name']] = {'urls': [item['articleLink']], 'Scrape': item['Scrape']}

    return org_dict


def delete_brand(db, query):
    engine = init_connection_engine()
    sql = "DELETE FROM {} WHERE name='{}'".format(db, query)
    result = engine.execute(sql)
    return result


def update_avoid(what, link, db='newsdb'):
    engine = init_connection_engine()
    sql = "UPDATE {} SET Scrape = '{}' WHERE articleLink='{}'".format(db, what, link)
    print('MAKING ERROR' + what)
    result = engine.execute(sql)
    return result


def update_brand(content_dict, table='newsdb'):
    engine = init_connection_engine()
    sql = "UPDATE {} SET sentiment = %(stats)s, article = %(article_text)s WHERE articleLink=%(link)s".format(table)
    print('Adding', content_dict['link'])
    try:
        result = engine.execute(sql, content_dict)
        return result
    except (sqlalchemy.exc.IntegrityError, ValueError, TypeError) as error:
        print('ERROR ADDING TO DB', error, content_dict['link'])
        # print(error, "making avoid", update_avoid("ERROR", link))


def add_country_code(data):
    engine = init_connection_engine()
    missing = []
    add_art = ("INSERT INTO countrycodes "
               "(Country, Code) "
               "VALUES (%s, %s)")
    for index, value in enumerate(data):
        try:
            engine.execute(add_art, data[index])
        except sqlalchemy.exc.IntegrityError as error:
            print(error)
            missing.append(data[index])
    print(missing)


def fetch_multiple_db(select, where):
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT {} FROM {} ORDER BY Time_accessed DESC LIMIT 50".format(select, where)
    cursor.execute(sql)
    head_rows = cursor.fetchall()
    connection.close()
    cursor.close()
    return head_rows


def fetch_our_world(db, countries):
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT * FROM {} WHERE Country in {} ORDER BY Time_accessed DESC LIMIT {}".format(db, countries,
                                                                                             len(countries))
    cursor.execute(sql)
    head_rows = cursor.fetchall()
    connection.close()
    cursor.close()
    return head_rows


def fetch_john_covid(db, countries, date_start, date_end):
    engine = init_connection_engine()
    cursor, connection = old_cursor(engine)
    sql = "SELECT * FROM {} WHERE Country in {} AND Date BETWEEN '{}' AND '{}'".format(db, countries, date_start,
                                                                                       date_end)
    cursor.execute(sql)
    head_rows = cursor.fetchall()
    connection.close()
    cursor.close()
    return head_rows


def add_our_world(df, db):
    print(df)
    start_time = time.time()
    engine = init_connection_engine()
    df.rename(columns={'location': 'Country', 'date': 'Time_accessed'}, inplace=True)
    df["Country"].replace(
        {"United Kingdom": "UK", "United States": "USA", "Taiwan*": "Taiwan", "Korea, South": "S. Korea"},
        inplace=True)
    df.to_sql(db, con=engine, if_exists='replace', chunksize=1000)
    print("--- %s seconds ---" % (time.time() - start_time))


def add_john_covid(df, db):
    start_time = time.time()
    engine = init_connection_engine()

    df.to_sql(db, con=engine, if_exists='replace', chunksize=1000,
              dtype={"Country": sqlalchemy.types.VARCHAR(length=255), "Date": sqlalchemy.types.DateTime})
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    print("Running from within")
    texter = """The trading pattern of the past two weeks – particularly alongside cryptocurrencys movements – suggests stocks could continue to be volatile in the week ahead. Investors are watching the wild swings in bitcoin and trying to gauge whether technology shares can gain traction after a rally attempt in the past week. Whats interesting is the market is being bullied around by where bitcoin goes said Peter Boockvar chief investment officer with Bleakley Advisory Group. Bitcoin plunged by as much as 30% on Wednesday to about $30000. Though it recovered to above $42000 it slid again on Friday. The cryptocurrency was down about 9% late Friday hovering around $36000 according to Coin Metrics. Bitcoin is a poster child for risk appetite said Boockvar. It tells you the stock market is more on uneven ground if were getting dragged along by bitcoin. There is some key data in the week ahead. Consumer confidence home price data and new home sales are out on Tuesday. Durable goods will be released Thursday and the consumer sentiment report is issued Friday. But the most important data will be the personal income and spending data which includes the personal consumption expenditure price deflator the Feds preferred inflation measure. The key to next week is going to be the inflation numbers. The inflation numbers are now becoming the new payroll numbers in terms of market performance said Boockvar. What will also be interesting is inside the consumer confidence numbers is where the inflation expectations go. As the market has chopped around this month dip buyers have stepped into the declines and snapped up perceived bargains. For me my framework is we can only get a 10% correction when we have a liquidity set back when we have a policy tightening said Barry Knapp managing partner of Ironsides Macroeconomics. In any of the little disturbances we are getting about a 4% to 6% pullback. Knapp said investors are fretting too much about higher interest rates being a problem for technology companies. You should be in the cyclical parts of tech he said. Knapp noted that subsectors like semiconductors and software should do well with the economic reopening and global manufacturing rebound. Tech squeaked out a slight gain in the past week gaining 0.1% but semiconductors popped nearly 3%. Software was up 0.2%. It wouldnt shock me if we went straight back to new highs Knapp said. Part of the reason I thought we would trade in a range was earnings season was done but net revisions is surging. He said earnings for the S&ampP 500 are now expected to be up 7% more for the year than when the first quarter reporting season began. Knapp expects the Fed may discuss tapering its bond buying at its Jackson Hole meeting in late summer and that is the likely trigger for a correction. Back to World War II he said the first correction after a recession was triggered by the Fed normalizing policy. Last cycle we had eight of those he said. Every attempt they made to normalize policy caused one of these risk off events. Knapp said its natural for investors to be focused on the Fed now. Its an uncertainty shock he said. It will cause a correction and everyone is focused on it. The Fed has not really changed its policy since the depths of the pandemic. Knapp said Treasury yields have drifted lower during efforts in Washington to reach a bipartisan plan on infrastructure spending. But he expects the market to react differently in the next two weeks since he expects those efforts will clearly fail and Democrats will focus on a big spending program that will increase the deficit. The bitcoin crypto mania was lifted by the idea of big spending from Washington and the infrastructure spending could be positive. The thing that was the surprise in 2021 that really drove the mania was the blue wave and then the spending blowout he said noting bitcoin gained on the potential for inflation and big deficit spending. Monday 1200 p.m. Atlanta Fed President Raphael Bostic 530 p.m. Kansas City Fed President Esther George Tuesday 900 a.m. S&ampPCaseShiller home prices 900 a.m. FHFA home prices 1000 a.m. New home sales 1000 a.m. Consumer confidence 1000 a.m. Fed Vice Chairman Randal Quarles at Senate Banking Committee Wednesday 330 p.m. Fed Vice Chairman Quarles Thursday 830 a.m. Initial jobless claims 830 a.m. Durable goods 830 a.m. Real Q1 GDP 1000 a.m. Pending home sales Friday 830 a.m. Personal spending PCE deflator 830 a.m. Advance indicators 945 a.m. Chicago PMI 1000 a.m. Consumer sentiment Got a confidential news tip We want to hear from you. Sign up for free newsletters and get more CNBC delivered to your inbox Get this delivered to your inbox and more info about our products and services.  Data is a realtime snapshot *Data is delayed at least 15 minutes. Global Business and Financial News Stock Quotes and Market Data and Analysis.
    """
    d = update_brand(
        {
            'link': 'https://www.euractiv.com/section/politics/opinion/the-brief-powered-by-gigaeurope-giving-vetoes-the-empty-chair/',
            'article_text': texter,
            'stats': '{"common": {"\u2019": 6, "EU": 6, "agreement": 6, "one": 4, "s": 4}, "sent": {"neg": 0.13, "neu": 0.757, "pos": 0.113, "compound": -0.8656}}'})
    print(d)
