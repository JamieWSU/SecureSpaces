import React from 'react';
import { Image, Button, Form, Col } from 'react-bootstrap';
import './App.css';


class App extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      file: null,
      intruder: true
    }
    this.handleChange = this.handleChange.bind(this)
    this.setAuthorized = this.setAuthorized.bind(this)
    this.setIntruder = this.setIntruder.bind(this)
    this.onChange = this.onChange.bind(this)
  }

  onChange(event) {
    this.setState({
      ...this.state,
      [event.target.name]: event.target.value
    });
  }

  setIntruder() {
    this.setState({
      ...this.state,
      intruder: true,
      name: undefined
    });
  }

  setAuthorized() {
    this.setState({
      ...this.state,
      intruder: false
    });
  }

  handleChange(event) {
    this.setState({
      ...this.state,
      file: URL.createObjectURL(event.target.files[0])
    })
  }
  render() {
    console.log(this.state.intruder)
    return (
      <div className="App">
        <Image src={this.state.file} thumbnail />
        <Form>
          <Col>
            <br />
            <Image className='upload' src={"https://image.freepik.com/free-icon/upload-document_318-8461.jpg"} />
            <br />
            <Button variant="dark">
              <input type="file" onChange={this.handleChange} name="file" id="file" class="inputfile" />
              <label for="file">Upload Image</label>
            </Button>
            <hr />
            <Button onClick={this.setIntruder} variant={this.state.intruder ? "dark" : "outline-dark"}>Intruder</Button>
            <Button onClick={this.setAuthorized} variant={this.state.intruder ? "outline-dark" : "dark"}>Authorized</Button>
            <Form.Group>
              {!this.state.intruder ? <div>
                <br />
                <Form.Control onChange={this.onChange} name="name" placeholder="Name" value={this.state.name} />
              </div> : null}
            </Form.Group>
            <hr />
            <Button variant="dark" size="lg" disabled={!this.state.file || (!this.state.name && !this.state.intruder) ? true : false}>Submit</Button>
          </Col>
        </Form>
        <br/>
      </div >
    );
  }
}

export default App;
