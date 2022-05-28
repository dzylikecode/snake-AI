class SnakeAgent:

    def __init__(self):
        self.game = None
        self.model = None
        self.data_set = None

    def main(self):
        
        state = self.get_state(self.game)

        action = self.model.predict(state)

        feedback = self.game.play_step(action)

        self.data_set.record(state, action, feedback)

        self.model.train(self.data_set)

    def get_state(self, game):
        pass
