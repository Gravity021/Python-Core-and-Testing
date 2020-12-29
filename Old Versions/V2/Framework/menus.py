class MenuFuncs:
    def __init__(self, transition):
        self.transition = transition

    def play(self):
        self.transition.target = "test_0.json"
        self.transition.transitioning = True