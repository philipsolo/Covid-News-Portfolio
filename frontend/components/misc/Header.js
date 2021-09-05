import React, {useState} from "react";
import {makeStyles} from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import {Link, NavLink, useLocation} from 'react-router-dom';
import useScrollTrigger from '@material-ui/core/useScrollTrigger';
import Slide from '@material-ui/core/Slide';
import {SwipeableDrawer, Tab, Tabs} from "@material-ui/core";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import DynamicFeedIcon from '@material-ui/icons/DynamicFeed';

const useStyles = makeStyles((theme) => ({
    list: {
        width: 250,
    },
    fullList: {
        width: 'auto',
    },
    tabs: {
        display: 'none',
        [theme.breakpoints.up('md')]: {
            display: 'block',
        }
    }
    ,
    menuButton: {
        marginRight: theme.spacing(2),
        display: 'block',
        [theme.breakpoints.up('md')]: {
            display: 'none',
        }
    },
    title: {
        flexGrow: 1
    },
    offset: theme.mixins.toolbar
}));

function HideOnScroll(props) {
    const {children, window} = props;
    const trigger = useScrollTrigger({target: window ? window() : undefined});

    return (
        <Slide appear={false} direction="down" in={!trigger}>
            {children}
        </Slide>
    );
}


function Header(props) {
    const classes = useStyles();
    const [state, setState] = React.useState({
        activeTab: 'default'
    });


    const toggleDrawer = (anchor, open) => (event) => {
        if (event && event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }

        setState({...state, [anchor]: open});
    };

    const links = {'/': 0, '/news': 1}
    let location = useLocation();
    const [value, setValue] = React.useState(links[location.pathname]);


    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const anchorItems = (anchor) => (
        <div
            className={anchor}
            role="presentation"
            onClick={toggleDrawer(anchor, false)}
            onKeyDown={toggleDrawer(anchor, false)}
        >
            <List>
                <ListItem button to='/' component={Link}>
                    <ListItemIcon><DashboardIcon/> </ListItemIcon>
                    <ListItemText primary={'News'}/>
                </ListItem>
                <ListItem button to='/Covid' component={Link}>
                    <ListItemIcon><DynamicFeedIcon/> </ListItemIcon>
                    <ListItemText primary={'Covid'}/>
                </ListItem>

            </List>
        </div>
    );


    return (
        <React.Fragment>
            <HideOnScroll {...props}>
                <AppBar color={"inherit"}>
                    <Toolbar>

                        <IconButton
                            onClick={toggleDrawer('top', true)}
                            edge="start"
                            className={classes.menuButton}
                            color="inherit"
                            aria-label="menu">
                            <MenuIcon/>
                        </IconButton>
                        <SwipeableDrawer
                            anchor={'top'}
                            open={state['top']}
                            onClose={toggleDrawer('top', false)}
                            onOpen={toggleDrawer('top', true)}
                        >
                            {anchorItems('top')}
                        </SwipeableDrawer>

                        <Tabs
                            className={classes.tabs}
                            value={value}
                            onChange={handleChange}
                            indicatorColor="primary"
                            textColor="primary"
                        >


                            <Tab label='Covid-19' key={''} to='/' component={NavLink}/>
                            <Tab label='News' key={'news'} to='/news' component={NavLink}/>

                        </Tabs>


                    </Toolbar>
                </AppBar>
            </HideOnScroll>
            <Toolbar/>
        </React.Fragment>
    );
}

export default Header