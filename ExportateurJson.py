import json
from os import link
import hou


def init(par):
    # Pour avoir des propositions avec le support de vscode
    parent:hou.Node = par
    receivedNode:hou.Node = parent.input(0)
    # On va chercher le template qui correspond à l'interface 
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    
    if g.find("points") == None:
        # Mettre en place le bouton 
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("points","This is a button")
        # la fonction update est activé quand on interagie avec le bouton
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        # a la suite du script le bouton est rajouté
        g.append(p)
    if g.find("link") == None:
        # Création du multiparm
        link:hou.StringParmTemplate = hou.StringParmTemplate("link","chemin",1)
        # On met le multiparm après le bouton
        g.append(link)
    # On update le template
    parent.setParmTemplateGroup(g)
    # On ce sert de deinit pour enlever l'ancien template
def deinit(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    points:hou.ParmTemplate = g.find("points")
    link:hou.ParmTemplate = g.find("link")
    
    if  points != None:
        g.remove(points)
    if link != None:
        g.remove(link)
    parent.setParmTemplateGroup(g)

def update():
    parent:hou.Node = hou.pwd()
    data = {

    }
    # Nous allons chercher l'index
    count = 0
    # Nous allons chercher les valeurs par rapport a l'index 
    for g in parent.children():
        pointsNode:hou.Node = g
        parmx = pointsNode.parm ("valv3_1x")
        parmy = pointsNode.parm ("valv3_1y")
        parmz = pointsNode.parm ("valv3_1z")
        data[count] = {}
        data[count]["posx"] = parmx.eval()
        data[count]["posy"] = parmy.eval()
        data[count]["posz"] = parmz.eval()

        count+=1
    # Permet de déposer le fichier json a l'endroit choisie
    fullpath = parent.parm("link").eval() + ".json"
    file = open(fullpath,"w")
    json.dump(data,file,indent=4)
    