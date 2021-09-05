import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Header from "./components/misc/Header";
import PageNotFound from "./components/misc/PageNotFound";
import NewsArticles from "./components/news/NewsArticles";
import CovidDash from "./components/covid/CovidDash";

ReactDOM.render(
    <div>
        <BrowserRouter>
            <Header/>
            <Switch>
                <Route exact path="/" component={NewsArticles} />
                <Route path="/news" component={CovidDash} />
                <Route component={PageNotFound}/>
            </Switch>
        </BrowserRouter>
    </div>,
    document.getElementById("react-root")
);