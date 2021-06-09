import os


def read_text_file(file_path):
    codice_modulo = '<meta codice_modulo_figlio="MARCA_BOLLO"'
    nLower = 'in_bollo="no"'
    pLower = 'in_bollo="si"'
    nUpper = 'in_bollo="NO"'
    pUpper = 'in_bollo="SI"'
    stringToCheck = [nLower, nUpper, pLower, pUpper]
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            data = file.read()
            if not any(x in data for x in stringToCheck):
                if codice_modulo in data:
                    if "istruzioni_compilazione=" in data:
                        data = data.replace(
                            "istruzioni_compilazione=", pLower+"\n"+"istruzioni_compilazione=")
                else:
                    data = data.replace("istruzioni_compilazione=",
                                        nLower+"\n"+"istruzioni_compilazione=")
            else:
                return False
    except IOError:
        print("impossibile leggere il file. errore di I/O " + file_path)

    with open(file_path, 'w', encoding="UTF8") as file:
        file.write(data)
    return True


mainPath = "C:/Users/giuli/Desktop/DEV/modulesChangerScript/modulistica/modules"

try:
    os.chdir(mainPath)
except FileNotFoundError as fileNotFoundException:
    print("questa cartella non esiste" + fileNotFoundException)

processedFiles = 0
numberOfFiles = 0
ignoredFolder = {"__REVISIONARE", "__sviluppo",
                 "_maggioli jcitygov", "_modelli"}

interestedFolders = [x for x in os.listdir(mainPath) if x not in ignoredFolder]


for folder in interestedFolders:

    for root, dirs, files in os.walk(mainPath+"/"+folder):
        if "_modules_r_" in root:
            for file in files:
                file_path = f"{root}/{file}"
                if file.endswith(".html"):
                    if read_text_file(file_path):
                        processedFiles += 1
                else:
                    print("this file does not end with .html: " + file_path)
                numberOfFiles += 1

print("i file HTML trovati sono " + str(numberOfFiles))
print(str(processedFiles) + " file processati")
