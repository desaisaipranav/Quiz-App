import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain ,create_extraction_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import plotly.graph_objects as go
import numpy as np
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(model_name='gpt-4', temperature=0.0)
memory = ConversationBufferMemory()


# def respond_to_query(query):
#     llm_agent = ConversationChain(
#         llm=llm,
#         memory=memory,
#     )
#     return llm_agent.run(query)
def sort_objects(obj_list):

    question = []
    options = []
    correct = []

    for obj in obj_list:

        if 'question' in obj :
            question.append(obj['question'])
        for i in range(3):
            list=[]
            if 'option1' in obj :
                list.append(obj['option1'])
            if 'option2' in obj :
                list.append(obj['option2'])
            if 'option3' in obj :
                list.append(obj['option3'])
        options.append(list)
        if 'correct answer' in obj :
            correct.append(obj['correct answer'])

    return [question,options,correct]

def create_ques_ans( topic):
    
    template =f"""Prepare 5 multiple choice questions on {{topic}}
    covering all levels of blooms taxonomy. try to make the questions on true definitons and on numerical or application also  somewhat complicated
    generate a python list which contains 4 sublists . In each python sublist ,
    first element should be the question. Second , third and fourth elements should be the only 3 options , 
    and fifth element should be the complete correct option to the question exactly as in options .avoid unnecesary text connotations
    , extra whitespaces and also avoid newlines anywhere , terminate the lists and strings correctly"""
    prompt = PromptTemplate.from_template(template)
    gpt4_model = ChatOpenAI(model="gpt-4")
    quizzer = LLMChain(prompt = prompt, llm = gpt4_model)
    a=quizzer.run(topic=topic)


    llm = ChatOpenAI(model = "gpt-4")
    schema = {
    "properties" : {
        "question" : {"type" : "string"},
        "option1" : {"type" : "string"},
        "option2" : {"type" : "string"},
        "option3" : {"type" : "string"},
        "correct answer" : {"type" : "string"}
    },
    "required" : ["question", "options","correct_answer"]
    }
    chain = create_extraction_chain(schema, llm)
    response = chain.run(a)
     
    return sort_objects(response) 
def report(list,score,total):
    x = np.linspace(0, total, 100)
    y = np.linspace(0, total, 100)
    x, y = np.meshgrid(x, y)

    # Define the 3D Gaussian function to generate z values
    def gaussian_3d(x, y, amplitude, xo, yo, sigma_x, sigma_y):
        g = amplitude * np.exp(-((x - xo) ** 2 / (2 * sigma_x ** 2) + (y - yo) ** 2 / (2 * sigma_y ** 2)))
        return g

    # Calculate the center position of the Gaussian peak at x=y=total questions
    center_x = total
    center_y = total
    sigma_x =0.4
    sigma_y=0.4
    # Generate z values using the Gaussian function
    z = 100 * gaussian_3d(x, y, amplitude=1, xo=center_x, yo=center_y, sigma_x=sigma_x * total, sigma_y=sigma_y * total)

    # Create a 3D surface plot
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    # Set plot layout
    fig.update_layout(
        title='Learning Status Graph',
        scene=dict(
            xaxis_title='Number of Correct Answers',
            yaxis_title='Number of Correct Answers',
            zaxis_title='Learning status curve',
        ),
    )
    # Add a point to the plot
    fig.add_trace(go.Scatter3d(x=[score], y=[score], z=[100 * gaussian_3d(score, score, amplitude=1, xo=center_x, yo=center_y, sigma_x=sigma_x * total, sigma_y=sigma_y * total)],
                               mode='markers', marker=dict(size=15, color='red', opacity=0.6), showlegend=False))
    fig.add_trace(go.Scatter3d(x=[score], y=[score], z=[100 * gaussian_3d(score, score, amplitude=1, xo=center_x, yo=center_y, sigma_x=sigma_x * total, sigma_y=sigma_y * total)],
                               mode='text', marker=dict(size=15, color='red', opacity=0.6),
                               text='Your performance', showlegend=False))
    # Show the plot
    st.plotly_chart(fig)
   
    template =f"""U are provided with a list of questions {{question}} and list of coreesponding answers{list[1]} marked .
    Just give 2 lines on how much understanding I have on the concept generally. """
    prompt = PromptTemplate.from_template(template)
    gpt4_model = ChatOpenAI(model="gpt-4",temperature=0.8)
    quizzer = LLMChain(prompt = prompt, llm = gpt4_model)
    a=quizzer.run(question=list[0])
    return a

    return 
