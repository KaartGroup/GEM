import React, { useMemo, useState, useContext, useEffect } from 'react';
import {useTable, useRowSelect} from 'react-table';
import {COLUMNS} from './columns';
import userList from './template.json';
import { DataContext } from "../../common/DataContext";
//import {outJson} from '../variables.js';
var jsonId= localStorage.getItem("fileIndex")
var columnId;
var outcolor;
////////////////////////////////////
const IndeterminateCheckbox = React.forwardRef(
    ({ indeterminate, ...rest }, ref) => {
      const defaultRef = React.useRef()
      const resolvedRef = ref || defaultRef

      React.useEffect(() => {
        resolvedRef.current.indeterminate = indeterminate
      }, [resolvedRef, indeterminate])
  
      return (
        <>
          <input type="checkbox" ref={resolvedRef} {...rest} />
        </>
      )
    }
  )
export const EditorTable = ({useData})=>{
    const columns = useMemo(() => COLUMNS,[])
    const data = useData 



     var outJson;
     const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        selectedFlatRows,
        state: { selectedRowIds },
      } =  useTable(
        {
        columns,
        data,

        },
        useRowSelect,
        hooks => {
            hooks.visibleColumns.push(columns => [
              // Let's make a column for selection
              {
                id: 'selection',
                // The header can use the table's getToggleAllRowsSelectedProps method
                // to render a checkbox
                Header: ({ getToggleAllRowsSelectedProps }) => (
                  <div>
                    <IndeterminateCheckbox {...getToggleAllRowsSelectedProps()} />
                  </div>
                ),
                // The cell can use the individual row's getToggleRowSelectedProps method
                // to the render a checkbox
                Cell: ({ row }) => (
                  <div>
                    <IndeterminateCheckbox {...row.getToggleRowSelectedProps()} />
                  </div>
                ),
              },
              ...columns,
            ])
          }
        )
        outJson= JSON.stringify(
          {
            'rowId': selectedRowIds,
            'editor': selectedFlatRows.map(
              d => d.original,
            ),
          },
    
        )
        localStorage.setItem("outJson", outJson); 
        
        return (
            <>
              
              <table {...getTableProps()}>
                <thead>
                  {headerGroups.map(headerGroup => (
                    <tr {...headerGroup.getHeaderGroupProps()}>
                      {headerGroup.headers.map(column => (
                        <th {...column.getHeaderProps()}>{ 
                          column.render('Header')
                          }</th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                  {rows.map((row, i) => {
                    prepareRow(row)
                    return (
                      <tr {...row.getRowProps()}>
                        {row.cells.map(cell => {
                            {
                              if(cell.column.id === 'LINECOLOR'){
                                let index = cell.row.index 
                                if (cell.value === null){
                                  return <div></div> 
                                }else{
                                return <img className="LineColors" src={cell.value} style={{'background-color':data[index].LINECOLOR}} alt=""/> 
                                }}

                              if(cell.column.id === 'NODESHAPE'){
                                let index = cell.row.index 
                                if(cell.value ===null){
                                  return <div></div> 
                                }else{
                              return <img className="NodeIcons" src={cell.value} style={{'background-color':data[index].NODECOLOR}} alt=""/> 
                              }}else{
                           return <td {...cell.getCellProps()}>{
                            cell.render('Cell')
                            }</td>}
                  }
                  })}
                      </tr>
                    )
                  })}
                </tbody>
              </table>



            </>
          )
        }