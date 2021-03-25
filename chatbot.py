import random
import json
import torch
from model import NeuralNet
from process import bag_words, token

cpu = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 1. Load Data json

with open('es.json', 'r') as dataJson:
    talks = json.load(dataJson)

# 2. Load Model with the different levals 
chatData = 'data.pth'
data = torch.load(chatData)

input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
wordsAll = data['wordsAll']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size).to(cpu)
model.load_state_dict(model_state)
model.eval()

# 3. Programmer chat with the bot:
bot = 'Sofy'
def get_response(msg):
    sentence = token(msg)
    X = bag_words(sentence, wordsAll)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(cpu)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item()>0.75:
        for talk in talks['talks']:
            if tag == talk['tag']:
                return random.choice(talk['responses'])
    return 'Disculpe, Aun no tengo informacion acerca de su pregunta!'
