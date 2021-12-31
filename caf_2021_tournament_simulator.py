import pandas as pd
import numpy as np
import random
import match_prediction_module as match_predicition

caf_teams_adress = 'caf_2022_teams.csv'

caf_teams = pd.read_csv(caf_teams_adress)


i_total = 1

def get_after_round_points(group, i1, i2, i3, i4):
    pts = [0, 0, 0, 0]
    
    global i_total
    
    match[i_total] = Match(list(group)[i1], list(group)[i2])
    i_total = i_total + 1
    match[i_total] = Match(list(group)[i3], list(group)[i4])
    i_total = i_total + 1
    
    match[i_total-2].run()
    match[i_total-1].run()
    
    if match[i_total-2].tie == True:
        pts[i1] = pts[i1] + 1
        pts[i2] = pts[i2] + 1
    elif match[i_total-2].winner == list(group)[i1]:
        pts[i1] = pts[i1] + 3
    elif match[i_total-2].unlucky == list(group)[i1]:
        pts[i2] = pts[i2] + 3
        
        
    if match[i_total-1].tie == True:
        pts[i3] = pts[i3] + 1
        pts[i4] = pts[i4] + 1
    elif match[i_total-1].winner == list(group)[i1]:
        pts[i3] = pts[i3] + 3
    elif match[i_total-1].unlucky == list(group)[i1]:
        pts[i4] = pts[i4] + 3
        
    
    return pts


def get_group_winners(group):
   teams = group.columns.values
   points = group.values[0]
   df = pd.DataFrame()
   df['team'] = teams
   df['points'] = points
   
   df = df.sort_values('points')
   
   first = df.iloc[3]['team']
   second = df.iloc[2]['team']
   third = df.iloc[1]['team']
   third_points = int(df.iloc[1]['points'])

   return first, second, third, third_points



def run_group_stage(teams):
    firsts = []
    seconds = []
    thirds = pd.DataFrame(columns=['team', 'points', 'group'])
    
    groups =  [None] * int(teams.shape[0]/4)
    for i in range(int(teams.shape[0]/4)):
        start = i*4
        end = (i+1)*4
        groups[i] = pd.DataFrame(data=[], columns=teams[start:end])
        
        groups[i].loc[0] = get_after_round_points(groups[i], 0, 1, 2, 3)
        groups[i].loc[0] = groups[i].loc[0] + get_after_round_points(groups[i], 0, 2, 1, 3)
        groups[i].loc[0] = groups[i].loc[0] + get_after_round_points(groups[i], 0, 3, 1, 2)
        
        first, second, third, third_points = get_group_winners(groups[i])
        
        firsts.append(first)
        seconds.append(second)
        
        thirds.loc[thirds.shape[0]]= (third, third_points, i)
        
        print(groups[i])
        
    thirds = thirds.sort_values('points')    
    thirds = thirds.iloc[::-1]
    thirds = thirds.iloc[:4]
    thirds = thirds.sort_values('group')
    thirds_teams = thirds['team'].values
    thirds_groups = thirds['group'].values
    thirds_shape = ''
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F']
    for t in thirds_groups:
        thirds_shape = thirds_shape + alphabet[t]
        
    return firsts, seconds, thirds_teams, thirds_shape

class Match:
    def __init__(self, host, away):
        self.host = host
        self.away = away
        self.winner = 'none'
        self.unlucky = 'none'
        self.tie = False
        self.host_score = 0
        self.away_score = 0
        
    def run(self):
        m = match_predicition.inference(self.host, self.away)
        mm = match_predicition.inference(self.away, self.host)
        
       # m = (m+mm) / 2
        tm = ((m[0]+mm[1])/2, (m[1]+mm[0])/2)
        m = tm
        
        self.host_score = round(m[0])
        self.away_score = round(m[1])
        if m[0] > m[1]:
            self.winner = self.host
            self.unlucky = self.away
        elif m[0] < m[1]:
            self.winner = self.away
            self.unlucky = self.host
        else:
            self.tie = True
            if random.randint(0,1) == 0:
                self.winner = self.host
                self.unlucky = self.away
            else:
                self.winner = self.away
                self.unlucky = self.host


def run_16():
    match[37] = Match(seconds[0], seconds[2])
    match[44] = Match(firsts[5], seconds[4])
    match[40] = Match(seconds[1], seconds[5])
    match[43] = Match(firsts[4], seconds[3])
    if thirds_groups == 'ABCD':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[3])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[1])
    elif thirds_groups == 'ABCE':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[1])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ABCF':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[1])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ABDE':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[1])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ABDF':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[1])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ABEF':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[1])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ACDE':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[2])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ACDF':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[2])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'ACEF':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[3])
        match[38] = Match(firsts[3], thirds[2])
    elif thirds_groups == 'ADEF':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[0])
        match[42] = Match(firsts[2], thirds[3])
        match[38] = Match(firsts[3], thirds[2])
    elif thirds_groups == 'BCDE':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[2])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'BCDF':
        match[39] = Match(firsts[0], thirds[1])
        match[41] = Match(firsts[1], thirds[2])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'BCEF':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[1])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'BDEF':
        match[39] = Match(firsts[0], thirds[2])
        match[41] = Match(firsts[1], thirds[1])
        match[42] = Match(firsts[2], thirds[0])
        match[38] = Match(firsts[3], thirds[3])
    elif thirds_groups == 'CDEF':
        match[39] = Match(firsts[0], thirds[0])
        match[41] = Match(firsts[1], thirds[1])
        match[42] = Match(firsts[2], thirds[3])
        match[38] = Match(firsts[3], thirds[2])
        
    for i in range(37, 45):
        match[i].run()

        
        
def run_knock_out():
    ## Round of 16
    run_16()
    
        
    ## Round of 8
    match[45] = Match(match[37].winner, match[38].winner)
    match[46] = Match(match[40].winner, match[39].winner)
    match[47] = Match(match[43].winner, match[42].winner)
    match[48] = Match(match[41].winner, match[44].winner)
    for i in range(45, 49):
        match[i].run()
        
        
    ## Semi-final
    match[49] = Match(match[45].winner, match[48].winner)
    match[50] = Match(match[46].winner, match[47].winner)
    for i in range(49, 51):
        match[i].run()
        
    ## Third-place
    match[51] = Match(match[49].unlucky, match[50].unlucky)
    ## Final
    match[52] = Match(match[49].winner, match[50].winner)
    for i in range(51, 53):
        match[i].run()

match = [None] * 53
firsts, seconds, thirds, thirds_groups = run_group_stage( caf_teams['team'].values )

run_knock_out()
print(match[52].winner)
print(match[52].unlucky)
print(match[51].winner)
print(match[51].unlucky)



for i in range(1, 53):
        print(match[i].host+' '+str(match[i].host_score)+' '+' - '+match[i].away+' '+str(match[i].away_score)+' '+' = '+match[i].winner)

        
        