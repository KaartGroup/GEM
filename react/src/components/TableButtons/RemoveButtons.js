
import React, { useState, useContext } from "react";
import styled from "styled-components";
import { DataContext } from "../../common/DataContext";
export var inEditName;
var inEditName;
var outJson;


const theme = {
    blue: {
      default: "#3f51b5",
      hover: "#283593"
    }
  };

const Button = styled.button`
  background-color: ${(props) => theme[props.theme].default};
  color: white;
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


export const RemoveButtons= (props) => {    
  
  
const RemoveAll =()=>{
  props.action(null,"RemoveAll")
}

const removeEditor=()=>{
    props.action(null,"RemoveEditor")
  }


        return (
            <>
                    <Button onClick={removeEditor}>Remove</Button>
                    <Button onClick={RemoveAll}>Remove All</Button>
            </>
        );
}