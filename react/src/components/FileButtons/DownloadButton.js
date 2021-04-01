import React, { Component, useState } from "react";
import styled from "styled-components";

export const Button = styled.button`
  box-sizing: inherit;
  display: flex;
  font-family: sans-serif;
  font-size: 100%;
  line-height: 1.15;
  min-width: 5vw;
  height: 5vh;
  overflow: visible;
  text-transform: none;
  border-radius: 6px;
  margin-top: 1em;
  margin-bottom: 1em;
  background-color: #f4753c;
  color: white;
  padding: 14px 20px;
  border: none;
  cursor: ${(props) => (props.disabled ? "not-allowed" : "pointer")};
  &:hover {
    background-color: ${(props) => (props.disabled ? "gray" : "#c85823")};
    color: black;
    background-color:  #ffff;
    border: 2px solid #f4753c;
  }
`;

      export const DownloadButton =(props)=> {
          return (
            <>
                <Button onClick={()=>props.action(null,"Download")}>Download</Button>
            </>
          );

    }