import re
import os
import flask_cors
import uuid
from flask import (Flask, render_template, redirect, request, jsonify, json, send_from_directory,make_response, send_file)
#from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask("__main__")
mainpath= os.getcwd()
UPLOAD_FOLDER = mainpath + '/static'
ALLOWED_EXTENSIONS = {'txt', 'mapcss', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_cors.CORS(app, support_credentials=True)
###################### # EDITOR CLASS # #######################
blankJson=[{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None}] 
##################### # BLANK JSON TEMPLATE # #################
class EDITORINFO(object):
    def __init__(self):
        self.NAME = ""
        self.UID = ""
        self.USERNAME = ""
        self.TITLE = ""
        self.LINECOLORTEXT = ""
        self.NODECOLORTEXT = ""
        self.LINECOLORUI = ""
        self.NODECOLORUI = ""
        self.ICONSIZE = 10
        self.LINEWIDTH = 5
        self.ICONSHAPE = ""
        self.ICONSHAPELINK = ""

class MAIN(object):
    def __init__(self):
        self.usercount = 0
        self.tempcount = 1
        #self.TEMPUSERS = {}
        #self.counttitle=str("EDITORCOUNT")
        # for j in range(100):
        #     self.TEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.OUTJSON = []
        self.UnUpJson=[]

        self.STATICBLOCK = """
meta {
  title: "";
  description: "";
  watch-modified: true;
  version: "";
  icon: "";

}

/* MODIFIED BUT NOT UPLOADED LAYER STYLE */

node:modified::modified_layer {
    symbol-shape: NOTUPNODESHAPE;
    symbol-size: NOTUPNODESIZE;
    symbol-stroke-color: NOTUPNODECOLOR;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}

way:modified::modified_layer,
node:modified < way::modified_layer {
    width: 6;
    color: transparent;
    opacity: 0;
    casing-width: 1;
    casing-color: #fffff;
    casing-opacity: 0.7;
    z-index: -5;
}

/*SELECTED LAYER STYLE*/
node:selected::selected_layer {
    symbol-shape: circle;
    symbol-size: 22;
    symbol-stroke-color: #ffffff;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}"""



        self.USERBLOCK="""
/* USER SEARCH SETTINGS */
setting::user_USERNAME {
            type:boolean;
            label:tr("Turn User USERNAME On/Off");
            default:true;
            }
/* USER SEARCH SETUP */

*[eval(JOSM_search("user:USERID"))][setting("user_USERNAME")] {
  set .USERNAME
}

/*USER WAY STYLE*/
way.USERNAME{
  z-index: -10;
  casing-color: USERWAYCOLOR;
  casing-width: USERWAYWIDTH;
  casing-opacity: 0.6;
  /*
  text: eval(concat("Highway type =", " ", tag("highway")));
  text-offset: -20;
  */
}

/*USER NODE STYLE*/
node.USERNAME{
  symbol-size: USERNODESIZE;
  symbol-shape: USERNODESHAPE;
  symbol-stroke-color: USERNODECOLOR;
  symbol-stroke-width: 3px;
  symbol-fill-opacity: 0.5;
  z-index: -5;
}"""






        
    def STRIPPER(self, IN):
        IN=str(IN).split(";")
        IN=str(IN[0])
        IN = IN.replace(" ","")
        IN = IN.replace("]","")
        IN = IN.replace("[","")
        IN = IN.replace("'","")
        IN = IN.replace('"',"")
        IN = IN.replace('Team',"")
        return(IN)
    
    def PARSER(self, INFILE):
        OUTTEXT= INFILE.split("meta {")
        TEAMTEXT = OUTTEXT[1]
 
        TEAMTEXT = TEAMTEXT.split("/*SELECTED LAYER STYLE*/")
        TEAMTEXT= TEAMTEXT[0]
        SELECTTEXT = TEAMTEXT[1]
        OUTTEXT=OUTTEXT[0]
        OUTTEXT= OUTTEXT.split("* USER SEARCH SETUP *")
        self.TEAMNAME =re.findall(r'"QC Styles For (.*)\"',TEAMTEXT)
        self.TEAMNAME = self.STRIPPER(self.TEAMNAME)
    
        self.UNUPNODESHAPE = re.findall(r'symbol-shape:(.*)\;',TEAMTEXT)
        self.UNUPNODESHAPE = self.STRIPPER(self.UNUPNODESHAPE)
        self.UNUPNODESIZE = re.findall(r'symbol-size:(.*)\;',TEAMTEXT)
        self.UNUPNODESIZE = self.STRIPPER(self.UNUPNODESIZE)
        self.UNUPNODECOLOR = re.findall(r'symbol-stroke-color:(.*)\;',TEAMTEXT)
        self.UNUPNODECOLOR = self.STRIPPER(self.UNUPNODECOLOR)
        self.UNUPLINECOLOR = re.findall(r'casing-color:(.*)\;',TEAMTEXT)
        self.UNUPLINECOLOR = self.STRIPPER(self.UNUPLINECOLOR)
        self.UNUPLINEWIDTH = re.findall(r'casing-width:(.*)\;',TEAMTEXT)
        self.UNUPLINEWIDTH = self.STRIPPER(self.UNUPLINEWIDTH)
        self.UnUpJson.append({"TEAMNAME":self.TEAMNAME,"UNUPNODESHAPE":self.UNUPNODESHAPE,"UNUPNODESIZE":self.UNUPNODESIZE,"UNUPNODECOLOR":self.UNUPNODECOLOR,"UNUPLINECOLOR":self.UNUPLINECOLOR,"UNUPLINEWIDTH":self.UNUPLINEWIDTH})

        for i in OUTTEXT:
            i=str(i).replace(" ","")
            i=i.replace("\\n","")
            CONSTRUCTOR = str(self.usercount)
            CONSTRUCTOR = EDITORINFO()
            CONSTRUCTOR.UID=re.findall(r'\=="(.+?)\"',i)
            CONSTRUCTOR.UID = self.STRIPPER(CONSTRUCTOR.UID)
            CONSTRUCTOR.NAME =re.findall(r'\"user_(.+?)"',i)
            CONSTRUCTOR.NAME = self.STRIPPER(CONSTRUCTOR.NAME)
            CONSTRUCTOR.LINECOLOR =re.findall(r'casing-color:(.*)\;',i)
            CONSTRUCTOR.LINECOLOR = self.STRIPPER(CONSTRUCTOR.LINECOLOR)
            CONSTRUCTOR.LINEWIDTH =re.findall(r'casing-width:(.*)\;',i)
            CONSTRUCTOR.LINEWIDTH  = self.STRIPPER(CONSTRUCTOR.LINEWIDTH )         
            CONSTRUCTOR.NODESIZE =re.findall(r'symbol-size:(.*)\;',i)
            CONSTRUCTOR.NODESIZE = self.STRIPPER(CONSTRUCTOR.NODESIZE)
            CONSTRUCTOR.NODESHAPE =re.findall(r'symbol-shape:(.*)\;',i)
            CONSTRUCTOR.NODESHAPE = self.STRIPPER(CONSTRUCTOR.NODESHAPE)
            CONSTRUCTOR.NODECOLOR =re.findall(r'symbol-stroke-color:(.*)\;',i)
            CONSTRUCTOR.NODECOLOR = self.STRIPPER(CONSTRUCTOR.NODECOLOR)
            if CONSTRUCTOR.NAME != "" :      
                self.ADDUSERS.append(CONSTRUCTOR)
                self.OUTJSON.append({'NAME':CONSTRUCTOR.NAME,"UID":CONSTRUCTOR.UID,"LINECOLOR":CONSTRUCTOR.LINECOLOR,"LINEWIDTH":CONSTRUCTOR.LINEWIDTH,"NODESIZE":CONSTRUCTOR.NODESIZE,"NODESHAPE":"/icons/%s.png"%(CONSTRUCTOR.NODESHAPE),"NODECOLOR":CONSTRUCTOR.NODECOLOR})
         
                self.usercount +=1
 
            else:
                pass
        self.OUTJSON.append(self.UnUpJson)      
        self.OUTPUTJSON=jsonify(self.OUTJSON)

        







###################### # routes # #############################


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

#@flask_cors.cross_origin(support_credentials=True)
@app.route("/gem_json/template")
@flask_cors.cross_origin(support_credentials=True)
def get_template():
    index=request.args.get('index')
    src = os.path.join(root_dir(),f"tmp/generated/{index}.json")
    return send_file(src)

@app.route("/gem_json/generate")
def get_or_create_json():
    index=uuid.uuid4()
    base_dir = (f"{root_dir()}/tmp/generated/") 
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    filename = base_dir + f"{index}.json"
    if not os.path.isfile(filename):
        with open(filename, 'w+')as json_file:
            json.dump(blankJson, json_file)
    return str(index)



@app.route("/removeAll")
def removeAll():
    fileID =request.args.get("fileID")
    path = (f"{root_dir()}/tmp/generated/{fileID}.json")

    with open(path, 'w+')as json_file:
        json.dump(blankJson, json_file)
    with open(path ,'r')as outJson:
        outJson=outJson.read()
    return (outJson)

@app.cli.command()
def scheduled():
    print('Deleting Files...')
    path1=os.path.join(root_dir(),"static/")
    path2=os.path.join(root_dir(),"tmp/generated/")
    for root, dirs, files in os.walk(path2):
        for f in files:
            os.remove(path2+f)
    for root, dirs, files in os.walk(path1):
        for i in files:
            os.remove(path1+i)

@app.route('/update', methods=['GET', 'POST'])
def update():
    injson= request.get_json()
    index=request.args.get('index')
    fileId=request.args.get('infile')
    path = os.path.join(root_dir(),f"tmp/generated/{fileId}.json")
    with open(path, 'r')as json_file:
        tempJson=json_file.read()
    tempJson=json.loads(tempJson)

    sub=request.args.get('sub')
    if sub =="update":
        tempJson[int(index)]=injson
    if sub =="add":
        if tempJson[0]['NAME']==None:
            tempJson=[injson]
        else:
            tempJson.append(injson)
           
    with open(path, 'w')as json_file:
            json.dump(tempJson, json_file)
    return (jsonify(tempJson))



@app.route('/parse', methods=['GET', 'POST'])
def upload_file():
        one = MAIN()
        fileId=request.args.get('ID')
        infile= request.files.get('infile')
        text=str(infile.read())
        one.PARSER(text)
        path = os.path.join(root_dir(),f"tmp/generated/{fileId}.json")
        with open(path, 'w')as json_file:
             json.dump(one.OUTJSON, json_file)
        return(jsonify(one.OUTJSON))



@app.route('/table', methods=['GET', 'POST'])
def table():

    newJson=[]
    sub=request.args.get('sub')
    fileID=request.args.get('fileID')
    injson= request.get_json()
    if injson != None:
        injson=json.loads(injson)
        index= injson["rowId"].keys()
        index=str(index).replace(' ',"")
        index= str(index).split("(")
        index=str (index[1::])
        index=index.replace("[","")
        index=index.replace("]","")
        index=index.replace(")","")
        index=index.replace("'","")
        index=index.replace('"',"")
        index=index.replace(' ',"")
        index=index.split(",")
    path = os.path.join(root_dir(),f"tmp/generated/{fileID}.json")
    with open(path, 'r')as json_file:
        tempJson=json_file.read()
    tempJson=tempJson.split("}, {")

    if sub == "remove":
        for i in sorted(index, reverse=True):
            del tempJson[int(i)]

        


    for i in tempJson:
        k={}
        i=i.replace("'","")
        i=i.replace("]","")
        i=i.replace("[","")
        i=i.replace("{","")
        i=i.replace("}","")
        i=i.replace(" ","")
        i=i.split(",")
        
        for j in i:
            j=j.replace('"',"")
            j=j.replace("'",'"')
            j=j.replace(" ","")
            j=j.split(":")
            k[str(j[0])]=str(j[1])
        newJson.append(k)

    if sub == "moveUp":
        for i in index:
            j=int(i)-1
            if j <0:
                pass
            else:
                newJson[int(i)],newJson[j] =newJson[j],newJson[int(i)]
    elif sub == "moveDown":
        for i in index:
            j=int(i)+1
            if j >= int(len(newJson)):
                pass
            else:
                newJson[int(i)],newJson[j] =newJson[j],newJson[int(i)]
    with open(path, 'w')as json_file:
            json.dump(newJson, json_file) 
    with open(path, "r")as outFile:
        outJson=outFile.read()
    return(outJson)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(root_dir(), app.config['UPLOAD_FOLDER'])    
    return send_from_directory(directory=uploads, filename=filename)




@app.route('/compile', methods=['GET', 'POST'])
def compile():
        one = MAIN()
        count = 0
        unUpJson= request.get_json()
        fileID=request.args.get("fileID")
        path = os.path.join(root_dir(),f"tmp/generated/{fileID}.json")
        with open(path, 'r')as json_file:
            injson=json_file.read()
        injson=json.loads(injson)
        FINDUSERNAME = re.compile('(?:|)USERNAME(?:|\W)')
        FINDUSERID = re.compile('(?:|)USERID(?:|\W)')
        FINDUSERNODESIZE = re.compile('(?:|)USERNODESIZE(?:|\W)')
        FINDUSERNODECOLOR = re.compile('(?:|)USERNODECOLOR(?:|\W)')
        FINDUSERNODESHAPE = re.compile('(?:|)USERNODESHAPE(?:|\W)')
        FINDUSERWAYWIDTH = re.compile('(?:|)USERWAYWIDTH(?:|\W)')
        FINDUSERWAYCOLOR = re.compile('(?:|)USERWAYCOLOR(?:|\W)')
        FINDNOTUPNODESIZE = re.compile('(?:|)NOTUPNODESIZE(?:|\W)')
        FINDNOTUPNODECOLOR = re.compile('(?:|)NOTUPNODECOLOR(?:|\W)')
        FINDNOTUPNODESHAPE = re.compile('(?:|)NOTUPNODESHAPE(?:|\W)')
        FINDNOTUPWAYCOLOR = re.compile('(?:|)NOTUPWAYCOLOR(?:|\W)')
        FINDNOTUPWAYWIDTH = re.compile('(?:|)NOTUPWAYWIDTH(?:|\W)')
        FINDTITLE = re.compile('(?:|)TITLE(?:|\W)')
        FINSHEDUSERBLOCK = ""
        for i in injson:
            if i != 'UNUPLOADED':
                editor=EDITORINFO()
                
                if 'NAME' in injson[int(count)]: 
                    editor.UID=injson[count]['UID']
                    editor.NAME=injson[count]['NAME']
                    editor.NODECOLOR=injson[count]['NODECOLOR']
                    editor.NODESIZE=injson[count]['NODESIZE']
                    editor.NODESHAPE=injson[count]['NODESHAPE']
                    editor.LINEWIDTH=injson[count]['LINEWIDTH']
                    editor.LINECOLOR=injson[count]['LINECOLOR']
                    editor.USERBLOCK=re.sub(FINDUSERNAME, editor.NAME , one.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERID, editor.UID , editor.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERNODESIZE, str(editor.NODESIZE) , editor.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERNODECOLOR, editor.NODECOLOR , editor.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERNODESHAPE, editor.NODESHAPE , editor.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERWAYWIDTH, str(editor.LINEWIDTH) , editor.USERBLOCK)
                    editor.USERBLOCK=re.sub(FINDUSERWAYCOLOR, editor.LINECOLOR , editor.USERBLOCK)
                    FINSHEDUSERBLOCK  += str(editor.USERBLOCK)
                    count += 1
        STATICBLOCK = re.sub(FINDNOTUPNODESIZE, str(unUpJson[0]['NodeSize']), one.STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODECOLOR,str(unUpJson[0]['NodeColor']), STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODESHAPE, str(unUpJson[0]['NodeShape']), STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYCOLOR, str(unUpJson[0]['LineColor']), STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYWIDTH, str(unUpJson[0]['lineWidth']), STATICBLOCK)
        STATICBLOCK = re.sub(FINDTITLE, str(unUpJson[0]['TeamName']), STATICBLOCK)
        BLOCK = FINSHEDUSERBLOCK + STATICBLOCK

        path=os.getcwd() + "/static"
        filename=str(str(unUpJson[0]['TeamName']))
        filename=filename+".mapcss"
        uppath=path+"/"+filename
        with open(uppath, 'w')as CSS:
            CSS.writelines (BLOCK)
        BLOCK = ""
        STATICBLOCK=""
        FINSHEDUSERBLOCK =""
        return ("exported")
        #return str(BLOCK)
  
    
# if __name__ == "__main__":
#     app.run(port = 3000)





