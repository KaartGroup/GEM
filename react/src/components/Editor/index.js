import  React from "react";

import { Upload, EditorMenu, UploadFile, UploadForm } from "./styles";

export const Editor = () => {

    const onChange = (e) => {
        console.log("WORK")
        let files = e.target.files;
        let infile = files[0];
        console.log(files)
        let formData = new FormData();
        formData.append("infile", infile);
        const request = async () => {
            const response = await fetch("/parse", {method:"POST", body: formData})
            if (response.ok){
                const JJ = await response.json()
                console.log(JJ);
            }
        }
        request();
    };
    
return(
    <EditorMenu>
        <UploadForm action="/parse" method="POST" encType="multipart/form-data">
    <Upload type="submit">Upload</Upload>
    <UploadFile type="file" onChange={(e)=>onChange(e)} name="file" id="file" />
    </UploadForm >
    </EditorMenu>
    );
};