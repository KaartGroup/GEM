import React from 'react';
import styled from "styled-components";

export const Button = styled.button`
  box-sizing: inherit;
  font-family: sans-serif;
  font-size: 100%;
  line-height: 1.15;
  min-width: 5vw;
  max-width: 10vw;
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

export const UnUpNodeShapeIconWrapper = styled.div`
  display: grid;
  grid-template-columns: 50% 50% 50%;
  max-width: 25vh;
`;

export const UnUpNodeShapeWrapper = styled.div`
  border-TOP: 2px solid #f4753c;
  display: flex;
  padding: 3%;
  flex-direction: column;
`;

export const UnUpNodeShapeMenu =(props)=> {


const changeShape = (e) => {
  props.action(e,"UnUpNodeShape")

}

const CloseMenu= ()=>{
  props.action(false,"ShowUnUpShapeMenu")
}

const toggleShowMenu = ()=>{ 
  if (props.ShowMenu){
     props.action(false,"ShowUnUpShapeMenu")
  }else{
     props.action(true,"ShowUnUpShapeMenu")
  }
}

    if (props.ShowMenu){
    return (
      <>
      <UnUpNodeShapeWrapper>
      <label> Node Shape:</label>
      
      <UnUpNodeShapeIconWrapper>
      <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/circle.png')}><img className="NodeIcons" src={'/icons/circle.png'} style={{'background-color':props.color}} alt=""/>Circle</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/triangle.png')}><img className="NodeIcons" src={'/icons/triangle.png'} style={{'background-color':props.color}} alt=""/>Triangle</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/square.png')}><img className="NodeIcons" src={'/icons/square.png'} style={{'background-color':props.color}} alt=""/>Square</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/pentagon.png')}><img className="NodeIcons" src={'/icons/pentagon.png'} style={{'background-color':props.color}} alt=""/>Pentagon</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/hexagon.png')}><img className="NodeIcons" src={'/icons/hexagon.png'} style={{'background-color':props.color}} alt=""/>Hexagon</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/heptagon.png')}><img className="NodeIcons" src={'/icons/heptagon.png'} style={{'background-color':props.color}} alt=""/>Heptagon</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/octagon.png')}><img className="NodeIcons" src={'/icons/octagon.png'} style={{'background-color':props.color}} alt=""/>Octagon</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/nonagon.png')}><img className="NodeIcons" src={'/icons/nonagon.png'} style={{'background-color':props.color}} alt=""/>Nonagon</Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/decagon.png')}><img className="NodeIcons" src={'/icons/decagon.png'} style={{'background-color':props.color}} alt=""/>Decagon</Button>
        </UnUpNodeShapeIconWrapper>
        <Button onClick={toggleShowMenu}>Close</Button>
      </UnUpNodeShapeWrapper>
      </>
    )}else{
      return (
        <>
       <UnUpNodeShapeWrapper>
        <label> Node Shape:</label>

        <img className="NodeIcons" src={props.src} style={{'background-color':props.color}} alt=""/>
      
        <Button onClick={toggleShowMenu}>Open</Button>
        </UnUpNodeShapeWrapper>
         </>
      )
    }
}
