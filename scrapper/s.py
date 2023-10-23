import spacy
# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Sample job description
job_description = """
We are looking for a Senior Software Engineer with experience in Python and web development. The ideal candidate should have experience in building and maintaining web applications using Django or Flask. Experience with database design, API integration, and front-end technologies is also required.
"""
# Process the job description
doc = nlp(job_description)

# Define relevant keywords for experience
experience_keywords = ["senior", "lead", "experienced", "expert", "manager", "director"]

# Extract experience-related sentences
experience_sentences = []
for sentence in doc.sents:
    for keyword in experience_keywords:
        if keyword in sentence.text.lower():
            experience_sentences.append(sentence.text)
            break

# Print extracted experience sentences
for sentence in experience_sentences:
    print(sentence)
