from autogoal.kb import AlgorithmBase
from autogoal.grammar import ContinuousValue, CategoricalValue, DiscreteValue
from ._semantics import GameStructure, Player
from .NeuralNet import NeuralNetwork
from .Agent import AlphaZeroAgent


class AlphaZeroAlgorithm(AlgorithmBase):
    def __init__(
        self,
        reg_const: ContinuousValue(0.0001, 0.001),
        learning_rate: ContinuousValue(0.0001, 0.5),
        batch_size: CategoricalValue(8, 16, 32, 64, 128, 256),
        epochs: DiscreteValue(10, 100),
        num_iters: DiscreteValue(10, 100),
        queue_len: DiscreteValue(20000, 40000),
        episodes: DiscreteValue(50, 100),
        memory_size: DiscreteValue(300, 1000),
        arena_games: DiscreteValue(40, 100),
        update_threshold: ContinuousValue(0.6, 0.99),
    ) -> None:
        self.reg_const = reg_const
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.num_iters = (num_iters,)
        self.queue_len = queue_len
        self.episodes = episodes
        self.memory_size = memory_size
        self.arena_games = arena_games
        self.update_threshold = update_threshold

    def run(self, game: GameStructure) -> Player:
        # First step, construct a CNN model
        # and train it with the hyperparameters
        # defined for this algorithm instance
        cnn = NeuralNetwork(
            self.reg_const, self.learning_rate, self.batch_size, self.epochs, game
        )
        agent = AlphaZeroAgent(game, cnn)

        # Train the agent
        agent.train(
            num_iters=self.num_iters,
            arena_games=self.arena_games,
            episodes=self.episodes,
            queue_len=self.queue_len,
            update_threshold=self.update_threshold,
        )

        return agent