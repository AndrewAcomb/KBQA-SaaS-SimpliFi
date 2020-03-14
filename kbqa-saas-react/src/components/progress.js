import React from 'react'
import Pusher from 'pusher-js'
import '../termynal/termynal.css'
import '../termynal/termynal.js'


const app_id = "960906"
const key = "d18ed2e42cf337876806"
const secret = "ffd3ef254ef8617ab31a"
const cluster = "us2"



export default class Progress extends React.Component {
    state = {
    loading: false,
    progress: [],
    };

    componentDidMount() {

    const pusher = new Pusher(key, {
        cluster: cluster,
        encrypted: false,
    });

    const channel = pusher.subscribe('pipeline')

    channel.bind('progress', data => {
        
        if (this.state.progress.length < 7){
            this.setState(state => ({
                progress: [...state.progress, data.message],
                }));
        }
        else{
            this.setState(state => ({
                progress: [...state.progress.slice(1, state.progress.length), data.message],
                }));

        }
    });}



    render(){

        if (this.state.progress.length == 0) return null;
        return(

            <div id="#termynal" data-termynal data-termynal data-ty-typedelay="40" data-ty-linedelay="700" data-ty-cursor="▋" linedata = {this.state.progress}>
                <script src="termynal.js" data-termynal-container="#termynal"></script>
                {this.state.progress.map((item, index) =>
                    <span data-ty="input" data-ty-prompt="▲" key={index} typeDelay = '40'>{item}</span>
                )}

            </div>
        );
    }
} 