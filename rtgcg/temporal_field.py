"""
Temporal Field module for the RTGCG system.
This module handles the time-evolving probabilistic fields that represent system states over time.
"""

import numpy as np

class TemporalField:
    def __init__(self, time_steps=100, state_dim=64):
        """
        Initialize the Temporal Field.
        
        Args:
            time_steps (int): Number of time steps to track in the temporal evolution.
            state_dim (int): Dimensionality of the state space at each time step.
        """
        self.time_steps = time_steps
        self.state_dim = state_dim
        self.states = np.zeros((time_steps, state_dim))
        self.current_time = 0
        
        # Initialize with small random values to simulate initial conditions
        self.states[0] = np.random.normal(0, 0.1, state_dim)
    
    def evolve(self, input_data):
        """
        Evolve the temporal field based on input data.
        Simulates time-dependent state transformations.
        
        Args:
            input_data (np.ndarray): Input data to influence the evolution.
            
        Returns:
            np.ndarray: Current state after evolution.
        """
        if self.current_time < self.time_steps - 1:
            self.current_time += 1
            
            # Simulate temporal evolution with a simple linear transformation
            # influenced by input data and previous state
            influence = np.mean(input_data, axis=-1) if input_data.ndim > 1 else input_data
            self.states[self.current_time] = (0.9 * self.states[self.current_time - 1] + 
                                             0.1 * influence[:self.state_dim] if len(influence) >= self.state_dim 
                                             else np.pad(influence, (0, self.state_dim - len(influence))))
            
            # Add small noise to simulate chaotic temporal dynamics
            self.states[self.current_time] += np.random.normal(0, 0.01, self.state_dim)
        
        return self.states[self.current_time]
    
    def update_from_feedback(self, feedback):
        """
        Update the temporal field based on feedback from recursive loops.
        
        Args:
            feedback (np.ndarray): Feedback data to incorporate into the temporal states.
        """
        if self.current_time < self.time_steps:
            # Incorporate feedback into the current state
            feedback_adjusted = feedback[:self.state_dim] if len(feedback) >= self.state_dim else np.pad(feedback, (0, self.state_dim - len(feedback)))
            self.states[self.current_time] += 0.05 * feedback_adjusted
    
    def get_history(self):
        """
        Retrieve the full history of temporal states.
        
        Returns:
            np.ndarray: Array of all states over time.
        """
        return self.states[:self.current_time + 1]
    
    def reset(self):
        """
        Reset the temporal field to initial conditions.
        """
        self.states = np.zeros((self.time_steps, self.state_dim))
        self.current_time = 0
        self.states[0] = np.random.normal(0, 0.1, self.state_dim)
