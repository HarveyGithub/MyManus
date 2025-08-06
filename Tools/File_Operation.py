import os
def Read_File(FilePath, StartLine=0, EndLine=0):
    try:
        content = ""
        with open(FilePath, "r") as f:
            idx = 0
            for line in f.readlines():
                idx+=1
                if idx > StartLine:
                    content += line
                if idx >= EndLine and EndLine != 0:
                    break
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

def Write_File(FilePath, Content):
    try:
        with open("./WorkSpace/" + FilePath, "w") as f:
            f.write(Content)
        return "File written successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def Append_File(FilePath, Content):
    try:
        with open("./WorkSpace/" + FilePath, "a") as f:
            f.write(Content)
        return "Content appended successfully"
    except Exception as e:
        return f"Error: {str(e)}"
os.system("pwd")
print(Read_File("./Tools/Tools.py"))