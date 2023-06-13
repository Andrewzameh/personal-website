import json
import requests
from flask import Blueprint, render_template, request, Response
from flask import Flask, render_template

import json
import re


ai = Blueprint("ai", __name__)

USER= "USER:"
BOT= "AIMY:"
CONTEXT= "A chat between a curious user and an artificial intelligence assistant named AIMY. AIMY gives helpful, detailed, and polite answers to the user's questions. AIMY is created by a team in FlairsTech\n\n"
MAINCONTEXT = "A chat between a curious user and an artificial intelligence assistant named AIMY. AIMY gives helpful, detailed, and polite answers to the user's questions.\n\n"
# URISTREAM = "http://54.144.255.165:5660/v1/chat/completions"
URISTREAM = "http://0.0.0.0:5660/v1/chat/completions"
# URI = "http://54.144.255.165:5000/api/v1/generate"
# URI = "http://54.144.255.165:5000/api/v1/generate"
# VURL = 'http://54.144.255.165:9000/asr'
VURL = 'http://0.0.0.0:9000/asr'

SECRET_KEY = 'asdfasdf4q89w0f4q4fasdfasda3c'



conversation = [CONTEXT]

def getPrompt(userInput,mode,customPrompt):
    global conversation
    if mode == "reset":
        conversation = [CONTEXT]
    elif mode == "answer":
        conversation[-1] = f'{BOT}{userInput}'
    elif mode == "oneshot":
        mailRows = [
            f"{MAINCONTEXT}",
            f"{USER}{customPrompt}{userInput}\n",
            f"{BOT}",
        ]
        return "".join(mailRows)
    elif mode == "conversation":
        chatRows = [
            f"{USER}{customPrompt}{userInput}\n",
            f"{BOT}",
        ]
        conversation += chatRows
        return "".join(conversation)

# def directRequest(context):
#     requestBody = {
#             "prompt": context,
#             "max_new_tokens": 2000 ,
#             "do_sample": True,
#             "temperature": 0.7,
#             "top_p": 0.5,
#             "typical_p": 1,
#             "repetition_penalty": 1.2,
#             "top_k": 40,
#             "min_length": 0,
#             "no_repeat_ngram_size": 0,
#             "num_beams": 1,
#             "penalty_alpha": 0,
#             "length_penalty": 1,
#             "early_stopping": False,
#             "seed": -1,
#             "add_bos_token": True,
#             "truncation_length": 2048,
#             "ban_eos_token": False,
#             "skip_special_tokens": True,
#             "stopping_strings": ['\n##', '\n### Assistant:',"\n### Human:"],
#         }
#     response = requests.post(URISTREAM, json=requestBody)
#     if response.status_code == 200:
#         result = response.json()["results"][0]["text"]
#         print("result: %s" %(result))
#         return result[:-2]

@ai.route("/ProEmail", methods=["GET", "POST"])
def mailIndex():
    return render_template("ai-emails.html")


@ai.route("/emailRes", methods=["GET", "POST"])
def email_response():
    userInput = request.args.get("msg")
    style = request.args.get("style")
    finalPrompt = getPrompt(userInput, 'oneshot',f'Write a {style} email about the following: ')
    print("finalPrompt: %s" %(finalPrompt))
    
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "model": "text-embedding-ada-002",
        "messages": finalPrompt,
        "temperature": 0.7,
        "top_p": 0.3,
        "n": 1,
        "max_tokens": 800,
        "stop": "USER:",
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "user": "USER:",
    }

    response = requests.post(URISTREAM, headers=headers, json=data, stream=True)
    
    def generate():
        FinalRes = ""
        for line in response.iter_lines():
            line = line[6:]
            if line:
                # print("line: %s" %(line))
                try:
                    # Parse the line as JSON
                    response_data = json.loads(line.decode("utf-8"))
                    # print("response_data: %s" %(response_data))

                    if "choices" in response_data:
                        choices = response_data["choices"]
                        for choice in choices:
                            if "content" in choice["delta"]:
                                content = choice["delta"]["content"]
                                if content:
                                    FinalRes += content
                                    htmlAnswer = "<p>" + FinalRes.replace("\n", "<br>") + "</p>"
                                    # print("htmlAnswer: %s" %(htmlAnswer))
                                    response_dict = {"content": htmlAnswer}
                                    yield f"data: {json.dumps(response_dict)}\n\n"                                    
                    if (
                        "object" in response_data
                        and response_data["object"] == "chat.completion.chunk"
                    ):
                        # Streaming has finished
                        response_dict = {"streaming_completed": True}
                        yield f"data: {json.dumps(response_dict)}\n\n"  
                        break

                except json.decoder.JSONDecodeError:
                    # Print the response content if it's not valid JSON
                    print('Invalid JSON:', line.decode('utf-8'))
                    pass
    
    return Response(generate() , mimetype='text/event-stream')

@ai.route("/gpt-conv")
def index():
    return render_template("gptconversation.html")


FinalRes = ''
@ai.route("/AiResponse", methods=["GET", "POST"])
def completion_response():
    global conversation
    user_input = request.args.get("msg")
    if len(conversation) > 15:
        getPrompt('','reset','')
    finalPrompt = getPrompt(user_input, 'conversation','')
    print("finalPrompt: %s" %(finalPrompt))
    # answer = directRequest(finalPrompt)
    
    
    
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "model": "text-embedding-ada-002",
        "messages": finalPrompt,
        "temperature": 0.7,
        "top_p": 0.3,
        "n": 1,
        "max_tokens": 1000,
        "stop": "USER",
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "user": "USER:",
    }

    response = requests.post(URISTREAM, headers=headers, json=data, stream=True)
    
    def generate():
        FinalRes = ""
        for line in response.iter_lines():
            line = line[6:]
            if line:
                try:
                    # Parse the line as JSON
                    response_data = json.loads(line.decode("utf-8"))
                    # print("response_data: %s" %(response_data))

                    if "choices" in response_data:
                        choices = response_data["choices"]
                        for choice in choices:
                            if "content" in choice["delta"]:
                                content = choice["delta"]["content"]
                                if content:
                                    FinalRes += content
                                    print("FinalRes: %s" %(FinalRes))
                                    htmlAnswer = "<p>" + FinalRes.replace("\n", "<br>") + "</p>"
                                    formatted_text = re.sub(r"```(.*?)```", r"<code>\1</code>", htmlAnswer)
                                    # print("htmlAnswer: %s" %(htmlAnswer))
                                    response_dict = {"content": formatted_text}
                                    yield f"data: {json.dumps(response_dict)}\n\n"                                    
                    if (
                        "object" in response_data
                        and response_data["object"] == "chat.completion.chunk"
                    ):
                        # Streaming has finished
                        response_dict = {"streaming_completed": True}
                        yield f"data: {json.dumps(response_dict)}\n\n"  
                        getPrompt(FinalRes,'answer','')
                        break

                except json.decoder.JSONDecodeError:
                    # Print the response content if it's not valid JSON
                    print('Invalid JSON:', line.decode('utf-8'))
                    pass
    
    
    print("conversation: %s" %(conversation))
    return Response(generate() , mimetype='text/event-stream')

@ai.route("/voice")
def voiceGen():
    return render_template("voice.html")


@ai.route("/ASR", methods=["GET", "POST"])
def voiceResponse():
    mode = request.form.get('mode')
    print("mode: %s" %(mode))
    lang = request.form.get('lang')
    print("lang: %s" %(lang))
    output = request.form.get('output')
    print("output: %s" %(output))
    file = request.files['file']
    print("file: %s" %(file))
    answer = f'hi\n{mode}\n{lang}\n{output}\n{file}\n'
    params = {
            "method": 'faster-whisper',
            "task": mode,
            "language": lang,
            "initial_prompt": "",
            "encode": True,
            "output": output,
        }
    data = {
        'audio_file':file
    }
    response = requests.post(VURL,params=params, files={'audio_file':(file.filename, file.stream, file.content_type)})
    # if response.status_code == 200:
    # result = response.json()
    print("result: %s" %(response.text))
    # HTMLFinalRes = "<p>" + result.replace("\n", "<br>") + "</p>"
    return Response(response.text, mimetype='text/plain')
