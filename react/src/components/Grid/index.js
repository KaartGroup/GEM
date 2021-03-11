import React, { useState, useContext, useEffect } from "react";
import ReactGridLayout, { WidthProvider } from "react-grid-layout";
import { Editor } from "components/Editor";
// import { InteractionContext } from "common/InteractionContext";
import "./styles.css";
import { BasicTable } from "components/Table"
// import "react-tabs/style/react-tabs.css";
// import { DataContext } from "common/DataContext";

const GridLayout = WidthProvider(ReactGridLayout);

export const Grid = () => {

  var outJson;
//import {outJson} from './variables.js';
const blank = async () => {
  const response =  await fetch('/blank')
  if(response.ok){
    const obj= await response.json()
    console.log(obj)
  }}
  blank();

  const [layouts, setLayouts] = useState({});

  const onLayoutChange = (layouts) => {
    setLayouts(layouts);
  };

  const getViewHeight = () => {
    return window.innerHeight - 130;
  };

  const moveUp = ()=>{
    outJson = localStorage.getItem("outJson");
    outJson=JSON.stringify(outJson)
    const request = async () => {
    const response =  await fetch('/table?sub=moveUp', {method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
    if(response.ok){
      const object = await response.text()
      console.log(object)
    }}
    request();
  }


const remove = () => {
  outJson = localStorage.getItem("outJson");
  outJson=JSON.stringify(outJson)
  const request = async () => {
  const response =  await fetch('/table?sub=remove', {method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
  if(response.ok){
    const object = await response.text()
    console.log(object)
  }}
  request();
}

const removeAll= () =>{
  blank()
}


const onChange = (e) => 
{
  let files = e.target.files
  let infile = files[0]
  let formData = new FormData();
  console.log(infile)
  formData.append("infile", infile);
  const request = async () => {
  const response =  await fetch('/parse', {method: "POST", body: formData})
  if(response.ok){
    const obj= await response.json()
    console.log(obj)
  }}
  request();
  //const data = JSON.stringify(obj);
  };


  return (
    <div className="Gem" >
        <GridLayout
          measureBeforeMount={true}
          className="layout"
          cols={12}
          containerPadding={[10, 10]}
          rowHeight={getViewHeight() / 2}
          margin={[10, 10]}
          layouts={layouts}
          onLayoutChange={(layout) => onLayoutChange(layout)}
        >
          <div
            className="Table"
            key="1"
            data-grid={{
              x: .5,
              y: 0,
              w: 10,
              h: 1,
              i: "table",
              static: true,
            }}
          >
              {/* Table */}
              <BasicTable />
              <form>
        <input type='file' name='file' onChange={(e)=>onChange(e)}/>
        <input type="button" name='remove' value="Remove" onClick={()=>remove}/>
        <input type="button" name='removeAll' value="Remove All" onClick={()=>removeAll}/>
        <input type="button" name='moveUp' value="Move Up" onClick={()=>moveUp}/>
      </form>
          </div>
          {/* <div
            className="editor"
            key="2"
            data-grid={{
              x: .5,
              y: 1,
              w: 4,
              h: 1,
              i: "editor",
              static: true,
            }}
          >
              <Editor />
              Editor
          </div> */}
          {/* <div
            className="team"
            key="3"
            data-grid={{
              x: 4.5,
              y: 1,
              w: 4,
              h: 1,
              i: "team",
              static: true,
            }}
          >
              Team
          </div> */}
          {/* <div
            className="Im/Ex"
            key="4"
            data-grid={{
              x: 9,
              y: 1,
              w: 2,
              h: 1,
              i: "Im/Ex",
              static: true,
            }}
          >
              Im/Ex
          </div> */}
        </GridLayout>
    </div>
  );
};
