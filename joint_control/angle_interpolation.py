'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes.hello import hello
from keyframes.leftBackToStand import leftBackToStand
import numpy as np

class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.offset = 0
        self.animation_not_running = True
        

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        self.target_joints['RHipYawPitch'] = self.target_joints['LHipYawPitch']
        return super(AngleInterpolationAgent, self).think(perception)
    
    def calculate_offset(self,perception):#added to calculate offset
        self.offset = perception.time

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        names, times, keys = keyframes
        
        if len(names) == 0:
            return target_joints
        
            
        if(self.animation_not_running):
            self.calculate_offset(perception)
            self.animation_not_running = False
        
            
        
        n = len(names)
        max_time = 0
        for i in range(n):
            xp = times[i]
            if max_time < np.amax(xp): # calculate time of last keyframe
                max_time = np.amax(xp)
                
            fp = []
            
            for j in range(len(xp)):
                fp.append(keys[i][j][0])
            
            target_joints[names[i]] = np.interp(perception.time-self.offset,xp,fp)
            
        if perception.time-self.offset > max_time: # check if last keyframe is done
            self.animation_not_running = True
            self.keyframes = ([], [], [])# deletes keyframes after animation is done
            
        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = leftBackToStand()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
