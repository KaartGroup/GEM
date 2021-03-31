import React, { Component } from "react";
import styled from "styled-components";

export const Button = styled.button`
box-sizing: inherit;
font-family: sans-serif;
font-size: 100%;
line-height: 1.15;
width: 2vw;
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


export const UnUpNodeSizeWrapper = styled.div`
border-TOP: 2px solid #f4753c;
display: flex;
padding: 1%;
align-items: center;
flex-direction: row;
justify-content: space-around;
`;

export const UnUpNodeSizeSpin =(props)=>{
 const add = () => {
    props.action("","+UnUpNodeSize");
}
 const  subtract= () => {
    props.action("","-UnUpNodeSize");
}
        return (
            <>
                <UnUpNodeSizeWrapper>
                  Node Size :
                    <input
                        style={{maxWidth: '15%', textAlign:'center'}}
                    type="numeric"
                    value={props.num}
                    />
                    <Button onClick={subtract}>-</Button>
                    <Button onClick={add}>+</Button>
                    </UnUpNodeSizeWrapper>
            </>
        );
}