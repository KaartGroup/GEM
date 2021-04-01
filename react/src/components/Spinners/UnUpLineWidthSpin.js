import React, { Component } from "react";
import styled from "styled-components";

export const Button = styled.button`
box-sizing: inherit;
font-family: sans-serif;
font-size: 100%;
line-height: 1.15;
min-width: 2vw;
text-align: center;
height: 3vh;
overflow: visible;
text-transform: none;
border-radius: 6px;
margin-top: 1em;
margin-bottom: 1em;
background-color: #f4753c;
color: white;
padding: 1px 1px;
border: none;
cursor: ${(props) => (props.disabled ? "not-allowed" : "pointer")};
&:hover {
  background-color: ${(props) => (props.disabled ? "gray" : "#c85823")};
  color: black;
  background-color:  #ffff;
  border: 2px solid #f4753c;
}
`;


export const UnUpLineWidthWrapper = styled.div`
display: flex;
padding: 1%;
align-items: center;
flex-direction: row;
justify-content: space-around;
`;

  export const UnUpLineWidthSpin=(props)=> {


  const add = () => {
    props.action("","+UnUpLineWidth");
}
  const subtract= () => {
    props.action("","-UnUpLineWidth");
}
        return (
            <>
                <UnUpLineWidthWrapper>
                  Line Width:
                    <input
                        style={{maxWidth: '15%', textAlign:'center'}}
                    type="numeric"
                    value={props.num}
                    />
                    <Button onClick={subtract}>-</Button>
                    <Button onClick={add}>+</Button>
                    </UnUpLineWidthWrapper>
            </>
        );
}