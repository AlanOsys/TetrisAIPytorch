

import torch
import random
import numpy as np
from collections import deque
import TetrisFile
from model import Linear_QNet, QTrainer
import pygame
#from helper import plot
import time
import os

fps = 25
counter = 0
MAX_MEMORY = 100000
BATCH_SIZE = 50
LR = 0.0005

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # rng
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)#popleft
        self.model = Linear_QNet(203,256,4)
        self.trainer = QTrainer(self.model, lr=LR, gamma = self.gamma)
        #self.model = Linear_QNet(203,256,4)
        if os.path.exists('./model/model.pth'):
            #os.makedirs('./model/model.pth')
            self.model.load_state_dict(torch.load('./model/model.pth'))
        #print("YES")
   

    def get_state(self,game):
        field = game.getField()
        field = np.array(field)
        field = field.reshape(200,)
        
        field = np.append(field,[game.figure.x,game.figure.rotation,game.figure.y])
        #print((field))
        
        state = field
        state = np.array(state)
        state = state.reshape(203,)
        #print(state)
        return np.array(state, dtype=int)
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state,action,reward,next_state,done))
        #print(self.memory)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)#list of tuples
        else:
            mini_sample = self.memory
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)
    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    def get_action(self,state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    counter = 0
    agent = Agent()
    game = TetrisFile.Tetris(20,10)
    if game.figure == None:
        game.figure = game.new_figure()
        #print("X",game.figure.x)
    
    while True:
        #reward = game.getReward()
        #counter += 1 

        
        
    
        
        #print(field)
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)
       
        reward, done, score = game.play_step(final_move)
        #print(score)
        #time.sleep(0.3)
        #reward += 3.5*(counter/100)
        #if game.break_lines():
         #   reward += 15
        
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old,final_move, reward, state_new, done)

        agent.remember(state_old,final_move, reward, state_new, done)
        if done:
            counter = 0
            #train long memory
            #game.reset()
            
            agent.n_games += 1
            agent.train_long_memory()
            if score >= record and score > 0:
                record = score
                agent.model.save()

            print('Game', agent.n_games,'Score',score,'Record:',record,"Reward:", reward)
            done = False
            
            #game.__init__(20,10)
            #print(plot_scores)
            #print(plot_mean_scores)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            #plot(plot_scores,plot_mean_scores)
            
            
        

if __name__ == '__main__':
    train()