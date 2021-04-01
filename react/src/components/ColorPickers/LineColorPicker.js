import zIndex from '@material-ui/core/styles/zIndex';
import { LineWidthWrapper } from 'components/Spinners/LineWidthSpin';
import React from 'react';
import { SketchPicker, } from 'react-color';
import styled from "styled-components";


export const Button = styled.button`
  box-sizing: inherit;
  font-family: sans-serif;
  font-size: 100%;
  line-height: 1.15;
  min-width: 5vw;
  height: 4vh;
  overflow: visible;
  text-transform: none;
  border-radius: 6px;
  margin-top: 1em;
  margin-bottom: 1em;
  background-color: #f4753c;
  color: white;
  border: none;
  cursor: ${(props) => (props.disabled ? "not-allowed" : "pointer")};
  &:hover {
    background-color: ${(props) => (props.disabled ? "gray" : "#c85823")};
    color: black;
    background-color:  #ffff;
    border: 2px solid #f4753c;
  }
`;

export const LineColorWrapper = styled.div`
  display: flex;
  padding: 3%;
  flex-direction: column;
`;

export const LineColorPicker =(props)=> {


const changeColor = (color) => {
  props.action(color.hex,"LineColor")
}


const toggleShowPicker = ()=>{
  if (props.showMenu){
    props.action(false,"ShowLineColorMenu")
}else{
    props.action(true,"ShowLineColorMenu")
}
}
    if (props.showMenu){
    return (
      <>
      <LineColorWrapper>
      <label > Line Color:</label>
        <SketchPicker  disableAlpha={true} color={props.color}onChange={ changeColor }/>
        <Button  onClick={toggleShowPicker}>Close</Button>
        </LineColorWrapper>
      </>
    )}else{
      return (
        <>
        <LineColorWrapper>
        <label > Line Color:</label>
        <img className="NodeIcons" src={null} style={{backgroundColor:props.color}} alt=""/>
        <Button  onClick={toggleShowPicker}>Open</Button>
        </LineColorWrapper>
         </>
      )
    }
}

