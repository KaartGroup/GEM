import React, { Component,useState, useContext } from "react";
import styled from "styled-components";
import { DataContext } from "../../common/DataContext";
import { Upload, EditorMenu, UploadFile, UploadForm } from "./styles";



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












export const FileButtons = (props) => {
  const { setTableData } = useContext(DataContext);
  const { fileID, } = useContext(DataContext);

    const onChange = (e) => {
        let files = e.target.files
        let infile = files[0]
        let formData = new FormData();
        formData.append("infile", infile);
        const request = async () => {
        const response =  await fetch('/parse?ID='+fileID, {method:"POST", body: formData})
        if(response.ok){
          const obj= await response.json()
          let UnUpData = obj[obj.length-1]
          obj.splice(-1,1)
          props.action(UnUpData,"UnUpData")
          // path = 
          setTableData(obj);
        }}
        request();

        };  
        
const fileInput = React.useRef();   

return(


   <>
    <Button type='file' name='file'onClick={()=>fileInput.current.click()}>Upload</Button>
          <input 
          ref={fileInput} 
          onChange={(e)=>onChange(e)}
          type="file" 
          style={{ display: 'none' }} />
    </>
    );
};