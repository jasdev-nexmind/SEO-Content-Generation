import os
import re
import time
import openai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the API key
openai.api_key = openai_api_key
openai.Model.list()


def chat_with_gpt3(prompt):
    while True:
        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are an AI designed to adeptly identify, generate, and implement search engine optimized long-tail keywords and align pertinent content, with the ultimate goal of enhancing your website's visibility, driving organic traffic, and improving your online business performance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                frequency_penalty=0.3,
                presence_penalty=0.2
            )
            return response.choices[0].message['content']
        except openai.error.APIError as e:
            if hasattr(e, 'response') and e.response.status_code == 429:  # rate limit error
                print("Rate limit reached. Waiting for 60 seconds before retrying...")
                time.sleep(60)  # wait for 60 seconds before retrying
            elif hasattr(e, 'response') and e.response.status_code == 502:  # rate limit error
                print("Bad Gateway. Waiting for 60 seconds before retrying...")
                time.sleep(60)
            else:
                raise e  # if it's not a rate limit error, re-raise the exception


def generate_keyword_clusters(topic):
    keyword_clusters = []
    prompt = f"Generate 5 SEO-optimized long-tail keywords related to the topic: {topic}."
    keywords_str = chat_with_gpt3(prompt)
    keywords = keywords_str.split('\n')  # split the keywords into a list assuming they are comma-separated
    keywords = [keyword.replace('"', '') for keyword in keywords]
    keywords = [re.sub(r'^\d+\.\s*', '', keyword) for keyword in keywords]
    keyword_clusters.extend(keywords)
    return keyword_clusters

def generate_title(keyword_clusters):
    titles = []
    for keywords in keyword_clusters:
        prompt = f""" Generate one interesting and engaging title for this keywords: {keywords}"""
        title = chat_with_gpt3(prompt)
        titles.append(title)
    return titles


def generate_articles(titles):
    articles = []
    for keywords in titles:
        prompt = f"""
        Generate a 1500-word, SEO-optimized article in HTML format on the topic related to these keywords: {keywords}. 
        The article should be engaging, unique, and include headings, META descriptions, subheadings, and a FAQ section. 
        The SEO keywords should be incorporated into the headings, subheadings, META descriptions, and spread evenly throughout the article. Ensure the HTML file has a proper formatting
        """
        article = chat_with_gpt3(prompt)
        articles.append(article)
        filename = sanitize_filename(keywords)  # use the first keyword as the filename
        with open(f'{filename}.html', 'w') as f:
            f.write(article)
    return articles


def sanitize_filename(filename):
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    sanitized_filename = re.sub('[^A-Za-z0-9 ]+', '', filename)  # remove special characters
    sanitized_filename = sanitized_filename.replace(' ', '_')  # replace spaces with underscores
    return sanitized_filename


if __name__ == "__main__" :
    topic = input("Your Topic: ")
    keyword_clusters = generate_keyword_clusters(topic)
    print(keyword_clusters)
    titles = generate_title(keyword_clusters)
    print(titles)
    articles = generate_articles(titles)
    print("Articles generated and written to HTML files.")