from scrapper_functions import *
import html2text





desc_d = """You hold a university degree in accounting,  finance or a quantitative field (e.g. mathematics, engineering, or information technology).
You demonstrate a keen understanding of the Finance functional processes.
Experience in SAP Finance environment is preferred.
Experience or knowledge of Agile and DevOps would be an added plus.
You have worked for 4-8 yrs and in the following areas: requirement gathering and analysis, documentation of functional specifications, Unit and Integration testing of IT solutions, master data management, financial accounting and reporting.
You know how to handle large amounts of data in MS Excel and present your findings in simple and visually appealing way.
You communicate clearly, speak and write eloquently in English; you can explain just about anything to anybody.
You are a problem solver and demonstrate a strong client centric attitude, embracing product ownership.
You anticipate future issues, drive progress despite uncertainty and handle conflicts effectively.
You are a self-starter who 50 - 60 years old company can handle multiple priorities, work independently and deliver high-quality products under pressure
You work hands-on, embracing virtual teams and partnering with  1-2 yrs people from different backgrounds and cultures."""
title = "VP – Regulatory Reporting, GSCs"
digits = find_experience(desc_d,title)
print(digits)