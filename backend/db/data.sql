create table countries_codes
(
    `index`  bigint null,
    Country  text   null,
    iso_code text   null
);

create index ix_countries_codes_index
    on countries_codes (`index`);

create table countrycodes
(
    Country varchar(255) not null,
    Code    varchar(200) not null
);

create table ecdc
(
    `index`          bigint null,
    country          text   null,
    country_code     text   null,
    continent        text   null,
    population       bigint null,
    indicator        text   null,
    weekly_count     bigint null,
    year_week        text   null,
    rate_14_day      double null,
    cumulative_count bigint null,
    source           text   null
);

create index ix_ecdc_index
    on ecdc (`index`);

create table john_covid
(
    Country varchar(255) null,
    Date    datetime     null,
    Cases   bigint       null,
    Deaths  bigint       null
);

create index ix_john_covid_Country
    on john_covid (Country);

create index ix_john_covid_Date
    on john_covid (Date);

create table news_long
(
    name          varchar(255) null,
    link          varchar(255) null,
    image         varchar(255) null,
    title         varchar(255) null,
    articleLink   varchar(255) null,
    summary       text         null,
    Time_accessed varchar(255) null,
    Scrape        varchar(255) null,
    sentiment     varchar(255) null,
    constraint newsdb_title_uindex
        unique (title)
);

create table news_sent
(
    `index`       bigint null,
    name          text   null,
    link          text   null,
    image         text   null,
    title         text   null,
    articleLink   text   null,
    summary       text   null,
    Time_accessed text   null,
    Scrape        text   null,
    sentiment     text   null,
    sent          text   null,
    sent_mag      text   null,
    category      text   null,
    cat_prob      text   null
);

create index ix_news_sent_index
    on news_sent (`index`);

create table newsdb
(
    name          varchar(255) null,
    link          varchar(255) null,
    image         varchar(255) null,
    title         varchar(255) null,
    articleLink   varchar(255) null,
    summary       text         null,
    Time_accessed varchar(255) null,
    Scrape        varchar(255) null,
    sentiment     varchar(255) null,
    constraint newsdb_articleLink_uindex
        unique (articleLink)
);

create table our_world
(
    `index`                               bigint null,
    iso_code                              text   null,
    continent                             text   null,
    Country                               text   null,
    Time_accessed                         text   null,
    total_cases                           double null,
    new_cases                             double null,
    new_cases_smoothed                    double null,
    total_deaths                          double null,
    new_deaths                            double null,
    new_deaths_smoothed                   double null,
    total_cases_per_million               double null,
    new_cases_per_million                 double null,
    new_cases_smoothed_per_million        double null,
    total_deaths_per_million              double null,
    new_deaths_per_million                double null,
    new_deaths_smoothed_per_million       double null,
    reproduction_rate                     double null,
    icu_patients                          double null,
    icu_patients_per_million              double null,
    hosp_patients                         double null,
    hosp_patients_per_million             double null,
    weekly_icu_admissions                 double null,
    weekly_icu_admissions_per_million     double null,
    weekly_hosp_admissions                double null,
    weekly_hosp_admissions_per_million    double null,
    new_tests                             double null,
    total_tests                           double null,
    total_tests_per_thousand              double null,
    new_tests_per_thousand                double null,
    new_tests_smoothed                    double null,
    new_tests_smoothed_per_thousand       double null,
    positive_rate                         double null,
    tests_per_case                        double null,
    tests_units                           text   null,
    total_vaccinations                    double null,
    people_vaccinated                     double null,
    people_fully_vaccinated               double null,
    new_vaccinations                      double null,
    new_vaccinations_smoothed             double null,
    total_vaccinations_per_hundred        double null,
    people_vaccinated_per_hundred         double null,
    people_fully_vaccinated_per_hundred   double null,
    new_vaccinations_smoothed_per_million double null,
    stringency_index                      double null,
    population                            double null,
    population_density                    double null,
    median_age                            double null,
    aged_65_older                         double null,
    aged_70_older                         double null,
    gdp_per_capita                        double null,
    extreme_poverty                       double null,
    cardiovasc_death_rate                 double null,
    diabetes_prevalence                   double null,
    female_smokers                        double null,
    male_smokers                          double null,
    handwashing_facilities                double null,
    hospital_beds_per_thousand            double null,
    life_expectancy                       double null,
    human_development_index               double null
);

create index ix_our_world_index
    on our_world (`index`);

create table our_world_tests
(
    `index`                                         bigint       null,
    Country                                         varchar(255) null,
    `ISO code`                                      text         null,
    Date                                            datetime     null,
    `Source URL`                                    text         null,
    `Source label`                                  text         null,
    Notes                                           text         null,
    `Daily change in cumulative total`              double       null,
    `Cumulative total`                              double       null,
    `Cumulative total per thousand`                 double       null,
    `Daily change in cumulative total per thousand` double       null,
    `7-day smoothed daily change`                   double       null,
    `7-day smoothed daily change per thousand`      double       null,
    `Short-term positive rate`                      double       null,
    `Short-term tests per case`                     double       null
);

create index ix_our_world_tests_index
    on our_world_tests (`index`);

create table twitter
(
    name          varchar(255) null,
    tweet_id      varchar(255) null,
    html_content  longtext     null,
    articleLink   varchar(255) null,
    tweet_created varchar(255) null,
    Time_accessed varchar(255) null,
    sentiment     varchar(255) null,
    constraint twitter_tweet_id_uindex
        unique (tweet_id)
)
    collate = utf8mb4_unicode_ci;

create table update_newsletter
(
    email      varchar(255) not null,
    time_added varchar(255) null,
    constraint update_newsletter_Email_uindex
        unique (email)
);

create table user_logs
(
    ip_address    varchar(255) null,
    requested_url varchar(255) null,
    user_agent    varchar(255) null,
    Time_accessed varchar(255) null
);

create table worldometer
(
    Country         varchar(255) not null,
    Total_cases     int          null,
    New_cases       int          null,
    Total_deaths    int          null,
    New_deaths      int          null,
    Total_recovered int          null,
    Active_cases    int          null,
    Critical_cases  int          null,
    cases_per_pop   int          null,
    deaths_per_pop  int          null,
    tests_per_pop   int          null,
    Total_tests     int          null,
    Population      int          null,
    Time_accessed   varchar(255) null
);

create index worldometer_Time_accessed_index
    on worldometer (Time_accessed);

