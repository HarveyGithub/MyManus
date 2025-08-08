import os
def Read_File(file_path, start_line=0, end_line=0):
    try:
        content = ""
        with open(file_path, "r") as f:
            idx = 0
            for line in f.readlines():
                idx+=1
                if idx >= start_line:
                    content += line
                if idx >= end_line and end_line != 0:
                    break
        return content
    except FileNotFoundError:
        return "错误: File not found"
    except Exception as e:
        return f"错误: {str(e)}"

def Write_File(file_path, content, append=False, front_newline=False, end_newline=False):
    try:
        with open(file_path, "a" if append else "w", encoding="utf-8") as f:
            if front_newline:
                f.write("\n")
            f.write(content)
            if end_newline:
                f.write("\n")
        return "成功写入文件"
    except Exception as e:
        return f"错误: {str(e)}"
    
def Edit_File(file_path, content):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for key in content:
            lines[key-1] = content[key] + '\n'
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return "成功修改文件"
    except FileNotFoundError:
        return "错误: File not found"
    except Exception as e:
        return f"错误: {str(e)}"
    
if __name__ == '__main__':
    print(Write_File(os.path.join("/home/harvey/Lysandra/WorkSpace/", "hello.py"), "print('Hello, World!')"))