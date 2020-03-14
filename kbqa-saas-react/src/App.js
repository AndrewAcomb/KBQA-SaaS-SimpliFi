import React from 'react';
import UploadProcess from './components/upload.js'
import Progress from './components/progress.js'
import Music from './components/music.js'
import './termynal/termynal.css'
// import './termynal/terminal.js'
import { white } from 'color-name';


var inputFormat = {
  "topic-entity": 
  {
    "entity": "value",
    "...":""
  },
  "...":""
}


class App extends React.Component{
  state = {
    uploaded_once: false
  }
  uploadedCallback = () => {
    this.setState({
      uploaded_once: true
    });
  }

 
  render()
  {

  if (this.state.uploaded_once == false)
  {
    return (  
      <div className="App">

        <header className="App-header"> 
        <h2 style={{'color':'white'}} >Specified Format:</h2>
        <pre style={{'color':'white'}}>
        {JSON.stringify( inputFormat, undefined, 2)}
        </pre>
        <UploadProcess uploadedPassback = {this.uploadedCallback}/>
        </header>
      </div>  
      
    );
  }
  else
  {
    return (
      <div>
      <Progress/>
      <Music/>
      </div>
    )
  }
  
  }
} 

export default App;
