This project predicts SLA Breaches and match tickets to the right employee skills
--
## Project Overview
This project explores how Machine Learning (ML) and Natural Language Processing (NLP) can be used to improve IT service management by making support ticket handling more efficient and helping teams identify opportunities to improve employee performance.

I developed this project as part of my learning journey into the practical applications of Artificial Intelligence (AI) and Machine Learning in IT and cybersecurity. My goal is to understand how these technologies can be applied to real-world problems, from improving operational efficiency to supporting data-driven decision-making. Developed for educational purposes, this project demonstrates the potential of machine learning to transform IT service management by turning operational data and written feedback into meaningful insights that support better decision-making, timely service delivery, and continuous performance improvement.

## Problem
I was reading an ITWeb App article that talks about how employees in some companies are complaining about their IT Support departments not responding to their tickets on time, and that leads to some of them resorting to shadow AI to resolve those problems they stated on their tickets on their own. This is one of the articles: [ Technology friction in the workplace costs institutions up to R30 million per thousand staff, a new report finds.  https://www.itweb.co.za/article/employees-are-giving-up-on-it-departments/RgeVDqPRmpR7KJN3 ]. So I asked myself that if I was one of the employees, what is it that I would do as part of a solution to this problem.

## Solution
So I developed two  machine learning models:
* Model 1: A logistic regression model that predicts a risk probability of a ticket experiencing an SLA breach. It aims to help IT support teams manage and resolve support tickets within their respective Service Level Agreement (SLA) deadlines. By considering each ticket’s priority and required resolution time, the solution can help teams identify tickets that may be at risk of missing their deadlines, allowing them to prioritize their work and respond more effectively.

* Model 2: The second model uses Natural Language Processing (NLP) techniques to analyze written feedback and performance reviews provided by supervisors or senior team members. By identifying recurring patterns and areas of concern in the feedback, the solution aims to generate practical recommendations that can help employees understand where improvement is needed and how their performance could be enhanced. These recommendations are intended to support human decision-making rather than replace managerial judgment.

## How to run the files
You can install the files alongside the datasets used to train them and run them on your prefered coding environment, but I highly recommend running script.ipynb in Jupyter Notebook or google collab, whilst the python files can be ran in Visual Studio Code or just the terminal

NB: The dataset used to train model one is in a zipped file cos of its big size, whilst the other ones used to run model 2 can be found in csv format in this repo. Also note that Script.ipynb is Model 1, whereas model 2 is feedback_model.py

## Conclusion

This project demonstrates the potential of Artificial Intelligence (AI), Machine Learning (ML), and Natural Language Processing (NLP) to address practical challenges in IT service management. By exploring ways to improve support ticket resolution within Service Level Agreement (SLA) deadlines and analyze employee performance feedback, the project highlights how data can be transformed into meaningful insights that support more efficient operations and continuous improvement.

Although developed for educational purposes, this project represents an important step in my journey toward understanding how machine learning can be applied to real-world IT and cybersecurity challenges. It has allowed me to explore how intelligent systems can support decision-making, identify potential problems, and provide actionable recommendations. Ultimately, this project reinforces my interest in developing data-driven solutions that go beyond theoretical concepts to address practical problems, improve operational efficiency, and contribute to smarter, more effective IT environments.
