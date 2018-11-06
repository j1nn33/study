import os, json, templateEditor, settings


projectFile = '.project'

def mkFolder(path):
    try:
        os.mkdir(path)
        return True
    except:
        return False

def createProject(data):
    # возвращает templete который создали в editor
    template = json.load(open(templateEditor.templateFile))
    # путь к проектам
    path = settings.settingsClass().load()['path']
    if os.path.exists(path):
        pName = checkLegalCharacters(data['name'])
        pPath = os.path.join(path, pName)
        if mkFolder(pPath):
            buildFolders(pPath, template)
        makeProjectFile(pPath, data)

def buildFolders(root, folders):
    for f in folders:
        full = os.path.join(root, f['name'])
        mkFolder(full)
        buildFolders(full, f['content'])

def makeProjectFile(path, data):
    filePath = os.path.join(path, projectFile)
    with open(filePath, 'w') as f:
        json.dump(data, f, indent=4)

def checkLegalCharacters(name):
    return name

def getProjectInfo(path):
    #filePath = os.path.join(path, projectFile)
    filePath = os.path.join(path,projectFile)
    if os.path.exists(filePath):
        #print (filePath)
        with open(filePath) as f:
            """
            print (f)
            f=f.name.split('\\')
            f='\\'.join(f[:-1])
            return f
            """
            #print(json.load(f))
            return json.load(f)


