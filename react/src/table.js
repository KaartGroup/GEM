import React, { Component } from "react";
import axios from "axios";
import { ReactTabulator } from "react-tabulator";
import "tabulator-tables/dist/css/tabulator.min.css"; //import Tabulator stylesheet
import $ from "jquery";
import jQuery from "jquery";

var tdat = [
  {
    elinecolor: "#ff0000",
    elinewidth: "1",
    ename: "Farris",
    enodecolor: "#ff0000",
    enodeshape: "circle",
    enodesize: "10",
    team: "Engineering",
    tlinecolor: "#0000ff",
    tlinewidth: "1",
    tnodecolor: "#ff0000",
    tnodeshape: "circle",
    tnodesize: "10",
    uid: "98989898",
    username: "Farieberrie",
  },
];

$(document).ready(function () {
  (function ($) {
    $.fn.serializeFormJSON = function () {
      var o = {};
      var a = this.serializeArray();
      $.each(a, function () {
        if (o[this.name]) {
          if (!o[this.name].push) {
            o[this.name] = [o[this.name]];
          }
          o[this.name].push(this.value || "");
        } else {
          o[this.name] = this.value || "";
        }
      });
      return o;
    };
  })(jQuery);

  $("form").submit(function (e) {
    e.preventDefault();
    var data = $(this).serializeFormJSON();
    tdat.push(data);
    alert("User added!");
    console.log(tdat);

    /* Object
    Key : "value"
    */

    return data;
  });
});

export class Table extends Component {
  state = {
    data: tdat,
    selectedName: "",
  };

  componentDidMount() {
    var config = {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    };
  }

  render() {
    var { data, errorMsg } = this.state;

    const columns = [
      {
        title: "Name",
        field: "ename",
        align: "left",
        headerFilter: "input",
      },
      {
        title: "Username",
        field: "username",
        align: "left",
        headerFilter: "input",
      },
      {
        title: "User ID",
        field: "uid",
        align: "left",
        headerFilter: "input",
      },
      {
        title: "Team",
        field: "team",
        align: "center",
        headerFilter: "input",
      },
      {
        title: "Line Color",
        field: "tlinecolor",
        formatter: "color",
        align: "center",
        headerFilter: "input",
      },
      {
        title: "Node Color",
        field: "enodecolor",
        formatter: "color",
        align: "right",
        headerFilter: "input",
      },
      {
        title: "Line Width",
        field: "elinewidth",
        align: "left",
        headerFilter: "input",
      },
      {
        title: "Node Size",
        field: "enodesize",
        align: "left",
        headerFilter: "input",
      },
      {
        title: "Node Shape",
        field: "enodeshape",
        align: "left",
        headerFilter: "input",
      },
    ];

    const options = {
      layoutColumnsOnNewData: true,
      layout: "fitColumns", //fit columns to width of table (optional)
      responsiveLayout: "hide", //hide columns that dont fit on the table
      tooltips: true, //show tool tips on cells
      addRowPos: "top", //when adding a new row, add it to the top of the table
      history: true, //allow undo and redo actions on the table
      pagination: "local", //paginate the data
      paginationSize: 10, //allow 20 rows per page of data
      paginationSizeSelector: [5, 10, 20, 50],
      movableColumns: true, //allow column order to be changed
      resizableRows: true, //allow row order to be changed
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
