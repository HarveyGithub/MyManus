def make_prompts(Message):
    sysprompt=''
    assprompt=''
    Message.append({'role':'system','content':sysprompt})
    Message.append({'role':'assistant','content':assprompt})