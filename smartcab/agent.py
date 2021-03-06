import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.gamma = 0           # Discount factor
        self.prev_state = None   # State the agent was in previously
        self.prev_action = None  # Previous action taken by the agent
        self.prev_reward = None  # Previous reward awarded to the agent
        self.def_Q = 0          # Default Q value to initialize the Q table
        self.n_trial = 0
        

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        self.n_trial = self.n_trial + 1

        if (testing):
            self.alpha = 0
            self.epsilon = 0
        else:
#            self.epsilon = self.epsilon  - 0.05
#            self.epsilon = 1 - 0.99 * math.e ** ( -math.e ** (-0.03 *(self.n_trial - 150)))
            #self.epsilon = 1 - 0.99 * math.e ** ( -math.e ** (-0.0177 *(self.n_trial - 200)))
            self.epsilon = 1 - 0.99 * math.e ** ( -math.e ** (-0.014 *(self.n_trial - 200)))
#            self.epsilon =math.e**(-.08*self.n_trial)


        self.gamma = 0           # Discount factor
        self.prev_state = None   # State the agent was in previously
        self.prev_action = None  # Previous action taken by the agent
        self.prev_reward = None  # Previous reward awarded to the agent


        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        # When learning, check if the state is in the Q-table
        #   If it is not, create a dictionary in the Q-table for the current 'state'
        #   For each action, set the Q-value for the state-action pair to 0
        
        state ={"light": inputs["light"],"oncoming": inputs["oncoming"],"left": inputs["left"],"waypoint": waypoint}
#        print("State =", state)        
        state = tuple(state.values())
#        print("State_tuple =", state)
        
        
        
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ = None
        maxQ_action = None
#        maxQ = 0


        if state in self.Q: #Check that the state is in the dictionary
            maxQ_action = max(self.Q[state])
            for actions in self.valid_actions:
                if maxQ < self.Q[state][actions]:
                    maxQ = self.Q[state][actions]

        print(" Max Q = ", maxQ , maxQ_action)        

        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        def_q_val=0.0
#        if self.learning is True:
#            if state not in self.Q.keys():
#                for action in self.valid_actions:
#                    self.Q={"light": 0.0,"oncoming": 0.0,"left": 0.0,"right": 0.0,"waypoint": 0.0}
#            else :
#             print("Self Q =", self.Q )      
       
        if self.learning is True:
            if state not in self.Q:
                self.Q[state] ={}
                for action in self.valid_actions:
                   self.Q[state][action] = def_q_val            
                    #self.Q =0

#        print (type(state), state)
#        
#        self.Q ={0,0}
#        print("State  ==",self.state,"  Actoon =",self.valid_actions)
        return self.Q


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
#        if not self.learning:
#            action = random.choice(self.valid_actions)

#        if not self.learning:
#            action = random.choice(self.valid_actions)
            
#        if random.random() <= self.epsilon:
#            action = random.choice(self.valid_actions)
#        else:
#            action = self.get_maxQ(self,state)
#        print(" self.get_maxQ(state) ", self.get_maxQ(state))    
        if not self.learning:
            action = random.choice(self.valid_actions)
        else:
            if random.random() <= self.epsilon:
                action = random.choice(self.valid_actions)
            else:
                maxQ = self.get_maxQ(state)
                best_actions = []
                for act in self.Q[state]:
                    if self.Q[state][act] == maxQ:
                        best_actions.append(act)
                if (len(best_actions) > 0):
                    action = random.choice(best_actions)
#        print(" self.Q[state] ",  self.Q[state])            
#        print("Action =",action)
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
#        q_key = self.createQ(state)
#        print("q_key = ",q_key)
#        cur_value = self.q_value_for(state, action)
#        inputs = self.env.sense(self)
#        self.next_waypoint = self.planner.next_waypoint()
#        new_state = self.build_state(inputs)
#        learned_value = reward + (self.discount_rate * self.max_q_value(new_state))
#        new_q_value = cur_value + (self.learning_rate * (learned_value - cur_value))
#        self.q_values[q_key] = new_q_value
        
        #self.Q[state][action] += self.alpha * reward
#        if self.learning is True:
#            new_value = self.alpha*reward
#            old_value = self.Q[self.prev_state][action]
#            self.Q[self.prev_state][action] = (1 - self.alpha)*old_value + new_value
#            self.Q = {'reward', self.alpha*reward}
#        oldv = self.Q.get((state, action), None)
#        oldv =  None
#        if oldv is None:
#            self.Q[(state, action)] = reward
#        else:
#            self.Q[(state, action)] = oldv + self.alpha * (1 - oldv)  
#        next_state = self.build_state()
#        self.createQ(next_state)

        if (self.learning):            
            self.Q[state][action] = (1-self.alpha) * self.Q[state][action] + self.alpha * reward
        return



    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent,learning=True, alpha = 0.6, epsilon = 0.1)
    
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline =True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env,update_delay=0.0,  display =True, log_metrics=True, optimized=True)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(tolerance = 0.01001, n_test=10)
    print "CONCLUSION REPORT"
    print "WINS: {}".format(env.wins)
    print "LOSSES: {}".format(env.losses)
    print "INVALID MOVES: {}".format(env.infractions)



if __name__ == '__main__':
    run()
