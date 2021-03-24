
import React, { useState } from "react";
import styled from "styled-components";
var outJson;
var url;

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


      export const MoveButtons= (props) => {
     
        const ButtonFunction = (e) => {
          if(e === "Up"){
                  props.action(null,'MoveUp')}
          else if(e === "Down"){
                  props.action(null,'MoveDown')}
            }

            


          return (
            <>
  
                <Button onClick={()=>ButtonFunction('Up')}>Move Up</Button>
                <Button onClick={()=>ButtonFunction('Down')}>Move Down</Button>

            </>
          );
        }     