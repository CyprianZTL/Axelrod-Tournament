from flask import Flask, render_template
import random

app = Flask(__name__)

#def
class AlwaysFair:
    def __init__(self):
        self.name = "Always Fair"

    def decision(self, opponent_history):
        return 1  # Fair

class AlwaysUnfair:
    def __init__(self):
        self.name = "Always Unfair"

    def decision(self, opponent_history):
        return -1  # Unfair

class Random:
    def __init__(self):
        self.name = "Random"

    def decision(self, opponent_history):
        return random.choice([1, -1])

class TitForTat:
    def __init__(self):
        self.name = "Tit for Tat"

    def decision(self, opponent_history):
        if not opponent_history:
            return 1  # Fair initially
        return opponent_history[-1]  # Mimic the opponent's last move

class ForgivingTitForTat:
    def __init__(self):
        self.name = "Forgiving Tit for Tat"

    def decision(self, opponent_history):
        if not opponent_history:
            return 1  # Fair initially
        if opponent_history[-1] == -1 and random.random() > 0.1:
            return 1  # Forgive with 90% chance
        return opponent_history[-1]

class GrimTrigger:
    def __init__(self):
        self.name = "Grim Trigger"
        self.triggered = False

    def decision(self, opponent_history):
        if self.triggered:
            return -1  # Unfair after opponent's first unfair move
        if -1 in opponent_history:
            self.triggered = True
            return -1
        return 1  # Fair initially

#kalkulacja kary
def myPenalty(myDecision, hisDecision):
    if myDecision == -1 and hisDecision == -1:
        return 7
    if myDecision == 1 and hisDecision == 1:
        return 3
    if myDecision == -1 and hisDecision == 1:
        return 0
    if myDecision == 1 and hisDecision == -1:
        return 10

#fukcja jednej rundy
def play_round(strategy1, strategy2, history1, history2):
    decision1 = strategy1.decision(history2)
    decision2 = strategy2.decision(history1)
    penalty1 = myPenalty(decision1, decision2)
    penalty2 = myPenalty(decision2, decision1)
    history1.append(decision1)
    history2.append(decision2)
    return penalty1, penalty2

#powtorzenie rundy 1000 razy
def simulate_tournament(strategies, rounds=1000):
    results = {strategy.name: {opponent.name: 0 for opponent in strategies} for strategy in strategies}

    for i, strategy1 in enumerate(strategies):
        for j, strategy2 in enumerate(strategies):
            if i != j:
                history1, history2 = [], []
                total_penalty1, total_penalty2 = 0, 0
                for _ in range(rounds):
                    penalty1, penalty2 = play_round(strategy1, strategy2, history1, history2)
                    total_penalty1 += penalty1
                    total_penalty2 += penalty2
                results[strategy1.name][strategy2.name] = total_penalty1
                results[strategy2.name][strategy1.name] = total_penalty2

    return results

@app.route('/')
def index():
    strategies = [AlwaysFair(), AlwaysUnfair(), Random(), TitForTat(), ForgivingTitForTat(), GrimTrigger()]
    results = simulate_tournament(strategies)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
