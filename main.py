'''
This file is part of SimMeR, an educational mechatronics robotics simulator.
Initial development funded by the University of Toronto MIE Department.
Copyright (C) 2023  Ian G. Bennett

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Imports
import time
import random
import pygame
from maze import Maze
from robot import Robot
from hud import Hud
import config as CONFIG
import control

### Initialization
print('SimMeR Loading...')

# Everything from here on needs work
'''
# Global Plotting Variables
global ray_plot
global rayend_plot
global ir_pts
global ir_pts_in
global ir_circle

## User-editable variables and flags

## Data Import
# Data Import

# Build Block
block = build_block(blocksize, block_center);

# Build Robot
bot_perim = import_bot;
bot_pos = pos_update(bot_center, bot_rot, bot_perim);
bot_front = [0.75*max(bot_perim(:,1)),0];

# Import Sensor Loadout and Positions
sensor = import_sensor;

# Import Drive information
drive = import_drive;

# Initialize integration-based sensor values
gyro_num = [];
odom_num = [];
for ct = 1:size(sensor.id)
    if strcmp('gyro', sensor.id{ct}(1:end-1))
        gyro_num = [gyro_num ct];
    end
    if strcmp('odom', sensor.id{ct}(1:end-1))
        odom_num = [odom_num ct];
    end
end

# Populate the gyroscope and odometer sensor variables
gyro = [gyro_num', sensor.err(gyro_num'), zeros(size(gyro_num))'];
odom = [odom_num', sensor.err(odom_num'), zeros(size(odom_num))'];


## Act on initialization flags
# Shuffle random number generator seed or set it statically
if randerror
    rng('shuffle') # Use shuffled pseudorandom error generation
else
    rng(0) # Use consistent pseudorandom error generation
end

# Randomize drive biases to verify algorithm robustness
if randbias
    drive = bias_randomize(drive, strength);
end

# Create the plot
if plot_robot
    fig = figure(1);
    axis equal
    hold on
    xlim(maze_dim(1:2))
    ylim(maze_dim(3:4))

    # Maze
    checker_plot = plot_checker(checker);
    maze_plot = plot_checker(maze(7:end,:), 'k', 1);
    plot(maze(:,1),maze(:,2), 'k', 'LineWidth', 2)
    xticks(0:12:96)
    yticks(0:12:48)

    # Block
    block_plot = patch(block(:,1),block(:,2), 'y');
    set(block_plot,'facealpha',.5)

end

## Initialize tcp server to read and respond to algorithm commands
clc  # Clear loading message
disp('Simulator initialized... waiting for connection from client')
[s_cmd, s_rply] = tcp_setup('server', 9000, 9001);
fopen(s_cmd);
# fopen(s_rply);

clc
disp('Client connected!')
'''

# Set random error seed
if ~CONFIG.rand_error:
    random.seed(CONFIG.error_seed)

# Load maze walls and floor pattern
MAZE = Maze()
MAZE.import_walls()
MAZE.generate_floor()
CANVAS_WIDTH = MAZE.size_x * CONFIG.ppi + CONFIG.border_pixels * 2
CANVAS_HEIGHT = MAZE.size_y * CONFIG.ppi + CONFIG.border_pixels * 2

# Load robot
ROBOT = Robot()

# Load the Heads Up Display
HUD = Hud()

# Initialize graphics
pygame.init()
canvas = pygame.display.set_mode([CANVAS_WIDTH, CANVAS_HEIGHT])

RUNNING = True
while RUNNING:

    # Check for and act on keyboard input
    game_events = pygame.event.get()
    RUNNING = control.check_input(game_events)
    keypress = pygame.key.get_pressed()

    # Recalculate the robot position
    ROBOT.define_perimeter()
    ROBOT.device_positions()

    # Fill the background with white
    canvas.fill((255, 255, 255))

    # Draw the maze checkerboard pattern
    MAZE.draw_floor(canvas)

    # Draw the maze walls
    MAZE.draw_walls(canvas)

    # Draw the robot onto the maze
    ROBOT.draw(canvas)
    ROBOT.draw_devices(canvas)

    # Update the various HUD elements
    HUD.draw_frame_indicator(canvas)
    HUD.draw_keys(canvas, keypress)

    # Flip the display (update the canvas)
    pygame.display.flip()

    # Slow framerate down for debug
    time.sleep(0.25)

# Done! Time to quit.
pygame.quit()