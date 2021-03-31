import React from "react";
import "./styles.css";

export const UserNameField =(props)=> {

  const ChangeUserName = (text) => {
    props.action(text.target.value,"UserName")
}
    return (
        <div className="OSMUsername">OSM Username:
            <input style={{display: 'flex'}}
              name="uname"
              type="text"
              value={props.value}
              onChange={ChangeUserName}
            />
        </div>
    );
}
