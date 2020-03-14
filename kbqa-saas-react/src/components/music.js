import React from 'react'



export default class Music extends React.Component {
    constructor(props) {
    super(props);
    this.state = {
      play: true,
      pause: false,
    }
    this.url = "https://ia601602.us.archive.org/1/items/MACINTOSHPLUS420_201705/MACINTOSH%20PLUS%20-%20%E3%83%AA%E3%82%B5%E3%83%95%E3%83%A9%E3%83%B3%E3%82%AF420%20_%20%E7%8F%BE%E4%BB%A3%E3%81%AE%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC.mp3";
    this.audio = new Audio(this.url);
  }


  render() {

    this.audio.play();

  return (
    <div>
    </div>
    );
  }
}

