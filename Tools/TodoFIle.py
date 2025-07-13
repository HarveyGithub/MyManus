import os

def Make_Todo_File(Tittle, TodoList):
    with open("/home/noi/MyManus/WorkSpace/Todo.md", "w") as f:
        f.write(f"# {Tittle}\n")
        f.write("\n")
        i = 0
        # print(TodoList)
        for SubileTodo in TodoList:
            f.write(f"## {SubileTodo}\n")
            f.write("\n")
            f.write(f"[ ] {TodoList[SubileTodo]}\n")
            f.write("\n")