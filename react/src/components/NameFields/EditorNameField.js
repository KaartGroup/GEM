import React from "react";
import "./styles.css";

export const EditorNameField = (props) => {
const handleChangeComplete = (text) => {
    props.action(text.target.value,"EditorName")
}
    return (
        <div className="EditorName" >Editor Name:  
            <input style={{display: 'flex'}}
              name="fname"
              type="text"
              value={props.value}
              onChange={handleChangeComplete}
            />
        </div>
    );
}

