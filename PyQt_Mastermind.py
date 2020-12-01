# mastermind game with PyQt

# written by Hade3 - version 0.5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
import functools
import random

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Mastermind Project')
windowLayout = QVBoxLayout()
inputButtonLayout = QGridLayout()

# Input Button Generation
inputBtn = list(range(9))
for x in range(9):
    inputBtn[x] = QPushButton(str(x + 1))
    # inputBtn[x].setFixedSize(250,250)
    inputBtn[x].setFont(QFont('Arial', 30))

# inputButtonLayout generator
btn = 0
for y in range(3):
    for x in range(3):
        inputButtonLayout.addWidget(inputBtn[btn], 3 - y, x + 1)
        btn += 1

deleteBtn = QPushButton('Del.')
# deleteBtn.setFixedSize(250,250)
deleteBtn.setFont(QFont('Arial', 30))
comfirmBtn = QPushButton('Ent.\n')
# comfirmBtn.setFixedSize(250,510)
comfirmBtn.setFont(QFont('Arial', 30))
inputButtonLayout.addWidget(deleteBtn, 1, 4)
inputButtonLayout.addWidget(comfirmBtn, 2, 4, 2, 1)

# phrase generation
def randomPhrase():
    phrase = [random.randint(1, 9)]
    for x in range(3):
        a = random.randint(1, 9)
        while a in phrase:
            a = random.randint(1, 9)
        phrase.append(a)
    return phrase

phrase = randomPhrase()
turn = 1

# game main frame
playerPhraseLayout = QVBoxLayout()
currentPhraseLayout = QHBoxLayout()
currentTitleLabel = QLabel('Phrase :')
currentTitleLabel.setFont(QFont('Arial', 20))
currentPhraseLayout.addWidget(currentTitleLabel)
playerPhraseLabel = list(range(4))

playerPhrase = []

def takeInput(x):
    if len(playerPhrase) < 4:
        playerPhrase.append(x)
        playerPhraseLabel[len(playerPhrase) - 1] = QLabel(str(x))
        playerPhraseLabel[len(playerPhrase) - 1].setFont(QFont('Arial', 30))
        currentPhraseLayout.addWidget(playerPhraseLabel[len(playerPhrase) - 1])


def deleteInput():
    if len(playerPhrase) >= 1:
        playerPhrase.pop(len(playerPhrase) - 1)
        playerPhraseLabel[len(playerPhrase)].setParent(None)

# comfirm try
comfirmedPhrasesLayout = QVBoxLayout()
comfirmedPhraseLayout = list(range(4))
comfirmedPhraseLabel = list(range(4))
for x in range(4):
    comfirmedPhraseLayout[x] = QHBoxLayout()
    comfirmedPhrasesLayout.addLayout(comfirmedPhraseLayout[x])

def comfirmInput():
	global turn
	if (len(playerPhrase) == 4) & (turn < 5):
		comfirmedPhrase = playerPhrase
		checkResult = checker(playerPhrase, phrase, turn)
		comfirmedPhraseLayout[turn - 1].addWidget(QLabel(str(turn)))
		for i in range(4):
			comfirmedPhraseLabel[i] = QLabel('       '+str(comfirmedPhrase[i]))
			if checkResult[i]=='X':
				comfirmedPhraseLabel[i].setStyleSheet('background-color: red')
			elif checkResult[i]=='A':
				comfirmedPhraseLabel[i].setStyleSheet('background-color: yellow')
			elif checkResult[i]=='O':
				comfirmedPhraseLabel[i].setStyleSheet('background-color: green')
			comfirmedPhraseLayout[turn - 1].addWidget(comfirmedPhraseLabel[i])
	playerPhrase.clear()
	for i in range(4):
		playerPhraseLabel[i].setParent(None)
	turn = turn + 1

def checker(plPhrase, winPhrase, turn):
	checkerString = ''
	for x in range(4):
		if (plPhrase[x] in winPhrase) & (plPhrase[x] != winPhrase[x]):
			checkerString = checkerString + 'A'
		elif plPhrase[x] == winPhrase[x]:
			checkerString = checkerString + 'O'
		else:
			checkerString = checkerString + 'X'

	if checkerString == 'OOOO':
		winLabel = QLabel('you win')
		playerPhraseLayout.addWidget(winLabel)
	elif (checkerString != 'OOOO') & (turn == 4):
		winLabel = QLabel('you lose ' + str(phrase))
		playerPhraseLayout.addWidget(winLabel)
	return checkerString

comfirmBtn.clicked.connect(comfirmInput)

for x in range(9):
    inputBtn[x].clicked.connect((functools.partial(takeInput, int(x + 1))))

deleteBtn.clicked.connect(deleteInput)

# General Layout Generation
playerPhraseLayout.addLayout(currentPhraseLayout)
playerPhraseLayout.addLayout(comfirmedPhrasesLayout)
windowLayout.addLayout(playerPhraseLayout)
windowLayout.addLayout(inputButtonLayout)

window.setLayout(windowLayout)
window.show()

sys.exit(app.exec_())
