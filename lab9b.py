from numpy import random

params = {
    'world_size': (20, 20),
    'num_agents': 380,
    'max_iter': 100,
    'out_path': r'c:\users\sara\desktop\python\week9lab\lab9b\lab9b.csv'
}

class Agent():
    def __init__(self, world):
        self.world = world
        self.location = None

    def move(self):
        vacancies = self.world.find_vacant(return_all=True)
        if vacancies:
            patch = random.choice(vacancies)
            self.world.remove_patch(patch)
            return 1  # Return 1 to indicate one vacancy removed
        return 0  # Return 0 if no vacancies removed

class World():
    def __init__(self, params):
        assert(params['world_size'][0] * params['world_size'][1] > params['num_agents']), 'Grid too small for number of agents.'
        self.params = params
        self.reports = {}

        self.grid = self.build_grid(params['world_size'])
        self.agents = self.build_agents(params['num_agents'])

        self.init_world()

    def build_grid(self, world_size):
        """Create the world that the agents can move around on."""
        locations = [(i, j) for i in range(world_size[0]) for j in range(world_size[1])]
        return {l: None for l in locations}

    def build_agents(self, num_agents):
        """Generate a list of Agents and place them randomly on the grid."""
        agents = [Agent(self) for _ in range(num_agents)]
        random.shuffle(agents)
        return agents

    def init_world(self):
        """Place agents in random vacant spots on the grid."""
        for agent in self.agents:
            loc = self.find_vacant()
            if loc is not None:  # Ensure a location is found
                self.grid[loc] = agent
                agent.location = loc

        assert all(agent.location is not None for agent in self.agents), "Some agents don't have homes!"
        assert sum(occupant is not None for occupant in self.grid.values()) == self.params['num_agents'], 'Mismatch between number of agents and number of locations with agents.'

    def find_vacant(self, return_all=False):
        """Find all empty patches on the grid and return a random one or a list of all empty patches."""
        empties = [loc for loc, occupant in self.grid.items() if occupant is None]
        if return_all:
            return empties
        else:
            if empties:  # Ensure there are vacant patches to choose from
                return random.choice(empties)
            return None  # Return None if no vacant patches

    def remove_patch(self, patch):
        """Remove a patch from the grid."""
        if patch in self.grid:
            self.grid[patch] = None

    def run(self):
        """Handle the iterations of the model."""
        self.reports['vacant_removed'] = []

        for iteration in range(self.params['max_iter']):
            random.shuffle(self.agents)  # Randomize agents before every iteration
            total_removed = 0

            for agent in self.agents:
                removed = agent.move()
                total_removed += removed

            self.reports['vacant_removed'].append(total_removed)

            if total_removed == 0:
                print(f'No more vacant patches to remove. Stopping after iteration {iteration}.')
                break

        self.report()

    def report(self, to_file=True):
        """Report final results after run ends."""
        reports = self.reports

        print('\nAll results begin at time=0 and go in order to the end.\n')
        print('Number of vacant patches removed per iteration:', reports['vacant_removed'])

        if to_file:
            out_path = self.params['out_path']
            with open(out_path, 'w') as f:
                headers = 'iteration,vacant_removed\n'
                f.write(headers)
                for i in range(len(reports['vacant_removed'])):
                    line = f'{i},{reports["vacant_removed"][i]}\n'
                    f.write(line)
            print('\nResults written to:', out_path)

world = World(params)
world.run()
