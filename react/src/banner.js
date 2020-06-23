import React from 'react';

export function Banner() {
    return (
        <div className="body-style">
            <div className="left-side">
                <p>Team Settings:</p>
            <label for="team">Team Name:</label>
            <input type="text" id="team" team="team" required
            minLength="4" maxLength="16" size="20"></input>
                <p >Choose Highlight Colors:</p> 
            <div className="way-values">
                <label for="linecolor"> Line Color: </label> 
                <input type="color" id="linecolor" name="linecolor" value="#FF0000"></input>
                <label for="linewidth">Line Width:</label>
                <input type="number" id="lindewidth" name="linewidth" min="1" max="20"></input>
                <label for="nodecolor"> Node Color: </label> 
                <input type="color" id="nodecolor" name="nodecolor" value="#0000FF"></input>
                <label for="nodesize">Node Size:</label>
                <input type="number" id="nodesize" name="nodesize" min="10" max="50"></input>
                </div>
                <label for="nodeshape" >Node Shape:</label>
                <div className="ebtns-container">
                 <button class="ebtns" type="button" >Circle</button> 
                 <button class="ebtns" type="button" >Triangle</button> 
                 <button class="ebtns" type="button" >Square</button>
                 <button class="ebtns" type="button" >Pentagon</button>
                 <button class="ebtns" type="button" >Hexagon</button>
                 <button class="ebtns" type="button" >Heptagon</button>
                 <button class="ebtns" type="button" >Octagon</button>
                 <button class="ebtns" type="button" >Nonagon</button>
                 <button class="ebtns" type="button" >Decagon</button>
                 </div>
            </div>
            <div className="editor-settings">
                <p>Editor Settings</p>
                <label for="editorname">Editor Name:</label>
                <input type="text" id="editorname" editorname="editorname" required minLength="4" maxLength="16" size="20"></input>
                <label for="editoruid">Editor User ID:</label>
                <input type="text" id="editoruid" editorname="editoruid" required minLength="4" maxLength="16" size="20"></input>
                <div className="ace-container">
                <button class="eshape-buttons" type="button" > Add </button>
                <button class="eshape-buttons" type="button" > Clear </button>
                <button class="eshape-buttons" type="button" > Edit </button>
                </div>
            <div className="editor-way">
                <label for="linecolor"> Line Color: </label> 
                <input type="color" id="linecolor" name="linecolor" value="#FF0000"></input>
                <label for="linewidth">Line Width:</label>
                <input type="number" id="lindewidth" name="linewidth" min="1" max="20"></input>
                <label for="nodecolor"> Node Color: </label> 
                <input type="color" id="nodecolor" name="nodecolor" value="#0000FF"></input>
                <label for="nodesize">Node Size:</label>
                <input type="number" id="nodesize" name="nodesize" min="10" max="50"></input>
                </div>
                </div>
                <div className="uidcheckbox"> 
                <label for="toggleUID">Toggle User ID in the Menu </label>
                <input type="checkbox" id="toggleUID" name="toggle" ></input>
                <label for="nodeshape" >Node Shape:</label>
                <div className="eshape-container">
                <button class="eshape-buttons" type="button" >Circle</button> 
                <button class="eshape-buttons" type="button" >Triangle</button> 
                <button class="eshape-buttons" type="button" >Square</button>
                <button class="eshape-buttons" type="button" >Pentagon</button>
                <button class="eshape-buttons" type="button" >Hexagon </button>
                <button class="eshape-buttons" type="button" >Heptagon</button>
                <button class="eshape-buttons" type="button" >Octagon</button>
                <button class="eshape-buttons" type="button" >Nonagon</button>
                <button class="eshape-buttons" type="button" >Decagon</button>
                </div>
            </div>
            <div className="m-container">
            <p>Table Settings</p>
            <button class="export-buttons" type="button" >Remove</button>
            <button class="export-buttons" type="button" >Remove All</button>
            <button class="export-buttons" type="button" >Import</button>
            <button class="export-buttons" type="button" >Export</button>
            </div>
            </div>
    );
}