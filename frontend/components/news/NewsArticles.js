import React from 'react';
import NewsCard from "./NewsCard";
import {Avatar, Backdrop, Chip, CircularProgress, Container, Grid, withStyles, Divider, Box} from "@material-ui/core";
import Pagination from "@material-ui/lab/Pagination";
import DoneIcon from '@material-ui/icons/Done';
import green from "@material-ui/core/colors/green";
import NewsFilter from "./NewsFilter";
import ScrollToTop from "../misc/ScrollToTop";


const styles = theme => ({
    root: {
        width: "100%",
        backgroundColor: 'primary',
        justifyContent: "center",
    },
    item: {
        padding: theme.spacing(1.2)
    },
    avatar: {marginRight: theme.spacing(5)},
    paginator: {
        justifyContent: "center",
        padding: "10px"
    }
});

class NewsArticles extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleFilterItem = this.handleFilterItem.bind(this);
        this.state = {
            error: null,
            isLoaded: false,
            currentArticles: [],
            allArticles: [],
            words: [],
            pageCount: 6,
            totalItems: 0,
            currentPage: 1,
            query: 'all',
            selectedSources: []
        };
    }


    handleChange = (event, value) => {

        this.setState({
            currentPage: value
        }, () => {
            window.scrollTo(0, 0);
        });
    };

    componentDidMount() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json; charset=utf-8'},
            body: JSON.stringify({query: 'all', page: this.state.currentPage})
        };

        fetch("/news/get_articles", requestOptions)
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result)
                    this.setState({
                        isLoaded: true,
                        currentArticles: result['articles'],
                        allArticles: result['articles'],
                        totalItems: result.metadata['art_len'],
                        words: result['top_words'],
                        metadata: result.metadata,
                        selectedSources: Object.keys(result.metadata['sources']),
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )

        window.scroll({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    }

    handleClick = (art, event) => {
        let tempSources = []
        let tempItems = {};
        let tempQuery
        let tempTotalArt = 0

        const {allArticles, metadata} = this.state

        let selectedWord = art['word']

        if (selectedWord === this.state.query) {
            tempItems = allArticles
            tempQuery = 'all'
            tempSources = Object.keys(this.state.metadata['sources'])
            tempTotalArt = metadata['art_len']
        } else {
            art.urls.map(function (url) {
                tempItems[url] = allArticles[url]
                tempSources.push(allArticles[url]['name'])
                tempTotalArt++
            })
            tempQuery = selectedWord
        }

        this.setState({
            currentPage: 1,
            currentArticles: tempItems,
            query: tempQuery,
            selectedSources: tempSources,
            totalItems: tempTotalArt
        });
    }

    handleFilterItem(selectedNews) {
        const {allArticles, metadata} = this.state
        let tempSources = []
        let tempTotalArt = 0

        if (selectedNews.length === 0) {
            tempSources = Object.keys(allArticles)
            tempTotalArt = metadata['art_len']
        } else {
            tempSources = selectedNews
            const selectedArts = Object.keys(allArticles).filter(url => selectedNews.indexOf(allArticles[url].name) > -1)
            tempTotalArt = selectedArts.length;

        }

        this.setState({
            currentPage: 1,
            selectedSources: tempSources,
            totalItems: tempTotalArt
        })

    }

    render() {
        const {
            error,
            isLoaded,
            currentArticles,
            words,
            pageCount,
            currentPage,
            metadata,
            query,
            selectedSources,
            totalItems
        } = this.state
        const {classes} = this.props;
        const offset = (6 * currentPage) - 6


        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>
                <Backdrop className={classes.backdrop} open={true}>
                    <CircularProgress color="inherit"/>
                </Backdrop>
            </div>;
        } else {
            return (
                <div>
                    <ScrollToTop>
                    <Container direction="row"
                               maxWidth="lg" style={{padding: 5}}>

                        <Grid container
                              justify="center"
                              alignItems="center" spacing={1} style={{marginTop: 10}}>
                            {
                                words.map(function (top_word) {
                                    return <Grid key={top_word['word']} item xs align="center">
                                        <Chip color={query === top_word['word'] ? "primary" : "default"}
                                              deleteIcon={<DoneIcon
                                                  style={query === top_word['word'] ? {color: green[500]} : {}}/>}
                                              onDelete={this.handleClick.bind(top_word, top_word)}
                                              onClick={this.handleClick.bind(top_word, top_word)}
                                              label={top_word['word']}
                                              avatar={<Avatar>{top_word['count']} </Avatar>}/>
                                    </Grid>
                                }, this)
                            }
                        </Grid>

                        <Divider style={{marginTop: 15}}/>

                        <Grid
                            container
                            direction="row"
                            justify="flex-start"
                            alignItems="flex-start">
                            <NewsFilter newsSources={metadata.sources}
                                        handleFilterItem={this.handleFilterItem}
                                        selectedSources={selectedSources}
                                        query={query}/>
                        </Grid>


                        <Grid container spacing={10} style={{marginTop: 10}} direction="row" alignItems="flex-start">
                            <Divider/>
                            {

                                Object.entries(currentArticles).slice(offset, offset + 6).map(function (article) {
                                    let url_key = article[0]
                                    let art_item = article[1]
                                    if (selectedSources.indexOf(art_item.name) > -1) {


                                        return <Grid item xs>
                                            <NewsCard key={url_key} image={art_item.image}
                                                      heading={art_item.title}
                                                      body={art_item.summary}
                                                      url={art_item['articleLink']}/>
                                        </Grid>
                                    }


                                })
                            }
                        </Grid>
                        <Divider/>

                        <Box component="span">
                            <Pagination
                                count={Math.ceil(totalItems / pageCount)}
                                page={currentPage}
                                onChange={this.handleChange}
                                defaultPage={1}
                                color="primary"
                                size="large"
                                showFirstButton
                                showLastButton
                                classes={{ul: classes.paginator}}
                            />
                        </Box>
                    </Container>
                    </ScrollToTop>
                </div>
            )
        }
    }
}


export default withStyles(styles, {withTheme: true})(NewsArticles);