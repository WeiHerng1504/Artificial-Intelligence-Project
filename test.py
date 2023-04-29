import os
import neat

# red is positive
# blue is negative

start_grid = [0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 1, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0]

class Test:
    def __init__(self):
        self.grid = start_grid
        self.turn_number = 0
        self.player = 0

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        # run = True
        # while run:

        #     output1 = net1.activate(
        #         (self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
        #     decision1 = output1.index(max(output1))

        #     if decision1 == 0:
        #         pass
        #     elif decision1 == 1:
        #         self.game.move_paddle(left=True, up=True)
        #     else:
        #         self.game.move_paddle(left=True, up=False)

        #     output2 = net2.activate(
        #         (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
        #     decision2 = output2.index(max(output2))

        #     if decision2 == 0:
        #         pass
        #     elif decision2 == 1:
        #         self.game.move_paddle(left=False, up=True)
        #     else:
        #         self.game.move_paddle(left=False, up=False)

      

        #     if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
        #         self.calculate_fitness(genome1, genome2, game_info)
        #         break

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Test()
            game.train_ai(genome1, genome2, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    # with open("best.pickle", "wb") as f:
    #     pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # run_neat(config)
    #test_ai(config)