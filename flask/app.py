import re
import os
from flask import (Flask, render_template, redirect, request, jsonify, json,send_from_directory)
#from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
mainpath= os.getcwd()
UPLOAD_FOLDER = mainpath + '/static'
ALLOWED_EXTENSIONS = {'txt', 'mapcss', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask("__main__")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###################### # EDITOR CLASS # #######################
blankJson=[{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None},
{"NAME":None,"UID":None,"LINEWIDTH":None,"LINECOLOR":None,"NODESHAPE":None,"NODESIZE":None,"NODECOLOR":None}]

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
        self.TEMPUSERS = {}
        self.counttitle=str("EDITORCOUNT")
        for j in range(100):
            self.TEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.OUTJSON = []

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
                #self.OUTJSON[self.usercount]={'NAME':CONSTRUCTOR.NAME,'UID':CONSTRUCTOR.UID,'LINECOLOR':CONSTRUCTOR.LINECOLOR,'LINEWIDTH':CONSTRUCTOR.LINEWIDTH,'NODESIZE':CONSTRUCTOR.NODESIZE,'NODESHAPE':CONSTRUCTOR.NODESHAPE,'NODECOLOR':CONSTRUCTOR.NODECOLOR}
                self.OUTJSON.append({'NAME':CONSTRUCTOR.NAME,"UID":CONSTRUCTOR.UID,"LINECOLOR":CONSTRUCTOR.LINECOLOR,"LINEWIDTH":CONSTRUCTOR.LINEWIDTH,"NODESIZE":CONSTRUCTOR.NODESIZE,"NODESHAPE":CONSTRUCTOR.NODESHAPE,"NODECOLOR":CONSTRUCTOR.NODECOLOR})
         
                self.usercount +=1
 
            else:
                pass

        #print(self.OUTJSON)    
        self.OUTPUTJSON=jsonify(self.OUTJSON)
        







###################### # routes # #############################
@app.route('/blank')
def blank():
    with open("/Users/imac25/Desktop/WEBGEM/WEBAPP/gem/src/components/template.json", 'w')as json_file:
            json.dump(blankJson, json_file)
    return(blankJson)

@app.route('/parse', methods=['GET', 'POST'])
def upload_file():
        one = MAIN()
        infile= request.files.get('infile')
        text=str(infile.read())
        one.PARSER(text)
        with open("/Users/imac25/Desktop/WEBGEM/WEBAPP/gem/src/components/template.json", 'w')as json_file:
            json.dump(one.OUTJSON, json_file)
           #json.write (str(one.OUTJSON))
        return(one.OUTJSON)


       
    
if __name__ == "__main__":
    app.run(port = 3000)





