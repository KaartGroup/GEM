  import React, { Component, useState, useContext, useEffect } from "react";
import ReactGridLayout, { WidthProvider } from "react-grid-layout";
import "./styles.css";
import { FileButtons } from "components/FileButtons";
import { ExportButton } from "../FileButtons/ExportButton.js";
import { DownloadButton } from "../FileButtons/DownloadButton.js";
import { EditorTable } from "components/Table"
import { EditButton } from "../Edit/EditButton.js"
import { TeamNameField } from "../TeamName/TeamNameField.js"
import { EditorNameField } from "../NameFields/EditorNameField.js"
import { UserNameField } from "../NameFields/UserNameField.js"
import { LineWidthSpin} from "../Spinners/LineWidthSpin.js"
import { UnUpLineWidthSpin} from "../Spinners/UnUpLineWidthSpin.js"
import { NodeSizeSpin} from "../Spinners/NodeSizeSpin.js"
import { UnUpNodeSizeSpin} from "../Spinners/UnUpNodeSizeSpin.js"
import { LineColorPicker } from "../ColorPickers/LineColorPicker.js"
import { UnUpLineColorPicker } from "../ColorPickers/UnUpLineColorPicker.js"
import { NodeColorPicker } from "../ColorPickers/NodeColorPicker.js"
import { UnUpNodeColorPicker } from "../ColorPickers/UnUpNodeColorPicker.js"
import { NodeShapeMenu } from "../ShapeMenu/NodeShapeMenu.js"
import { UnUpNodeShapeMenu } from "../ShapeMenu/UnUpNodeShapeMenu.js"
import { RemoveButtons } from "../TableButtons/RemoveButtons.js"
import { MoveButtons } from "../TableButtons/MoveButtons.js"
import { render } from "@testing-library/react";
import { DataContext } from "../../common/DataContext";
import { saveAs } from 'file-saver'
import { GEM, MobileLineandNodeWrapper,MobileFileButtonsWrapper ,MobileTeamTableWrapper, MobileTeamTableBtns,MobileViewWrapper ,AddUpdateEditor, FileButtonsWrapper, UpExDown, UnUpLineandNodeWrapper, LineandNodeWrapper, TeamTable, UnUploadedEditor, TeamTableBtns, AddUpdateBtns  } from "./styles.js";
import {BrowserView, MobileView, isBrowser, isMobile} from 'react-device-detect';


var inEditName, inUserName, inLineWidth, inNodeSize, inLineWidth, inNodeSize, inLineColor, inNodeColor, inNodeShape;

const GridLayout = WidthProvider(ReactGridLayout);

export const Grid = () => {
  const { tableData, 
  setTableData,
  fileID,
  generateGemJsonId,
  } = useContext(DataContext);

  const [state, setState] = useState({
    tableData:tableData,
    TeamName:"",
    EditorName:"",
    UserName:"",
    LineColor: '#A9A9A9',
    LineWidth: 5,
    NodeColor:"#D3D3D3",
    NodeSize:5,
    NodeShape:'/icons/circle.png',
    UnUpLineColor: 'green',
    UnUpNodeColor: 'orange',
    UnUpLineWidth:5,
    UnUpNodeSize:5,
    UnUpNodeShape:'/icons/square.png',
    FileIndex: fileID,
    RowData:{},
    ShowShapeMenu:false,
    ShowUnUpShapeMenu:false,
    ShowLineColorMenu:false,
    ShowUnUpLineColorMenu:false,
    ShowNodeColorMenu:false,
    ShowUnUpNodeColorMenu:false,
    addEditor:true,
    newFile:true,

  });

  useEffect((fileID) => {
    if (fileID == null) {
      generateGemJsonId();
    }
  }, [])

    const GetUnUpload=() =>{
      if (state.TeamName ==="" && tableData[0].NAME !=null){
        alert("Please enter a valid team name before exporting")
        return
      }
      if (tableData[0].NAME ===null){
        alert("No Data to export. You must either import an existing .mapscc file to edit, or populate the table with editor data in order to export.")
        return
      }
      let path = '/api/uploads/' + state.TeamName + ".mapcss";
      const Downrequest = async () => {
        return fetch(path, {method: "GET",responseType: 'blob'})
        .then(response=>response.blob())
        .then(blob => saveAs(blob, state.TeamName + ".mapcss"))
      }
      let outJson= [{"TeamName":state.TeamName,"LineColor":state.UnUpLineColor,"lineWidth":state.UnUpLineWidth,"NodeSize":state.UnUpNodeSize,"NodeColor":state.UnUpNodeColor,"NodeShape":state.UnUpNodeShape}]
      outJson= JSON.stringify(outJson)
      let url ='/api/compile?fileID='+fileID
      const goEx = async () => {
        const response =  await fetch(url, {method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
        if(response.ok){
          const obj= await response.text()
          return fetch(path, {method: "GET",responseType: 'blob'})
          .then(response=>response.blob())
          .then(blob => saveAs(blob, state.TeamName + ".mapcss"))
        }}
        goEx();
    }

    const changeFeature=(e,f) =>{
    let outJson = state.RowData
    switch(f){
      case "LineColor":
        setState({...state,LineColor:e});
        break;

      case "NodeColor":
        setState({...state,NodeColor:e});
        break;  

      case "UnUpLineColor":
        setState({...state,UnUpLineColor:e});
        break;  

      case "UnUpNodeColor":
        setState({...state,UnUpNodeColor:e});
        break;  

      case "NodeShape":
        setState({...state,NodeShape:e,ShowShapeMenu:false})
        break;  

      case "UnUpNodeShape":
        setState({...state,UnUpNodeShape:e,ShowUnUpShapeMenu:false})
        
        break; 

      case "+LineWidth":
        if (state.LineWidth !== 10){
          setState({ ...state,LineWidth:state.LineWidth +1})}
        break; 

      case "-LineWidth":
        if (state.LineWidth !== 0){
          setState({ ...state,LineWidth:state.LineWidth -1})}
        break; 

      case "+UnUpLineWidth":
        if (state.UnUpLineWidth !== 10){
          setState({ ...state,UnUpLineWidth:state.UnUpLineWidth +1})}
        break; 

      case "-UnUpLineWidth":
        if (state.UnUpLineWidth !== 0){
          setState({ ...state,UnUpLineWidth:state.UnUpLineWidth -1})}
        break; 

      case "+NodeSize":
        if (state.NodeSize !== 10){
          setState({ ...state,NodeSize:state.NodeSize +1})}
        break;

      case "-NodeSize":
        if (state.NodeSize !== 0){
          setState({ ...state,NodeSize:state.NodeSize -1})}
      break;

      case "+UnUpNodeSize":
         if (state.UnUpNodeSize !== 10){
          setState({ ...state,UnUpNodeSize:state.UnUpNodeSize +1})}
      break; 

      case "-UnUpNodeSize":
         if (state.UnUpNodeSize !== 0){
          setState({ ...state,UnUpNodeSize:state.UnUpNodeSize -1})}
      break; 

      case "TeamName":
         if (state.UnUpNodeSize !== 0){
          setState({ ...state,TeamName:e})}
      break; 

      case "EditorName":
        setState({ ...state,EditorName:e})
      break; 

      case "UserName":
        setState({ ...state,UserName:e})
      break; 

      case "ShowShapeMenu":
        setState({ ...state,ShowShapeMenu:e})
      break; 

      case "ShowUnUpShapeMenu":
        setState({ ...state,ShowUnUpShapeMenu:e})
      break; 

      case "ShowLineColorMenu":
        setState({ ...state,ShowLineColorMenu:e})
      break; 

      case "ShowUnUpLineColorMenu":
        setState({ ...state,ShowUnUpLineColorMenu:e})
      break; 

      case "ShowNodeColorMenu":
        setState({ ...state,ShowNodeColorMenu:e})
      break; 

      case "ShowUnUpNodeColorMenu":
        setState({ ...state,ShowUnUpNodeColorMenu:e})
      break; 

      case "GetRowData":
        setState({ ...state,RowData:e})
      break; 

      case "Download":
      break; 

      case "UnUpData":
        setState({ ...state,
        newFile:false,
        TeamName:e[0]["TEAMNAME"],
        UnUpNodeColor:e[0]["UNUPNODECOLOR"], 
        UnUpNodeSize:e[0]["UNUPNODESIZE"],
        UnUpNodeShape:"/icons/"+e[0]["UNUPNODESHAPE"]+".png",  
        UnUpLineColor:e[0]["UNUPLINECOLOR"],
        UnUpLineWidth:e[0]["UNUPLINEWIDTH"],
      })
  
      break; 


      case "RemoveEditor":
          outJson=JSON.stringify(outJson)
          const request = async () => {
          const response =  await fetch('/api/table?sub=remove&fileID='+fileID, {method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
          if(response.ok){
            let object = await response.json()
            object=JSON.stringify(object)
            object=JSON.parse(object)
            setTableData(object)
          }}
          request();
      break; 

      case "RemoveAll":
        const removeRequest = async () => {
        const response =  await fetch('/api/removeAll?fileID='+fileID, {method: "GET"})
        if(response.ok){
          let object = await response.json()
          object=JSON.stringify(object)
          object=JSON.parse(object)
          setTableData(object)
        }}
        removeRequest();
        setState({...state,
          newFile:true,
          TeamName:""
        })
      
      break;


      case "MoveUp":
        
        
        outJson=JSON.stringify(outJson)
        const moveUpRequest = async () => {
        const response =  await fetch('/api/table?sub=moveUp&fileID='+fileID,{method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
        if(response.ok){
          let object = await response.json()
          object=JSON.stringify(object)
          object=JSON.parse(object)
          setTableData(object)
        }}
        moveUpRequest();
      
      break;

      case "MoveDown":
        outJson=JSON.stringify(outJson)
        const moveDownRequest = async () => {
        const response =  await fetch('/api/table?sub=moveDown&fileID='+fileID,{method: "POST", body: outJson ,headers: {'Content-Type': 'application/json'}})
        if(response.ok){
          let object = await response.json()
          object=JSON.stringify(object)
          object=JSON.parse(object)
          setTableData(object)
        }}
        moveDownRequest();
      
      break;
      case "Clear":
        setState({...state,
        EditorName: "",
        UserName: "",
        LineColor: '#A9A9A9',
        LineWidth: 5,
        NodeColor:"#D3D3D3",
        NodeSize:5,
        NodeShape:'/icons/circle.png'
      })
      break;
      
    }

  }

  function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}


    const ChangeAddButton=()=>{
      let outJson = state.RowData
      let checkJson= JSON.parse(outJson)
      let count =  0
      for (let key in checkJson['editor']){
          count ++
      }
      if (isEmpty(checkJson['rowId'])){
        alert("Invalid Secection");}
  
        else if ( checkJson['editor'][0]['NAME']===null){
            alert("Invalid Selection");
  
        }else if (count > 1 && checkJson['editor'][0]['NAME']!=null){
        alert("Only one user may be edited at a time"); 
        }else{
      setState({ ...state,addEditor:false})
     //
    }
  }

  useEffect(() => {
    if(state.addEditor===false){
      EditEditor()}
  }, [state.addEditor])

    const EditEditor = () => {
      let outJson = state.RowData
      let checkJson= JSON.parse(outJson)
      inEditName = checkJson['editor'][0]['NAME']
      inUserName = checkJson['editor'][0]['UID']
      inLineWidth = checkJson['editor'][0]['LINEWIDTH']
      inNodeSize = checkJson['editor'][0]['NODESIZE']
      inLineColor=checkJson['editor'][0]['LINECOLOR']
      inNodeColor=checkJson['editor'][0]['NODECOLOR']
      inNodeShape=checkJson['editor'][0]['NODESHAPE']
      setState({...state,
        EditorName: inEditName,
        UserName: inUserName,
        LineWidth: parseInt(inLineWidth),
        NodeSize: parseInt(inNodeSize),
        LineColor: inLineColor,
        NodeShape:inNodeShape,
        NodeColor:inNodeColor,
      })

    }
    
    const updateEditor = (e) => {
      let sub = e
      if (state.EditorName === "" && e ==="add"){
        alert("Please enter a valid Name for the Editor")
        return;
      }
      if (state.UserName === "" && e ==="add"){
          alert("Please enter a valid OSM Username")
          return;
        
        
      }else if(state.EditorName === "Mappy McMappington III" && e ==="update"){
        alert("You must first select an Editor from the table to update. ")
        return;
      }
    
    let outJson = state.RowData
    let checkJson= JSON.parse(outJson)
    let index= Object.keys(checkJson.rowId)[0]
    let entry = {'NAME':state.EditorName,"UID":state.UserName,'NODESHAPE':state.NodeShape,'NODECOLOR':state.NodeColor,"NODESIZE":state.NodeSize,'LINEWIDTH':state.LineWidth,"LINECOLOR":state.LineColor}
    entry=JSON.stringify(entry)
    let url ='/api/update?sub='+sub+'&index='+index+'&infile='+fileID+"&newFile="+state.newFile
    const update = async () => {
      const response =  await fetch(url, {method: "POST", body: entry ,headers: {'Content-Type': 'application/json'}})
      if(response.ok){
        const obj= await response.json()
        setTableData(obj)
      }}
    update();
    setState({...state,
      EditorName:"",
      UserName: "",
      LineColor: '#A9A9A9',
      LineWidth: 5,
      NodeColor:"#D3D3D3",
      NodeSize:5,
      NodeShape:'/icons/circle.png',
      addEditor:true
      })
    } 

  return (
    <div className="Gem" >
      <BrowserView>
          <GridLayout
            measureBeforeMount={true}
            className="layout"
            cols={12}
            containerPadding={[5, 5]}
          >
            <div 
              className="Table"
              key="1"
              data-grid={{
                x: 1,
                y: .1,
                w: 3,
                h: .5,
                i: "table",
                static: true,
              }}
            >
              <TeamTable>
                { tableData ? <EditorTable useData={tableData} action={changeFeature}/> : null}
                <TeamTableBtns>
                <RemoveButtons action={changeFeature}/>
                <MoveButtons action={changeFeature}/>
                </TeamTableBtns>
            </TeamTable>
            </div>
            <div
              className="FileFunctions"
              key="2"
              data-grid={{
                x: 8,
                y: 0,
                w: 1,
                h: 1,
                i: "file",
                static: true,
              }}
            > <div className="MenuLabel">
              <label >Import/Export:</label>
              </div>
              
              <label>Team Name:</label> 
            
              <TeamNameField action={changeFeature} value={state.TeamName}/>
              <FileButtonsWrapper>
              <FileButtons fileID={state.fileID} action={changeFeature} />
              <DownloadButton action={ GetUnUpload }/>
              </FileButtonsWrapper>
              </div>
            <div
              className="UnUploaded"
              key="4"
              data-grid={{
                x: 8,
                y: 1.2,
                w: 2.4,
                h: 1,
                i: "UnUpload",
                static: true,
              }}
              >             
            <div className="MenuLabel">
            <label>Non-uploaded edits:</label> 
            </div>
            <UnUpLineWidthSpin  num={state.UnUpLineWidth}action={changeFeature}/>
            <UnUpNodeSizeSpin  num={state.UnUpNodeSize}action={changeFeature}/>
            <UnUpLineandNodeWrapper>
            <UnUpLineColorPicker  action={changeFeature}color={state.UnUpLineColor}showMenu={state.ShowUnUpLineColorMenu}/>
            <UnUpNodeColorPicker action={changeFeature}color={state.UnUpNodeColor}showMenu={state.ShowUnUpNodeColorMenu}/>
            </UnUpLineandNodeWrapper>
            <UnUpNodeShapeMenu  action={changeFeature}color={state.UnUpNodeColor}src={state.UnUpNodeShape} ShowMenu={state.ShowUnUpShapeMenu}/>
            </div> 
            <div
              className="EditEditor"
              key="5"
              data-grid={{
                x: 5,
                y: .1,
                w: 2.4,
                h: 1,
                i: "Im/Ex",
                static: true,
              }}
              >
            <div className="MenuLabel">
            <label >Add/Update Editor:</label> 
            </div>
                <AddUpdateBtns>
            <EditButton       action={changeFeature} action2={updateEditor}action3={ChangeAddButton}bool={state.addEditor}/>
            </AddUpdateBtns>
              <AddUpdateEditor>
            <EditorNameField  action={changeFeature}value={state.EditorName}/>
            <UserNameField    action={changeFeature}value={state.UserName}/>
            <LineWidthSpin    action={changeFeature}num={state.LineWidth}/>

            <NodeSizeSpin     action={changeFeature}num={state.NodeSize}/>
              <LineandNodeWrapper>

            <LineColorPicker  action={changeFeature}color={state.LineColor}showMenu={state.ShowLineColorMenu}/>
            <NodeColorPicker  action={changeFeature}color={state.NodeColor}showMenu={state.ShowNodeColorMenu}/>

            </LineandNodeWrapper>

            <NodeShapeMenu    action={changeFeature}color={state.NodeColor}src={state.NodeShape} ShowMenu={state.ShowShapeMenu}/>
            </AddUpdateEditor>
            </div>
          </GridLayout>
          </BrowserView>
          <MobileView>
            <MobileViewWrapper>

            <MobileTeamTableWrapper>
            <TeamTable>
                { tableData ? <EditorTable useData={tableData} action={changeFeature}/> : null}
                <MobileTeamTableBtns>
                <RemoveButtons action={changeFeature}/>
                <MoveButtons action={changeFeature}/>
                </MobileTeamTableBtns>
            </TeamTable>
            </MobileTeamTableWrapper>
            <label style={{textAlign: 'center', borderBottom:"2px solid #f4753c"}} >Import/Export:</label>
            <label style={{padding: '4%'}}>Team Name:</label> 
            <TeamNameField action={changeFeature} value={state.TeamName}/>
              <MobileFileButtonsWrapper>
              <FileButtons fileID={state.fileID} action={changeFeature} />
              <DownloadButton action={ GetUnUpload }/>
              </MobileFileButtonsWrapper>
              <UnUpLineWidthSpin  num={state.UnUpLineWidth}action={changeFeature}/>
            <UnUpNodeSizeSpin  num={state.UnUpNodeSize}action={changeFeature}/>
            <MobileLineandNodeWrapper>
            <UnUpLineColorPicker  action={changeFeature}color={state.UnUpLineColor}showMenu={state.ShowUnUpLineColorMenu}/>
            <UnUpNodeColorPicker action={changeFeature}color={state.UnUpNodeColor}showMenu={state.ShowUnUpNodeColorMenu}/>
            </MobileLineandNodeWrapper>
            <label>Non-uploaded edits:</label> 
            <UnUpNodeShapeMenu  action={changeFeature}color={state.UnUpNodeColor}src={state.UnUpNodeShape} ShowMenu={state.ShowUnUpShapeMenu}/>
            <AddUpdateBtns>
            <EditButton       action={changeFeature} action2={updateEditor}action3={ChangeAddButton}bool={state.addEditor}/>
            </AddUpdateBtns>
            <label >Add/Update Editor:</label> 
              <AddUpdateEditor>
            <EditorNameField  action={changeFeature}value={state.EditorName}/>
            <UserNameField    action={changeFeature}value={state.UserName}/>
            <LineWidthSpin    action={changeFeature}num={state.LineWidth}/>

            <NodeSizeSpin     action={changeFeature}num={state.NodeSize}/>

              <MobileLineandNodeWrapper>
            <LineColorPicker  action={changeFeature}color={state.LineColor}showMenu={state.ShowLineColorMenu}/>
            <NodeColorPicker  action={changeFeature}color={state.NodeColor}showMenu={state.ShowNodeColorMenu}/>
            </MobileLineandNodeWrapper>
            <NodeShapeMenu    action={changeFeature}color={state.NodeColor}src={state.NodeShape} ShowMenu={state.ShowShapeMenu}/>
            </AddUpdateEditor>
              
            </MobileViewWrapper>

          </MobileView>
      </div>
    );
}