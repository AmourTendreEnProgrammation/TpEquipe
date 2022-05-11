import hou

def init(par):
    # On va chercher le parent de la Node et VScode nous offre des suggestions
    parent:hou.Node = par
    # On va chercher le template nécessaire pour l'interface
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    obj:hou.Node = hou.node("/obj/team_python_v2")

    if g.find("points") == None:
        # On applique la création du bouton
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("points","Création polygon")
        # Update de l'interface lorsque l'action est effectuée
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        # On allonge l'interface avec l'apparition du bouton 
        g.append(p)

    if g.find("multi") == None:
        # On aménage un multiparm afin de le manipuler
        folder:hou.FolderParmTemplate = hou.FolderParmTemplate("multi","Positions",folder_type=hou.folderType.MultiparmBlock)
        # On conçoit le type de parm
        vec3:hou.FloatParmTemplate = hou.FloatParmTemplate("posf","position",3,naming_scheme=hou.parmNamingScheme.XYZW)
        # On détermine le type de parm
        folder.addParmTemplate(vec3)
        # On greffe le multiparm à la suite du bouton
        g.append(folder)
        # On synchronise l'interface avec les nouvelles informations
    parent.setParmTemplateGroup(g)

def update():
    parent:hou.Node = hou.pwd()
    multiparm:hou.Parm = parent.parm("multi")
    if multiparm != None:
        for i in range(0,multiparm.multiParmInstancesCount()):
            # Créer des nodes pour sauvegarder les valeurs des positions
            attributeexpressionSop:hou.SopNode = parent.createNode ("attribexpression")
            snippet1:hou.Parm = attributeexpressionSop.parm("snippet1")
            # On change le paramètre de snippet
            snippet1.set("value")
    # On se sert de count pour mieux repérer l'index
    count = 1
    instances = multiparm.multiParmInstances()
    
    for x in instances:
        #On place 
        parm:hou.Parm = x
        attributeexpressionSop:hou.SopNode = parent.node("attribexpression" + str(count))
        #On va chercher la valeur du paramètre
        value = parm.eval()
        #On va consulter la variable afin d'avoir des valeurs précises selon leurs noms
        if parm.name().find("x") > -1:
            xp = attributeexpressionSop.parm("valv3_1x")
            xp.set(value)
        if parm.name().find("y") > -1:
            yp = attributeexpressionSop.parm("valv3_1y")
            yp.set(value)
        if parm.name().find("z") > -1:
            zp = attributeexpressionSop.parm("valv3_1z")
            zp.set(value)
        #On augmente la valeur de count
            count+=1
    
