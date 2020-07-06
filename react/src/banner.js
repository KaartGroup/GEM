import React from 'react';

var linecolor;
var nodecolor;
var elinecol;
var enodecol;
var lcolor = '#0000ff';
var ncolor = '#ff0000';
var elcolor = '#ff0000';
var encolor = '#0000ff';

window.addEventListener("load", startup, false);

function startup(){
    linecolor = document.querySelector("#linecolor");
    linecolor.value = lcolor;
    //linecolor.addEventListener("input", updateFirst,false);
    //linecolor.addEventListener("change", updateAll, false);
    linecolor.select(lcolor);

    nodecolor = document.querySelector("#nodecolor");
    nodecolor.value = ncolor;
    nodecolor.select(ncolor);

    elinecol = document.querySelector("#elinecolor");
    elinecol.value = elcolor;
    elinecol.select(elcolor);

    enodecol = document.querySelector("#enodecolor");
    enodecol.value = encolor;
    enodecol.select(encolor);    
}

function updateFirst(event) {
    var p = document.querySelector("p");
    var b = document.querySelector("button");

    if(b){
        b.style.background = event.target.value
    }

    if (p) {
        
        p.style.color = event.target.value;
    }
  }

function updateAll(event) {
    document.querySelectorAll("button").forEach(function(b){
        b.style.background = event.target.value

    });
    document.querySelectorAll("p").forEach(function(p) {
        p.style.color = event.target.value;
    });
  }

export function Banner() {
    return (
    
    <div className="body-style">
    <form action="/add" method="POST" className='form' >
    <div className="left-side">
        <p>Team Settings: </p>
    <label for="team">Team Name:</label>
    <input type="text" id="team" name="team" placeholder="Enter a Team Name" required minLength="4" maxLength="16" size="20"></input>
        <p >Choose Highlight Colors:</p> 
        <div className="way-values">
        <label for="linecolor"> Line Color: </label> 
        <input type="color" id="linecolor" name="tlinecolor" ></input>
        <label for="linewidth">Line Width:</label>
         <input type="number" id="lindewidth" name="tlinewidth" min="1" max="20" placeholder="1"></input>
        <label for="nodecolor"> Node Color: </label> 
            <input type="color" id="nodecolor" name="tnodecolor"  ></input>
        <label for="nodesize">Node Size:</label>
        <input type="number" id="nodesize" name="tnodesize" min="10" max="50" placeholder="10"></input> </div>
        <label for="tnodeshape" >Node Shape:</label>
        <select name = "tnodeshape">
            <option value="">--Please Select an Option--</option>
            <option value="circle">Circle</option>
            <option value="triangle">Traingle</option>
            <option value="square">Square</option>
            <option value="pentagon">Pentagon</option>
            <option value="hexagon">Hexagon</option>
            <option value="heptagon">Heptagon</option>
            <option value="octagon">Octagon</option>
            <option value="nonagon">Nonagon</option>
            <option value="decagon">Decagon</option>
            </select>
            </div>
    <div className="editor-settings">
        <p>Editor Settings</p>
            <label for="ename">Editor Name:</label>
            <input type="text" id="ename" placeholder="Enter an Editor's Name" name="ename" required minLength="4" maxLength="16" size="20"></input>
            <label for="username">User Name:</label>
            <input type="text" id="username" placeholder="Enter a Username" name="username" required minLength="4" maxLength="16" size="20"></input>
            <label for="editoruid">User ID:</label>
            <input type="text" id="editoruid" name="editoruid" placeholder="Enter a User ID" required minLength="4" maxLength="16" size="20"></input>
    <div className="editor-way">
        <label for="linecolor"> Line Color: </label> 
        <input type="color" id="elinecolor" name="elinecolor" ></input>
        <label for="linewidth">Line Width:</label>
        <input type="number" id="elinewidth" name="elinewidth" min="1" max="20" placeholder="1"></input>
        <label for="nodecolor"> Node Color: </label> 
        <input type="color" id="enodecolor" name="enodecolor" ></input>
        <label for="nodesize">Node Size:</label>
        <input type="number" id="enodesize" name="enodesize" min="10" max="50" placeholder="10"></input>
        </div>
        <label for="enodeshape" >Node Shape:</label>
        <select name = "enodeshape">
            <option value="">--Please Select an Option--</option>
            <option value="circle">Circle</option>
            <option value="triangle">Traingle</option>
            <option value="square">Square</option>
            <option value="pentagon">Pentagon</option>
            <option value="hexagon">Hexagon</option>
            <option value="heptagon">Heptagon</option>
            <option value="octagon">Octagon</option>
            <option value="nonagon">Nonagon</option>
            <option value="decagon">Decagon</option>
        </select>
        </div>
    <p>Table Settings</p>
    <div className="ebtns-container">
        <button class="export-buttons" type="submit">Submit</button>
        <button class="export-buttons" type="button" >Remove</button>
        <button class="export-buttons" type="button" >Remove All</button>
        <button class="export-buttons" type="button" >Export</button>
        </div>
        </form>
    <div className="ebtns-container">                     
        <form  id="upload-form" className = "form" action="/upload" method="POST" encType="multipart/form-data">
        <input type="file" name="upfile" id="upfile"></input>
        <button class="export-buttons" type="submit" >Import</button>
        </form>
        </div>
        </div>
    );
}