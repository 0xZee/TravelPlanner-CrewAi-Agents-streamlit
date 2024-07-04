
import streamlit as st
import sys
from datetime import datetime, timedelta
from crewai import Crew, Process
from TravelAgents import TravelAgents, StreamToExpander
from TravelTasks import TravelTasks


st.set_page_config(page_icon="✈️", page_title="ZeeTravelPlanner", layout="wide")

# class TravelCrew
class TravelCrew:

  def __init__(self, from_city, destination_city, interests, date_from, date_to):
      self.destination_city = destination_city
      self.from_city = from_city
      self.interests = interests
      self.date_from = date_from
      self.date_to = date_to
      self.output_placeholder = st.empty()
  
  def run(self):
      agents = TravelAgents()
      tasks = TravelTasks()
  
      location_expert = agents.location_expert()
      guide_expert = agents.guide_expert()
      planner_expert = agents.planner_expert()

      location_task = tasks.location_task(
          location_expert,
          self.from_city,
          self.destination_city,
          self.date_from,
          self.date_to
        )

      guide_task = tasks.guide_task(
          guide_expert,
          self.destination_city,
          self.interests,
          self.date_from,
          self.date_to
        )

      planner_task = tasks.planner_task(
          [location_task, guide_task],
          planner_expert,
          self.destination_city,
          self.interests,
          self.date_from,
          self.date_to,
        )
  
      crew = Crew(
        agents=[location_expert, guide_expert, planner_expert],
        tasks=[location_task, guide_task, planner_task],
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        #llm=llm_groq,
        #manager_llm=llm,
        #max_iter=24,
        verbose=True
        )
  
      result = crew.kickoff()
      self.output_placeholder.markdown(result)
  
      return result


##
##
##
##

st.header("✈️ 🎫 Travel Planner :orange[Ai]gent 🏝️ 🗺️", divider="orange")

# sidebar
with st.sidebar:
  st.caption("Travel Planner Agent")
  st.markdown(
    """
    # 🏝️ Travel Planner 🗺️
        1. Pick your dream destination
        2. give us your interests
        3. Set your travel dates
        4. Bon voyage !!
    """
  )
  st.divider()
  st.caption("Created by @0xZee")

st.session_state.plan_pressed = False
# User Inputs
today = datetime.now()
one_year_from_now = today + timedelta(days=365)
seven_days_from_now = today + timedelta(days=7)

st.caption("🗺️ Let's plan your Travel")


# User Details container
C = st.container(border=True)
X1, X2 = C.columns(2)
from_city = X1.text_input("📍 From :", placeholder="Paris, France")
destination_city = X2.text_input("🏝️ Your Destination :", placeholder="London, UK")

interests = C.text_input("🍹🛍️ Your interests :",  placeholder="Cultural, hotspots, Food, Shopping..")

Y1, Y2 = C.columns(2)

date_from = Y1.date_input(
  "📅 Vacation Start ✈️",
  today,
  format="DD/MM/YYYY",
)
date_to = Y2.date_input(
  "📅 Vacation End 🧳",
  seven_days_from_now,
  format="DD/MM/YYYY",
)
travel_period = (date_to - date_from).days
# out container
#LOGIC to CORRECT HERE
# out container
if from_city and destination_city and date_from and date_to and interests:
  st.caption("👌 Let's recap you Travel Plan :")
  st.write(f":sparkles: Your 🎫 :blue[{travel_period}-Days] Voyage from 📍 :blue[{from_city}] is starting the ✈️ {date_from} to 🧳 {date_to}. 🗺️ Your are heading to 🏝️ :orange[{destination_city}], to Enjoy 🍹 :orange[{interests}] 📸.")
  if plan := st.button("💫 Sounds Good ! 🗺️ Generate The Travel Plan", use_container_width=True, key="plan"):
    with st.spinner(text="🤖 Agents working for the best Travel Plan 🔍 ..."):
      # RUN
      with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=200, border=False):
            sys.stdout = StreamToExpander(st)
            travel_crew = TravelCrew(from_city, destination_city, interests, date_from, date_to)
            result = travel_crew.run()
        status.update(label="✅ Trip Plan Ready!",
                      state="complete", expanded=False)

      st.subheader("🗺️ Here is your Trip Plan 🎫 🏝️", anchor=False, divider="rainbow")
      st.markdown(result["final_output"])
      st.divider()
      # Display each key-value pair in 'usage_metrics'
      st.json(result['usage_metrics'])
      st.divider()
      # expander for each 'exported_output'
      for i, task in enumerate(result['tasks_outputs']):
          with st.expander(f"Agent Report {i+1} :", expanded=False):
              st.markdown(task)
      st.divider()

  








