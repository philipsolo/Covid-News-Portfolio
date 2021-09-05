import React from 'react';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import FilterListIcon from "@material-ui/icons/FilterList";
import {Avatar, Checkbox, ListItemAvatar, ListItemSecondaryAction, withStyles} from "@material-ui/core";


const drawerWidth = 240;

const styles = theme => ({
    root: {
        display: 'flex',
    },

    appBarShift: {
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
        }),
        marginRight: drawerWidth,
    },

    hide: {
        display: 'none',
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
    },
    drawerHeader: {
        display: 'flex',
        alignItems: 'center',
        padding: theme.spacing(0, 1),
        // necessary for content to be below app bar
        ...theme.mixins.toolbar,
        justifyContent: 'flex-start',
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing(3),
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        marginRight: -drawerWidth,
    },
    contentShift: {
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
        }),
        marginRight: 0,
    },
    listBullet: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    }
});

class NewsFilter extends React.Component {

    constructor(props) {
        super(props);
        this.handleToggle = this.handleToggle.bind(this);
        this.state = {
            open: false,
            checked: []
        }
    }

    handleToggle = (value) => () => {

        let checkmark = this.state.checked
        const currentIndex = checkmark.indexOf(value);
        const newChecked = [...checkmark];
        if (currentIndex === -1) {
            newChecked.push(value);
            this.props.handleFilterItem(newChecked)

        } else {
            newChecked.splice(currentIndex, 1);
            this.props.handleFilterItem(newChecked)
        }

        this.setState({
            checked: newChecked
        });

    };


    handleDrawerOpen = () => {
        this.setState({
            open: true
        });
    };

    handleDrawerClose = () => {
        this.setState({
            open: false
        });
    };

    handleDrawerToggle = () => {
        this.setState(prevState => ({
            open: !prevState.open
        }));
    };

    render() {
        const {open} = this.state
        const {classes,newsSources, selectedSources, query} = this.props;

        return (

            <div className={classes.root}>
                <IconButton

                    onClick={this.handleDrawerToggle}
                    aria-label="delete">
                    <FilterListIcon/>
                </IconButton>


                <Drawer
                    className={classes.drawer}
                    variant="persistent"
                    anchor="right"
                    open={open}
                    classes={{
                        paper: classes.drawerPaper,
                    }}>

                    <div className={classes.drawerHeader}>
                        <IconButton onClick={this.handleDrawerClose}>
                            <ChevronLeftIcon/>
                        </IconButton>
                    </div>

                    <Divider/>
                    <List dense className={classes.listBullet}>

                        {Object.keys(newsSources).map(function (source) {

                            const labelId = `checkbox-list-secondary-label-${source}`;

                                return (
                                    <ListItem key={source} button>
                                        <ListItemAvatar>

                                            <Avatar
                                                alt={`News Image for°${source}`}
                                                src={newsSources[source]}
                                            />

                                        </ListItemAvatar>
                                        <ListItemText id={labelId} primary={`${source}`}/>
                                        <ListItemSecondaryAction>
                                            <Checkbox
                                                edge="end"
                                                onChange={this.handleToggle(source)}
                                                checked={selectedSources.indexOf(source) > -1}
                                                inputProps={{'aria-labelledby': labelId}}
                                                disabled={query !== 'all'}
                                            />
                                        </ListItemSecondaryAction>
                                    </ListItem>
                                );

                        }, this)}
                    </List>

                </Drawer>
            </div>
        );
    }
}

export default withStyles(styles, {withTheme: true})(NewsFilter);
