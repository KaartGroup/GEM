import React, { useState, useContext } from "react";
import styled from "styled-components";
export var inEditName;
var inEditName;

export const Button = styled.button`
  box-sizing: inherit;
  font-family: sans-serif;
  font-size: 100%;
  text-align: center
  line-height: 1.15;
  min-width: 5vw;
  max-width: 11vw;
  height: 5vh;
  overflow: visible;
  text-transform: none;
  border-radius: 6px;
  margin-top: 1em;
  margin-bottom: 1em;
  background-color: #f4753c;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: ${(props) => (props.disabled ? "not-allowed" : "pointer")};
  &:hover {
    background-color: ${(props) => (props.disabled ? "gray" : "#c85823")};
    color: black;
    background-color:  #ffff;
    border: 2px solid #f4753c;
  }
`;

export const RemoveButtons= (props) => {    
  
const RemoveAll =()=>{
  props.action(null,"RemoveAll")
}

const removeEditor=()=>{
    props.action(null,"RemoveEditor")
  }

   return (
       <>
               <Button onClick={removeEditor}>Delete Editor</Button>
               <Button onClick={RemoveAll}>Delete All</Button>
       </>
   );
}