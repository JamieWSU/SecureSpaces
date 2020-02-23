import React from 'react';
import { Image, Button, Card, ButtonToolbar, ToggleButtonGroup, ToggleButton } from 'react-bootstrap';
import './App.css';


class App extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      file: null
    }
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(event) {
    this.setState({
      file: URL.createObjectURL(event.target.files[0])
    })
  }
  render() {
    return (
      <div className="App">
        <Image src={this.state.file} thumbnail />
        <br />
        <Image className='upload' src={"https://simpleicon.com/wp-content/uploads/cloud-upload-1.png"} />
        <br />
        <Button>
          <input type="file" onChange={this.handleChange} name="file" id="file" class="inputfile" />
          <label for="file">Upload Image</label>
        </Button>
        <hr />
        <ButtonToolbar className={"radiobutton"}>
          <ToggleButtonGroup type="radio" name="options" defaultValue={1}>
            <ToggleButton value={1}>Intruder</ToggleButton>
            <ToggleButton value={2}>Authorized</ToggleButton>
          </ToggleButtonGroup>
        </ButtonToolbar>
      </div>
    );
  }
}

export default App;
