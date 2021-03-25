import React, { createContext, useContext, useState, useEffect } from "react";
import { useLocalStorageState } from "../useLocalStorageState";
import { json as fetchJson } from "d3-fetch";
import { API_URL } from "components/constants.js";

export const DataContext = createContext({});

export const DataProvider = ({ children }) => {

const [fileID, setFileID] = useLocalStorageState("gem.file_id", null);
const [tableData, setTableData] = useState(null);

  useEffect(() => {
    if (fileID != null) {
      fetchGemJson();
    }
  }, [fileID])


const fetchGemJson = () => {
    let jsonURL = API_URL.concat("gem_json/template")
        .concat("?index=")
        .concat(fileID);
    fetchJson(jsonURL) 
      .then((resp) => setTableData(resp))
  };

const generateGemJsonId = () => {
    let jsonURL = API_URL.concat("gem_json/generate")
      
    fetch(jsonURL)
      .then((response) => {
        if (!response.ok) {
          throw response;
        }
        return response.text();
      })
      .then((resp) => setFileID(resp))
      .catch((error) => {
        console.log(error);
      });
  };







   const value = {
        fileID,
        tableData,
        setTableData,
        fetchGemJson,
        generateGemJsonId,

        TeamName:"Sneffles",
        EditorName:"Mappy McMappington III",
        UserName:"VLD-Whatever",
        LineColor: 'darkgrey',
        LineWidth: 5,
        NodeColor:"lightgrey",
        NodeSize:5,
        NodeShape:'/icons/circle.png',
        UnUpLineColor: 'green',
        UnUpNodeColor: 'orange',
        UnUpLineWidth:5,
        UnUpNodeSize:5,
        UnUpNodeShape:'/icons/square.png',
        FileIndex: fileID,
    };

    return value ? (
        <DataContext.Provider value={value}>{children}</DataContext.Provider>
    ) : null;
};
