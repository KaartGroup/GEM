import  React, {  useMemo, useState, useContext, useEffect } from 'react';
import ReactTable from 'react-table-6';
import {COLUMNS} from './columns';
import { DataContext } from "../../common/DataContext";
//import {outJson} from '../variables.js';
import {TableLineColor, NodeShapes} from "./styles";



export const EditorTable = (props)=>{
    const columns = useMemo(() => COLUMNS,[])
    const data = props.useData
    var selectedRowID;
    var outJson;

    const {
      selectedRow,
      setSelectedRow,
      EditorRow,
      setEditorRow,
    } = useContext(DataContext);


        useEffect(() => {
          // props.action(outJson,"GetRowData")
          // setSelectedRow(EditorRow);
          setEditorRow(selectedRow);
        }, [selectedRow])

        
        //localStorage.setItem("outJson", outJson); 
        
        return (
            <>
             
 <ReactTable 
  className="-highlight"
  style={{ boxShadow: '0px 2px 4px -1px rgba(0, 0, 0, 0.2), 0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12)' ,
  width: "100%",
  height: "100%", 
  borderTop: '2px solid #f4753c',
  borderRight: '1px solid #f4753c', 
  borderLeft: '1px solid #f4753c', 
  borderRadius: '.9%',
  padding: '1%' }}
  sortable={false}
  data={data}
  defaultPageSize={10}
  columns={
    [
      {
          Header: 'Name',
          accessor: "NAME"
      },
      {
          Header: 'UID',
          accessor: "UID"
      },
      {
          Header: 'Line Color',
          accessor: "LINECOLOR",
          Cell: (row) => (
          <TableLineColor style= {{width: '11vw', border: 'none'}} color={row.value} /> 
          )
      },
      {
          Header: 'Line Width',
          accessor: "LINEWIDTH"
      },
      {
          Header: 'Node Size',
          accessor: "NODESIZE"
      },
      {
          Header: 'Node Shape',
          accessor: "NODESHAPE",
          Cell: (row) => (
            row.value ?
             <NodeShapes src={row.value }  color={row.original.NODECOLOR}  />
             : ""  
            )
      }
  ]
}

  resolveData={data => data.map(row => row)}
  getTdProps={(state, rowInfo, column, instance ) => {  
    


  return{
    
    onClick: () => {
      
      if(rowInfo){
        setSelectedRow(rowInfo.index);
        if(EditorRow == selectedRow){
          setEditorRow(rowInfo.index);
        
        console.log(selectedRow);
        // console.log(rowInfo.index)
        
        outJson = JSON.stringify(
          {
            'rowId': rowInfo.index,
            'editor': rowInfo.original
          }
          )
        }
      }
        props.action(outJson,"GetRowData");
      },
      style:{
        color : rowInfo ? rowInfo.index == selectedRow  ? '#f4753c' : null : "",
        padding : rowInfo ? rowInfo.index == selectedRow  ? '1%' : null : "",
        fontSize : rowInfo ? rowInfo.index == selectedRow  ? '20px' : null : "",
        
      }
}

  }
  }

  />

            </>
        ) 
        }