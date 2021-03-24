import React from 'react';
import { SketchPicker, } from 'react-color';
import styled from "styled-components";

const theme = {
  blue: {
    default: "#3f51b5",
    hover: "#283593"
  }
};

const Button = styled.button`
background-color: ${(props) => theme[props.theme].default};
color: white;
width:20;
height:20;
padding: 5px 15px;
border-radius: 5px;
outline: 0;
text-transform: uppercase;
margin: 10px 0px;
cursor: pointer;
box-shadow: 0px 2px 2px lightgray;
transition: ease background-color 250ms;
&:hover {
  background-color: ${(props) => theme[props.theme].hover};
}`;

Button.defaultProps = {
  theme: "blue"
};

export const UnUpLineColorPicker =(props)=> {

const changeColor = (color) => {
props.action(color.hex,"UnUpLineColor")
}

const toggleShowPicker = ()=>{
  if (props.showMenu){
      props.action(false,"ShowUnUpLineColorMenu")
}else{
      props.action(true,"ShowUnUpLineColorMenu")
  }
}

    if (props.showMenu){
    return (
      <>
      <div>
      <label> Line Color:</label>
      </div>
      <div >
        <SketchPicker color={props.color}onChange={ changeColor }/>
      </div>

      <div>
        <Button onClick={toggleShowPicker}>Close</Button>
      </div>
      </>
    )}else{
      return (
        <>
        <div>
        <label> Line Color:</label>
        </div>
        <div>
        <img className="NodeIcons" src={null} style={{backgroundColor:props.color}} alt=""/>
        </div>
        <div>
        <Button onClick={toggleShowPicker}>Open</Button>
        </div>
         </>
      )
    }
  };


