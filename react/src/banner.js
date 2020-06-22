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
            <div className="shape-buttons"> 
                <input class="button-container" type="button" value="Circle"></input> 
                <input class="button-container" type="button" value="Triangle"></input> 
                <input class="button-container" type="button" value="Square"></input>
                <input class="button-container" type="button" value="Pentagon"></input>
                <input class="button-container" type="button" value="Hexagon"></input>
                <input class="button-container" type="button" value="Heptagon"></input>
                <input class="button-container" type="button" value="Octagon"></input>
                <input class="button-container" type="button" value="Nonagon"></input>
                <input class="button-container" type="button" value="Decagon"></input></div>
                </div>
            <div className="editor-settings">
                <p>Editor Settings</p>
                <label for="editorname">Editor Name:</label>
                <input type="text" id="editorname" editorname="editorname" required minLength="4" maxLength="16" size="20"></input>
                <label for="editoruid">Editor User ID:</label>
                <input type="text" id="editoruid" editorname="editoruid" required minLength="4" maxLength="16" size="20"></input>
                <div><button class="eshape-buttons" type="button" >Add</button></div>
                <div><button class="eshape-buttons" type="button" >Clear</button></div>
                <div><button class="eshape-buttons" type="button" >Edit</button></div>
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
                <div><button class="eshape-buttons" type="button" >Circle</button> </div>
                <div><button class="eshape-buttons" type="button" >Triangle</button> </div>
                <div><button class="eshape-buttons" type="button" >Square</button></div>
                <div><button class="eshape-buttons" type="button" >Pentagon</button></div>
                <div><button class="eshape-buttons" type="button" >Hexagon</button></div>
                <div><button class="eshape-buttons" type="button" >Heptagon</button></div>
                <div><button class="eshape-buttons" type="button" >Octagon</button></div>
                <div><button class="eshape-buttons" type="button" >Nonagon</button></div>
                <div><button class="eshape-buttons" type="button" >Decagon</button></div>
                </div>
    </div>
    );
}