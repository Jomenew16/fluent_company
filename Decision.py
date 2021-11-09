from datetime import datetime

class Decision:
    def __init__(self, collaborator, responsible, urgency = 5, importance = "normal") -> None:
        self.collaborator = collaborator
        self.responsible = responsible
        self.urgency = urgency #estimation in days of how long the decision should take
        self.importance = importance
        self.beginning = datetime.now()

#include and observer strategy to check whether the time has past.... 