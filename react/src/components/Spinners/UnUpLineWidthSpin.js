import React, { Component } from "react";
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

  export const UnUpLineWidthSpin=(props)=> {


  const add = () => {
    props.action("","+UnUpLineWidth");
}
  const subtract= () => {
    props.action("","-UnUpLineWidth");
}
        return (
            <>
                <div>Line Width:
                    <input
                    type="numeric"
                    value={props.num}
                    />
                    <Button onClick={add}>+</Button>
                    <Button onClick={subtract}>-</Button>
                </div>
            </>
        );
}