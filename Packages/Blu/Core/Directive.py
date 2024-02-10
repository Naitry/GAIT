from Blu.Core.Information import InformationFragment as InfoFrag


class Directive(InfoFrag):
	def __init__(self,
				 body: str = ""):
		super().__init__(body=body)
