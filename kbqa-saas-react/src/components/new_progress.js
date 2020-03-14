
import { Progress } from 'antd';
import React from 'react'
import Pusher from 'pusher-js';

const app_id = "960906"
const key = "d18ed2e42cf337876806"
const secret = "ffd3ef254ef8617ab31a"
const cluster = "us2"

export default class Progress extends React.Component {
    state = {
    loading: false,
    progress: ["No progress yet"],
    data_parsed: 0,
    config_updated: 0,
    

    };

    componentDidMount() {

    const pusher = new Pusher(key, {
        cluster: cluster,
        encrypted: false,
    });

    const channel = pusher.subscribe('pipeline')

    channel.bind('progress', data => {
        this.setState(state => ({
        progress: [...state.progress, data.message],
        }));

    });}

    render(){
        return(
            <div>>
                <Progress percent={75} />
                <Progress percent={70} status="exception" />
                <Progress percent={100} />
            </div>
        );
    }
} 