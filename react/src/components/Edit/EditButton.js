
import React, { Component,useState } from "react";
import styled from "styled-components";
var outJson;
var url;
var key;

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
  
export const EditButton = (props) => {

  const clear= () => {
    props.action(null,"Clear")
        }
  const Add=()=>{
    props.action2('add')
  }

  if(props.bool===true){
    return (

        <div>
          <Button onClick={props.action3}>Edit</Button>
          <Button onClick={Add}>Add</Button>
          <Button onClick={clear}>Clear</Button>
        </div> 

    );
  }else{
    return (

        <div>
          <Button onClick={props.action3}>Edit</Button>
          <Button onClick={()=>props.action2('update')}>Update</Button>
          <Button onClick={clear}>Clear</Button>
        </div> 

    );
  
    }
  }