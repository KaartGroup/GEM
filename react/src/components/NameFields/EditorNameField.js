import React, { Component } from "react";
export const EditorNameField = (props) => {
const handleChangeComplete = (text) => {
    props.action(text.target.value,"EditorName")
}
    return (
        <div >Editor Name:  
            <input
              name="fname"
              type="text"
              value={props.value}
              onChange={handleChangeComplete}
            />
        </div>
    );
}

