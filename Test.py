import hou

def DoStuff():
    print("Hello From Test")

def init(par):
    # Pour nous aider à avoir des suggestions dans vscode
    parent:hou.Node = par
    # On va chercher le groupe de l'interface
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    # Si l'interface ne contient pas le bouton on l'ajoute
    if g.find("test") == None:
        # On créer le bouton 
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("test","This is a button")
        # On assigne la fonction appeler lorsque le bouton est clicker
        p.setScriptCallback("print('Jai ete appeler')")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        # On ajoute le bouton après le menu scripts
        g.insertAfter("scripts",p)
    if g.find("multi") == None:
        # On creer un multiparm a utiliser
        folder:hou.FolderParmTemplate = hou.FolderParmTemplate("multi","Positions",folder_type=hou.folderType.MultiparmBlock)
        # On creer le type de parm que le multiparm va ajouter
        vec3:hou.FloatParmTemplate = hou.FloatParmTemplate("posf","position",3,naming_scheme=hou.parmNamingScheme.XYZW)
        # On ajoute le type de parm au multiparm
        folder.addParmTemplate(vec3)
        # On ajoute le multiparm après le bouton
        g.insertAfter(p.name(),folder)
    # On met à jour l'interface
    parent.setParmTemplateGroup(g)
def deinit(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    test:hou.ParmTemplate = g.find("test")
    multi:hou.ParmTemplate = g.find("multi")
    # Si test et/ou multi existe, on les enlève vu que nous serons un autre script
    if  test != None:
        g.remove(test)
    if multi != None:
        g.remove(multi)
    parent.setParmTemplateGroup(g)
