
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


  function onChange(e) 
{

  let files = e.target.files
  let infile = files[0]
  let formData = new FormData();
  formData.append("infile", infile);
  const request = async () => {
  const response =  await fetch('/parse', {method:"POST", body: formData})
  if(response.ok){
    const obj= await response.text()
  }}
  request();
  };   


  export const FileButton= () => {
     
    const fileInput = React.useRef();       
      return (
        <>
          <div>
            <Button type='file' name='file'onClick={()=>fileInput.current.click()}>Upload</Button>
            <Button type='file' name='file'>Export</Button>
          </div>
          <input 
          ref={fileInput} 
          onChange={(e)=>onChange(e)}
          type="file" 
          style={{ display: 'none' }} 
        />    
        </>
      );
    }