import React, { Component } from "react";
import axios from "axios";
import { ReactTabulator } from "react-tabulator";
import "tabulator-tables/dist/css/tabulator.min.css"; //import Tabulator stylesheet

export class Table extends Component {
  constructor(props) {
    super(props);

    this.state = {
        data: [],
      errorMsg: ""
    };
  }

  componentDidMount() {
    var config = {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    };
    axios
      .get("http://127.0.0.1:5000", config)
      .then(response => {
        this.setState({ todos: response.data });
      })
      .catch(error => {
        this.setState({
          errorMsg: `Error retreiving data. Detailed error : ${error}`
        });
      });
  }

  render() {
    const { data, errorMsg } = this.state;

    const columns = [
      {
        title: "Name",
        field:"name",
        align: "left",
        headerFilter: "input"
      },
      {
        title: "Username",
        field:"username",
        align: "left",
        headerFilter: "input"
      },
      {
        title: "User ID",
        field: "uid",
        align: "left",
        headerFilter: "input"
      },
      { 
        title: "Team", 
        field: "team",
        align: "center",
        headerFilter: "input" 
     },
      {
        title: "Line Color",
        field: "tlinecolor",
        formatter:"color",
        align: "center",
        headerFilter: "input"
      },
      {
        title: "Node Color",
        field: "enodecolor",
        formatter:"color",
        align: "right",
        headerFilter: "input"
      },
      {
        title: "Line Width",
        field:"elinewidth",
        align: "left",
        headerFilter: "input"
      }, 
      {
        title: "Node Size",
        field:"enodesize",
        align: "left",
        headerFilter: "input"
      },
      {
        title: "Node Shape",
        field:"enodeshape",
        align: "left",
        headerFilter: "input"
      }
    ];

    const options = {
      layoutColumnsOnNewData: true,
      layout: "fitColumns", //fit columns to width of table (optional)
      responsiveLayout: "hide", //hide columns that dont fit on the table
      tooltips: true, //show tool tips on cells
      addRowPos: "top", //when adding a new row, add it to the top of the table
      history: true, //allow undo and redo actions on the table
      groupBy: "userId",
      pagination: "local", //paginate the data
      paginationSize: 10, //allow 20 rows per page of data
      paginationSizeSelector: [5, 10, 20, 50],
      movableColumns: true, //allow column order to be changed
      resizableRows: true //allow row order to be changed
    };

    return (
      <div>
        <ReactTabulator
          data={data}
          columns={columns}
          tooltips={true}
          layout={"fitData"}
          options={options}
        />
        {errorMsg ? <div>{errorMsg}</div> : null}
      </div>
    );
  }
}

export default Table;
