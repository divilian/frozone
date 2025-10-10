from abc import ABC , abstractmethod

class Detector(ABC):
	
	@abstractmethod
	def detect(self , text , **kwargs):
		pass
