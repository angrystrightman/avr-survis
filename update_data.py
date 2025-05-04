import os, json, codecs, time, sys
dataDir       = "src/data/"
bibFile       = "bib/references.bib"        # ★ 确认相对路径正确
generatedDir  = os.path.join(dataDir, "generated/")
bibJsFile     = os.path.join(generatedDir, "bib.js")
papersPdfDir  = os.path.join(dataDir, "papers_pdf/")
papersImgDir  = os.path.join(dataDir, "papers_img/")
availablePdf  = os.path.join(generatedDir, "available_pdf.js")
availableImg  = os.path.join(generatedDir, "available_img.js")

# ------------ helper ------------
def safe_mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)
safe_mkdir(generatedDir)
# ------------ parse bib ----------
def parseBibtex(path):
    parsed = {}; last = ""
    with codecs.open(path, "r", "utf-8-sig") as f:
        for line in f:
            l = line.strip()
            if l.startswith("@"):
                cid  = l.split("{",1)[1].rstrip(",")
                ctyp = l.split("{",1)[0].lstrip("@")
                parsed[cid] = {"type": ctyp}
                cur = cid
            elif "=" in l:
                field,val = l.split("=",1)
                field = field.strip().lower()
                val = val.strip().rstrip(",").strip("{}").strip()
                parsed[cur][field] = parsed[cur].get(field,"") + " " + val
                last = field
            elif last:
                val = l.strip().strip("{}").rstrip(",")
                if val: parsed[cur][last] += " " + val
    return parsed

def writeJSON(data):
    with codecs.open(bibJsFile,"w","utf-8") as f:
        f.write("define({ entries : ")
        json.dump(data,f,indent=2,ensure_ascii=False)
        f.write("});")

def listAvailable(dirPath, exts, outFile, varname):
    names = [f[:-4] for f in os.listdir(dirPath) if f.lower().endswith(exts)]
    with open(outFile,"w") as f:
        f.write(f"define({{{varname}: {json.dumps(names)}}});")

def update():
    print(">>> regenerating SurVis data …")
    writeJSON(parseBibtex(bibFile))
    listAvailable(papersPdfDir, (".pdf",), availablePdf, "availablePdf")
    listAvailable(papersImgDir, (".png",".jpg"), availableImg, "availableImg")  # ★ 支持 jpg
    print(">>> done")

# ------- run once immediately -------
update()

prev = os.stat(bibFile).st_mtime
while True:
    try:
        cur = os.stat(bibFile).st_mtime
        if cur != prev:
            update()
            prev = cur
        else:
            print("waiting for changes in", bibFile)
    except FileNotFoundError:
        print("ERROR: check path to bibFile", file=sys.stderr)
    time.sleep(1)
