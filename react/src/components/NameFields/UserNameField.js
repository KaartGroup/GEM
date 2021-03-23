import React, { Component } from "react";

export const UserNameField =(props)=> {

  const ChangeUserName = (text) => {
    props.action(text.target.value,"UserName")
}
    return (
        <div>User Name:
            <input
              name="uname"
              type="text"
              value={props.value}
              onChange={ChangeUserName}
            />
        </div>
    );
}
