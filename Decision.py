from datetime import datetime

from collaborator import Collaborator

class Decision:
    def __init__(self, collaborator, responsible, urgency = 5, importance = "normal") -> None:
        self.collaborator:Collaborator = collaborator
        self.responsible:Collaborator = responsible
        self.urgency = urgency #estimation in days of how long the decision should take
        self.importance = importance
        self.beginning = datetime.now()

#include and observer strategy to check whether the time has past.... 

    def grow_decision():
        pass

    def color_decision():
        pass