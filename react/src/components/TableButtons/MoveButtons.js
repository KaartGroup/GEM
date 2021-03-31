
import React from "react";
import styled from "styled-components";

// const Button = styled.button`
//   background-color: #f4753c;
//   color: white;
//   display: flex;
//   font-size: 13px;
//   text-align: center;
//   width: 4vw;
//   padding: .75% 2%;
//   border-radius: 5px;
//   outline: 0;
//   font-family: "Hind Guntur", sans-serif;
//   cursor: pointer;
//   box-shadow: 0px 2px 2px lightgray;
//   transition: ease background-color 250ms;
//   border-color: #f4753c;
//   &:hover {
//     background-color: #fffdfd;
//     color: black;
//   }`;

export const Button = styled.button`
  box-sizing: inherit;
  font-family: sans-serif;
  font-size: 100%;
  text-align: center
  line-height: 1.15;
  width: 5vw;
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