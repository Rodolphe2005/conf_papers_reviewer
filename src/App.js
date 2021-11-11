import logo from './logo.svg';
import './App.css';
import React from 'react'
import axios from 'axios'
import ArrowKeysReact from 'arrow-keys-react';

class Card extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="card">
      <div className="title">
        {this.props.title}
      </div>
      <div className="abstract">
      {this.props.abstract}
    </div></div>
    );
  }
  
}

class CardsNavigation extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      user_id: 1,
      paper_id: null,
      title: null,
      abstract: null,
      content: null
    };
    this.cardsNavigationRef = React.createRef()
    ArrowKeysReact.config({
      left: () => {
        this.setState({
          content: 'left key detected.'
        });
      },
      right: () => {console.log('before this.like'); console.log(this); this.like(this.state.paper_id, this.state.user_id)},
      up: () => {
        this.setState({
          content: 'up key detected.'
        });
      },
      down: () => {
        this.setState({
          content: 'down key detected.'
        });
      }
    });
  }

  like(paper_id, user_id){
    console.log('I like it !!')
    console.log(this)
    axios.get(`http://127.0.0.1:8000/save_user_interaction/
    ${user_id}/${paper_id}/like`)
        .then(response => this.getNewPaperToReview());
  }

  getNewPaperToReview(){
    axios.get('http://127.0.0.1:8000/next_paper_to_check/1')
         .then(response => this.setState({
           paper_id: response.data.paper_id,
           title: response.data.title,
           abstract: response.data.abstract,
          }));
  }

  render(){
    return (
      <div className="CardsNavigation" {...ArrowKeysReact.events} tabIndex="1"
      ref={this.cardsNavigationRef}>
      <Card title={this.state.title} abstract={this.state.abstract}></Card>
      {this.state.content}
      </div>
    )
  }

  componentDidMount() {
    this.cardsNavigationRef.current.focus()
    // Simple GET request using axios
    this.getNewPaperToReview()
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <CardsNavigation></CardsNavigation>
      </header>
    </div>
  );
}

export default App;
