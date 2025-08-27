import json
import os

class Memory:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.data = []
        self.filename = f"agent_{agent_id}_memory.json"
        self.load()

    def add(self, action, result):
        self.data.append({"action": action, "result": result})

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def analyze(self):
        deaths = sum(1 for m in self.data if m["result"] == "dead")
        heals = sum(1 for m in self.data if m["action"] == "heal")
        attacks = sum(1 for m in self.data if m["action"] == "attack" and m["result"] == "success")
        return {"deaths": deaths, "heals": heals, "attacks": attacks}

    def clear(self):
        self.data = []
        self.save()