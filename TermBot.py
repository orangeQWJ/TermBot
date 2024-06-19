#!/usr/bin/python3
# 调用opencvAI的API
import openai
# 用于处理openAI返回的markdown文本
from rich.console import Console
from rich.markdown import Markdown
# 用于读取命令行参数
import sys
# 用于信号捕捉
import os
# 读取环境变量
openai.api_key = os.environ.get('OPENAI_API_KEY')



# 用于显示渲染后的文本
console = Console()


import readline                                                                            
                                                                                           
# 定义一个回调函数，用于自动补全和预设输入                                                 
def completer(text, state):                                                                
    possible_strings = [ 'hello', 'world', 'help', 'exit' ]                                
    matches = [s for s in possible_strings if s.startswith(text)]                          
    if state < len(matches):                                                               
        return matches[state]                                                              
    else:                                                                                  
        return None                                                                        
# 设置自动补全和预设输入的回调函数                                                         
readline.set_completer(completer)                                                          
# 启用自动补全和预设输入                                                                   
readline.parse_and_bind('tab: complete')                                                   
# 不显示底部的行号                                                                         
readline.set_startup_hook(lambda: readline.insert_text(''))                                
# 添加一些默认输入到历史缓冲区中                                                           
#readline.add_history('hello')                                                              
#readline.add_history('world')                                                              
#readline.add_history('help')                                                               
#readline.add_history('exit')                                                               
# 读取用户输入，显示输入历史                                                               
#while True:                                                                                
#    line = input('> ')                                                                     
#    if line == 'exit':                                                                     
#        break                                                                              


# 将你的对chatgpt的设定写在这里，例如：用一个小迷妹的语气和我讲话
messages = [
    {
        "role": "system",
        "content": "你是一个友善的AI助手"
    },
]

# 阅读当前文件,用于代码分析
flag = False
if len(sys.argv) > 1:
    flag = True
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
        messages.append({
            "role": "user",
            "content": contents + "你先看看这些代码"
        })


def getResponse():
    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages
    )
    return response


def getMessages(response):
    responseMessage = response['choices'][0]["message"]["content"]
    return responseMessage


def addMessages(text):
    global messages
    messages.append({
        "role": "user",
        "content": text
    })


def show(text):
    print("🤖   ", end="")
    md = Markdown(text)
    #console.print(md, style="trans")
    console.print(md)
###################
while True:
    # 提出问题
    myQuestion = input("🤔   ")
    # 将出的问题添加到上下文
    addMessages(myQuestion)
    try:
        # 超出max token时会出错
        response = getResponse()
    except:
        print("🤖 🤖 🤖 🤖 🤖 🤖 🤖")
        if flag:
            messages = messages[:2]
        else:
            messages = messages[:1]
        addMessages(myQuestion)
        print("🤖 🤖 🤖 🤖 🤖 🤖 🤖")

        response = getResponse()
    responseMessage = getMessages(response)
    show(responseMessage)
    addMessages(responseMessage)
