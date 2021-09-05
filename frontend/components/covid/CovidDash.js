import React from 'react';
import {Paper} from "@material-ui/core";

class CovidDash extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
    }
    componentDidMount() {
        console.log("Fetching Covid")
        // fetch("/covid/get_our_world")
        //     .then(res => res.json())
        //     .then(
        //         (result) => {
        //             this.setState({
        //                 isLoaded: true,
        //                 items: result
        //             });
        //         },
        //         (error) => {
        //             this.setState({
        //                 isLoaded: true,
        //                 error
        //             });
        //         }
        //     )
        let result = [];
        this.setState({
            isLoaded: true,
            items: result
        });
    }
    render() {
        const {error, isLoaded, items} = this.state
        console.log(items)
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (

                <Paper  zDepth={5} circle >
                    <div style={{margin: '40% 0 0 35%', position: 'absolute'}}>
                        ABC
                    </div>
                </Paper>



            )
        }
    }
}

export default CovidDash;