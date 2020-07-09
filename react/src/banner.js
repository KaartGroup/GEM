import React from 'react';
import $ from 'jquery';

var tlinecolor;
var tnodecolor;
var elinecolor;
var enodecolor;
var tlcolor = '#0000ff';
var tncolor = '#ff0000';
var elcolor = '#ff0000';
var encolor = '#0000ff';

window.addEventListener("load", startup, false);

function startup(){
    tlinecolor = document.querySelector("#tlinecolor");
    tlinecolor.value = tlcolor;
    //linecolor.addEventListener("input", updateFirst,false);
    //linecolor.addEventListener("change", updateAll, false);
    tlinecolor.select(tlcolor);

    tnodecolor = document.querySelector("#tnodecolor");
    tnodecolor.value = tncolor;
    tnodecolor.select(tncolor);

    elinecolor = document.querySelector("#elinecolor");
    elinecolor.value = elcolor;
    elinecolor.select(elcolor);

    enodecolor = document.querySelector("#enodecolor");
    enodecolor.value = encolor;
    enodecolor.select(encolor);    
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
$(document).ready(function(){
  
  (function($){
      $.fn.serializeFormJSON = function (){
          
          var o = {};
          var a = this.serializeArray();
          $.each(a, function(){
              if(o[this.name].push){
                  if (!o[this.name].push){
                      o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';    
                }
            });
            return o;
        };
    })($);


  $('iform').submit(function(e){
      e.preventDefault();
      var data = $(this).serializeFormJSON();
      console.log(data);
  });

    $("#add").click(function(){
        var x = $("form").serializeArray();
        $.each(x, function(i, field){
            $("#output").append(field.name + ":" 
                        + field.value + " ");
        });
    });
});

export function Banner() {
    return (
    <div className="body-style">
    <form actions=""  id="iform" className="form">
    <div className="left-side">
        <p>Team Settings: </p>
    <label for="team">Team Name:</label>
    <input type="text" id="team" name="team" placeholder="Enter a Team Name" required minLength="4" maxLength="16" size="20"></input>
        <p >Choose Highlight Colors:</p> 
        <div className="way-values">
        <label for="tlinecolor"> Line Color: </label> 
        <input type="color" id="tlinecolor" name="tlinecolor" ></input>
        <label for="tlinewidth">Line Width:</label>
         <input type="number" id="tlindewidth" name="tlinewidth" min="1" max="20" placeholder="1"></input>
        <label for="tnodecolor"> Node Color: </label> 
            <input type="color" id="tnodecolor" name="tnodecolor"  ></input>
        <label for="tnodesize">Node Size:</label>
        <input type="number" id="tnodesize" name="tnodesize" min="10" max="50" placeholder="10"></input> </div>
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
            <input type="text" id="editoruid" name="uid" placeholder="Enter a User ID" required minLength="4" maxLength="16" size="20"></input>
    <div className="editor-way">
        <label for="elinecolor"> Line Color: </label> 
        <input type="color" id="elinecolor" name="elinecolor" ></input>
        <label for="elinewidth">Line Width:</label>
        <input type="number" id="elinewidth" name="elinewidth" min="1" max="20" placeholder="1"></input>
        <label for="enodecolor"> Node Color: </label> 
        <input type="color" id="enodecolor" name="enodecolor" ></input>
        <label for="enodesize">Node Size:</label>
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
        <button id="add" class="export-buttons" type="submit"> Add User</button>
        <button class="export-buttons" type="button" >Remove</button>
        <button class="export-buttons" type="button" >Remove All</button>
        <button class="export-buttons" type="button" >Export</button>
        </div>
        </form>
        <div id="output"></div>
    <div className="ebtns-container">                     
        <form  id="upload-form" className = "form" action="/upload" method="POST" encType="multipart/form-data">
        <input type="file" name="upfile" id="upfile"></input>
        <button class="export-buttons" type="submit" >Import</button>
        </form>
        </div>
        </div>
    );
}