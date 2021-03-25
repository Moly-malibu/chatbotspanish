import numpy as np
import random
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from process import bag_words, token, stem
from model import NeuralNet

# 1. load Data from Json:
with open('es.json', 'r') as f: #Load data from json db
    talks =  json.load(f)

# 2. Create loops, extend and append:
tags = []
wordsAll = []
result = []

for talk in talks['talks']: 
    tag = talk['tag']
    tags.append(tag) #add tag list
    for pattern in talk["patterns"]:
        wordsToken = token(pattern)
        wordsAll.extend(wordsToken) #extend or add the words list
        result.append((wordsToken, tag)) # add result 

# 3. Clean unnecesary gramma simbols:
clean_simbols = ['.', '!', '?']
wordsAll = [stem(w) for w in wordsAll  if wordsToken not in clean_simbols]
wordsAll = sorted(set(wordsAll))
tags = sorted(set(tags))

# 4. Creaate Traing Data
X_train = []
y_train = []

for (patternSent, tag) in result:
    bag = bag_words(patternSent, wordsAll)
    X_train.append(bag) #add x_train bag
    label = tags.index(tag)
    y_train.append(label) # add y_train label

X_train = np.array(X_train) #numpy array train
y_train = np.array(y_train)

# 5. Parameters
epochs = 1000
batch_size = 8
rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)

# 6. from data set in json to see size and get sample:
class Chat(Dataset):
    def __init__(self):
        self.samples = len(X_train)
        self.X = X_train
        self.y = y_train
    
    def __getitem__(self, index): # get sample
        return self.X[index], self.y[index]
    
    def __len__(self):  #see data size
        return self.samples

# 7. Parameter for Train Model:
dataset = Chat()
trainLoad = DataLoader(dataset=dataset, 
                        batch_size=batch_size,
                        shuffle=True,
                        num_workers=0)
# 8. USE CPU 
cpu = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 9. MODEL
model = NeuralNet(input_size, hidden_size, output_size). to(cpu)

# 10. LOSS and OPTIMIZER
criter = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=rate)

# 11. TRAIN THE MODEL
for epoch in range(epochs):
    for (words, labels) in trainLoad:
        words = words.to(cpu)
        labels = labels.to(dtype=torch.long).to(cpu)
        outputs = model(words)
        loss = criter(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch+1) % 100  == 0:
        print (f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
print(f'final loss: {loss.item():.4f}')

# 12. load and saved final model

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"wordsAll": wordsAll,
"tags": tags
}

FILE = 'data.pth'
torch.save(data, FILE)
print(f'training complete. file saved to {FILE}')
