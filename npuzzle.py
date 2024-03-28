import random
from copy import deepcopy
import numpy as np
import time
import os

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
while True:
   n = int(input())
   if n < 10:
       break

def shuffle_list(board_list):
    # Tạo một hoán vị ngẫu nhiên của các chỉ số (ngoại trừ index 0)
    indices_except_first = list(range(1, len(board_list)))
    random.shuffle(indices_except_first)

    # Tạo danh sách mới với vị trí đã được đánh tráo (ngoại trừ index 0)
    shuffled_list = [board_list[0]] + [board_list[i] for i in indices_except_first]
    return shuffled_list

def createBoard(flat_list):
    reshaped_list = np.array(flat_list).reshape((int(n), int(n))).tolist()
    return reshaped_list

#//create Board
END = createBoard(list(range(n*n)))
board = createBoard(shuffle_list(list(range(n*n))))

class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h
    
def get_pos(current_state, element):
    for row in range(n):
        if element in current_state[row]:
            return (row, current_state[row].index(element))
        
def euclidianCost(current_state):
    cost = 0
    for row in range(n):
        for col in range(n):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            # listNode += [Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir)]
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))
    return listNode
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

def printboard(board):
    for i in board:
        for j in i:
            if j == 0:
                print(" " , end=" ")
                continue
            print(j, end= " ")
        print(end="\n")
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

if __name__ == '__main__':
    #it is start matrix
    br = main(board)
    print()
    for b in br:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'U':
                letter = 'UP'
            elif b['dir'] == 'R':
                letter = "RIGHT"
            elif b['dir'] == 'L':
                letter = 'LEFT'
            elif b['dir'] == 'D':
                letter = 'DOWN'
            os.system('cls')
            print(letter)
        printboard(b['node'])
        time.sleep(1)
    print('total steps : ', len(br) - 1)
    print('ABOVE IS THE OUTPUT')