import re
import os
from flask import (Flask, render_template, redirect, request, jsonify, json,send_from_directory)
#from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask("__main__")
mainpath= os.getcwd()
UPLOAD_FOLDER = mainpath + '/static'
ALLOWED_EXTENSIONS = {'txt', 'mapcss', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        self.TEMPUSERS = {}
        self.counttitle=str("EDITORCOUNT")
        for j in range(100):
            self.TEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.OUTJSON = {}

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
        IN = IN.replace(' Team',"")
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
                self.TEMPUSERS[str(self.usercount)] = CONSTRUCTOR
                self.ADDUSERS.append(CONSTRUCTOR)
                self.OUTJSON[self.usercount]={'NAME':CONSTRUCTOR.NAME,'UID':CONSTRUCTOR.UID,'LINECOLOR':CONSTRUCTOR.LINECOLOR,'LINEWIDTH':CONSTRUCTOR.LINEWIDTH,'NODESIZE':CONSTRUCTOR.NODESIZE,'NODESHAPE':CONSTRUCTOR.NODESHAPE,'NODECOLOR':CONSTRUCTOR.NODECOLOR}
                self.usercount +=1
 
            else:
                pass

        #print(self.OUTJSON)    
        self.OUTPUTJSON=jsonify(self.OUTJSON)
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/parse', methods=['GET', 'POST'])
def upload_file():
        one = MAIN()
        infile= request.files.get('infile')
        text=str(infile.read())
        one.PARSER(text)
        return(one.OUTJSON)
    
@app.route('/download/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    return render_template('downloads.html',value=filename)

    
    #filename=str(request.args.get('filename'))
    #path=str(request.args.get('path'))
    #return send_from_directory(directory=path, filename=filename,as_attachment=True, mimetype='application/octet-stream', attachment_filename=(str(filename)) + '.map')
       

       

@app.route('/compile', methods=['GET', 'POST'])
def compile():
        one = MAIN()
        count = 0
        injson= request.get_json()
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
                editor.NAME=injson[i]['name']
                editor.UID=injson[i]['uid']
                editor.NODECOLOR=injson[i]['ncolor']
                editor.NODESIZE=injson[i]['nsize']
                editor.NODESHAPE=injson[i]['nshape']
                editor.LINEWIDTH=injson[i]['lwidth']
                editor.LINECOLOR=injson[i]['lcolor']
                editor.USERBLOCK=re.sub(FINDUSERNAME,editor.NAME , one.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERID,editor.UID , editor.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERNODESIZE,editor.NODESIZE , editor.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERNODECOLOR,editor.NODECOLOR , editor.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERNODESHAPE,editor.NODESHAPE , editor.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERWAYWIDTH,editor.LINEWIDTH , editor.USERBLOCK)
                editor.USERBLOCK=re.sub(FINDUSERWAYCOLOR,editor.LINECOLOR , editor.USERBLOCK)

                FINSHEDUSERBLOCK  += str(editor.USERBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODESIZE, injson['UNUPLOADED']['unupnsize'], one.STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODECOLOR,injson['UNUPLOADED']['unupncolor'], STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODESHAPE, injson['UNUPLOADED']['unupnshape'], STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYCOLOR, injson['UNUPLOADED']['unuplcolor'], STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYWIDTH, injson['UNUPLOADED']['unuplwidth'], STATICBLOCK)
        STATICBLOCK = re.sub(FINDTITLE, injson['UNUPLOADED']['teamname'], STATICBLOCK)
        BLOCK = FINSHEDUSERBLOCK + STATICBLOCK
        path=app.config['UPLOAD_FOLDER']``
        filename=str(injson['UNUPLOADED']['teamname'])
        filename="QAQC_"+filename+".mapcss"
        uppath=path+"/"+filename
        print(path)
        with open(uppath, 'w')as CSS:
            CSS.writelines (BLOCK)
        BLOCK = ""
        STATICBLOCK=""
        FINSHEDUSERBLOCK =""
        return redirect('/download/'+uppath)

        
    
if __name__ == "__main__":
    app.run(port = 3000)





