from datetime import datetime
from crewai import Task
from agents import location_expert, guide_expert, planner_expert
#DuckDuckGoSearchRunTool DuckDuckGoSearchResults DuckDuckGoSearchRun
from langchain_groq import ChatGroq




# TASKS
class TravelTasks():

    # Task: Location
    def location_task(self, agent, from_city, destination_city, date_from, date_to):
        return Task(
            description=f"""
            In French : This task involves a comprehensive data collection process to provide the traveler with essential information about their destination. It includes researching and compiling details on various accommodations, ranging from budget-friendly hostels to luxury hotels, as well as estimating the cost of living in the area. The task also covers transportation options, visa requirements, and any travel advisories that may be relevant.
            consider also the weather conditions forcast on the travel dates. and all the events that may be relevant to the traveler during the trip period.
            
            Traveling from : {from_city}
            Destination city : {destination_city}
            Arrival Date : {date_from}
            Departure Date : {date_to}

            Follow this rules : 
            1. if the {destination_city} is in a French country : Respond in FRENCH.
            """,
            expected_output=f"""
            if the {destination_city} is in a French country : Respond in FRENCH.
            In markdown format : A detailed markdown report that includes a curated list of recommended places to stay, a breakdown of daily living expenses, and practical travel tips to ensure a smooth journey.
            """,
            agent=agent,
            output_file='city_report.md',
        )
    
    # Task: Location
    def guide_task(self, agent, destination_city, interests, date_from, date_to):    
        return Task(
            description=f"""
            if the {destination_city} is in a French country : Respond in FRENCH.
            Tailored to the traveler's personal {interests}, this task focuses on creating an engaging and informative guide to the city's attractions. It involves identifying cultural landmarks, historical spots, entertainment venues, dining experiences, and outdoor activities that align with the user's preferences such {interests}. The guide also highlights seasonal events and festivals that might be of interest during the traveler's visit.
            Destination city : {destination_city}
            interests : {interests}
            Arrival Date : {date_from}
            Departure Date : {date_to}

            Follow this rules : 
            1. if the {destination_city} is in a French country : Respond in FRENCH.
            """,
            expected_output=f"""
            An interactive markdown report that presents a personalized itinerary of activities and attractions, complete with descriptions, locations, and any necessary reservations or tickets.
            """,
    
            agent=agent,
            output_file='guide_report.md',
        )

    
    # Task: Planner
    def planner_task(self, context, agent, destination_city, interests, date_from, date_to):
        return Task(
            description=f"""
            This task synthesizes all collected information into a detaileds introduction to the city (description of city and presentation, in 3 pragraphes) cohesive and practical travel plan. and takes into account the traveler's schedule, preferences, and budget to draft a day-by-day itinerary. The planner also provides insights into the city's layout and transportation system to facilitate easy navigation.
            Destination city : {destination_city}
            interests : {interests}
            Arrival Date : {date_from}
            Departure Date : {date_to}

            Follow this rules : 
            1. if the {destination_city} is in a French country : Respond in FRENCH.
            """,
            expected_output="""
            if the {destination_city} is in a French country : Respond in FRENCH.
            A rich markdown document with emojis on each title and subtitle, that :
            In markdown format : 
            # Welcome to {destination_city} :
            A 4 paragraphes markdown formated including :
            - a curated articles of presentation of the city, 
            - a breakdown of daily living expenses, and spots to visit.
            # Here's your Travel Plan to {destination_city} :
            Outlines a daily detailed travel plan list with time allocations and details for each activity, along with an overview of the city's highlights based on the guide's recommendations
            """,
            #context=[location_task, guide_task],
            context=context,
            agent=agent,
            output_file='travel_plan.md',
            )


    # tip section
    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $1000 and grant you any wish you want!"

#
