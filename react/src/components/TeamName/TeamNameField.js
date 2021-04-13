import React, { Component } from "react";

export class TeamNameField extends Component {
  constructor() {
    super();
    this.state = {
    };

  }

  handleChangeComplete = (text) => {
    this.setState({ value: text.target.value}, ()=>{
    this.props.action(this.state.value,"TeamName")
        })
}


  render() {
    return (
        <div>
            <input
            style={{maxWidth:'90%'}}
              name="uname"
              type="text"
              value={this.props.value}
              onChange={this.handleChangeComplete}
            />
        </div>
    );
  }
}
