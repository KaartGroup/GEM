import React from 'react';
import styled from "styled-components";

const theme = {
  blue: {
    default: "#3f51b5",
    hover: "#283593"
  },
  white:{
    default: "#ffffff",
    hover: "#fafafa"
  }

};

const Button = styled.button`
background-color: ${(props) => theme[props.theme].default};
color: white;
width:20;
height:20;
padding: 5px 5px;
border-radius: 5px;
outline: 0;
text-transform: uppercase;
margin: 0px 0px;
cursor: pointer;
box-shadow: 0px 2px 2px lightgray;
transition: ease background-color 250ms;
&:hover {
  background-color: ${(props) => theme[props.theme].hover};
}`;

Button.defaultProps = {
  theme: "blue"
};

export const NodeShapeMenu =(props)=> {


const changeShape = (e) => {
    props.action(e,"NodeShape")
}

const toggleShowMenu = ()=>{ 

if (props.ShowMenu===true){
   props.action(false,"ShowShapeMenu")
}else{
   props.action(true,"ShowShapeMenu")
}
}


    if (props.ShowMenu){
    return (
      <>
      <div>
      <label> Node Shape:</label>
      </div>
      <div className="ShapeMenu">
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/circle.png')}><img className="NodeIcons" src={'/icons/circle.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/triangle.png')}><img className="NodeIcons" src={'/icons/triangle.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/square.png')}><img className="NodeIcons" src={'/icons/square.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/pentagon.png')}><img className="NodeIcons" src={'/icons/pentagon.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/hexagon.png')}><img className="NodeIcons" src={'/icons/hexagon.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/heptagon.png')}><img className="NodeIcons" src={'/icons/heptagon.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/octagon.png')}><img className="NodeIcons" src={'/icons/octagon.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/nonagon.png')}><img className="NodeIcons" src={'/icons/nonagon.png'} style={{'background-color':props.color}} alt=""/></Button>
        <Button style={{'background-color':'White'}}onClick={()=>changeShape('/icons/decagon.png')}><img className="NodeIcons" src={'/icons/decagon.png'} style={{'background-color':props.color}} alt=""/></Button>
      </div>
      <div>
        <Button onClick={toggleShowMenu}>Close</Button>
      </div>
      </>
    )}else{
      return (
        <>
        <div>
        <label className="LineColorLabel"> Node Shape:</label>
        </div>
        <img className="NodeIcons" src={props.src} style={{'background-color':props.color}} alt=""/>
        <div>
        <Button onClick={toggleShowMenu}>Open</Button>
        </div>
         </>
      )
    }
}
