import streamlit as st
import pandas as pd
import numpy as np
import random
import math


def switch_strat(init_door: int, win_door: int)->int:
    """Switch strategy 

    Args:
        init_door (int): initial door selected
        win_door (int): prize door

    Returns:
        int: 0 or 1 to indicate win-loose
        """
    if init_door != win_door:
        return 1
    else: 
        return 0

def stay_strat(init_door: int, win_door: int)->int:
    """Stay strategy

    Args:
        init_door (int): intial door selected
        win_door (int): prize door

    Returns:
        int: 0 or 1 to indicate win/loose
    """    
    if init_door == win_door:
        return 1
    else: 
        return 0 

my_df = pd.DataFrame(columns=["Selected","Prize", "Stay", "Switch"])
random.seed(42)

for i in range(5):
    select_door = random.randint(1,3)
    prize_door = random.randint(1,3)
    my_df.loc[len(my_df)]=[select_door, prize_door, stay_strat(select_door, prize_door), switch_strat(select_door,prize_door)] 


st.title("The Monty Hall Problem")

st.markdown("On the game show, a prize was hidden behind one of three doors. Contestants had to select a door.")
st.markdown("But, then there was a twist - after the contestent picked a door, the host then opened one of the remaining doors.")
st.markdown("The host asked the contestant if they'd like to switch doors.")

st.subheader("So that is the question. Switch or stay?")

st.markdown("In the simulation below, we simulate the switch and stay strategys.")
st.markdown("If there is a *1* in the Stay column, that strategy won.")
st.markdown("If there is a *1* in the Switch column, that strategy won.")

st.write(my_df)

if 'stay_mean' not in st.session_state:
    st.session_state.stay_mean = 0
if 'switch_mean' not in st.session_state:
    st.session_state.switch_mean = 0
if 'the_data' not in st.session_state:
   st.session_state.the_data=my_df
 


def update_means():
    st.session_state.stay_mean = st.session_state.the_data['Stay'].mean()
    st.session_state.switch_mean = st.session_state.the_data['Switch'].mean()


def average_list():
    mystay = []
    myswitch=[]
    the_data = st.session_state.the_data
    for i in range(len(the_data)):
        mystay.insert(i,the_data["Stay"][0:i+1].mean())
        myswitch.insert(i, the_data["Switch"][0:i+1].mean())
    my_results =pd.DataFrame()
    my_results["Stay"]=mystay
    my_results["Switch"]=myswitch
    return my_results


number = st.number_input("Enter a number of trials, to see which strategy is better.")
number = math.floor(number)

increment = st.button('Update')
if increment:
    the_data = st.session_state.the_data
    for i in range(int(number)):
        select_door = random.randint(1,3)
        prize_door = random.randint(1,3)
        the_data.loc[len(the_data)]=[select_door, prize_door, stay_strat(select_door, prize_door), switch_strat(select_door,prize_door)]
    st.session_state.the_data = the_data
    update_means()
    st.write('Stay percentage wins = ', st.session_state.stay_mean)    
    st.write('Switch percentage wins =', st.session_state.switch_mean)
    st.write(len(st.session_state.the_data))

results = average_list()
st.line_chart(results)

