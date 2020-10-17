from abc import ABC, abstractmethod

class Agent(ABC):

  @abstractmethod
  def action(self, env, last_action):
    pass