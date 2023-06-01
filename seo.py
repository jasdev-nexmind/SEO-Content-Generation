import os
import re
import time
import openai
from threading import Thread
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the API key
openai.api_key = openai_api_key
openai.Model.list()

def generate_chat_response(prompt, retries, max_retries):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are an AI designed to adeptly identify, generate, and implement search engine optimized long-tail keywords and align pertinent content, with the ultimate goal of enhancing your website's visibility, driving organic traffic, and improving your online business performance."},
                    {"role": "user", "content": prompt}
                ],
            temperature=0.8,
            # max_tokens=1000,
            # top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
        )
        return response.choices[0].message['content']
    
    except openai.error.RateLimitError as e:  # rate limit error
        print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
    except openai.error.Timeout as e:  # timeout error
        print("Request timed out. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
    except openai.error.APIError as e:
        if hasattr(e, 'response') and e.response.status_code == 429:  # rate limit error
            print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        elif hasattr(e, 'response') and e.response.status_code == 502:  # bad gateway error
            print("Bad Gateway. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        elif hasattr(e, 'response') and e.response.status_code == 600:  # read timeout error
            print("Read Timeout. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        else:
            raise e  # if it's not a rate limit error, re-raise the exception
    time.sleep(60)  # wait for 60 seconds before retrying
    return None  # return None if an exception was caught

def chat_with_gpt3(prompt):
    max_retries = 5
    for retries in range(max_retries):
        response = generate_chat_response(prompt, retries, max_retries)
        if response is not None:   # If a response was successfully received
            return response
    raise Exception(f"Max retries exceeded. The API continues to respond with an error after " + str(max_retries) + " attempts.")
        
def get_industry(topic):
    prompt = f"Considering these keywords '{topic}', what industry do they seem to be most related to?"
    industry = chat_with_gpt3(prompt)
    print("Industry Found")
    return industry

def get_target(topic):
    audienceList = []
    prompt = f"Given the keywords '{topic}', who are some potential target audiences that might be interested in a product or service related to these words?"
    audience = chat_with_gpt3(prompt)
    audiences = audience.split('\n')  # split the keywords into a list assuming they are comma-separated
    audiences = [target.replace('"', '') for target in audiences]
    audiences = [re.sub(r'^\d+\.\s*', '', target) for target in audiences]
    audienceList.extend(audiences)
    print("Target Audience Generated")
    return (audienceList)

def generate_keyword_clusters(topic):
    keyword_clusters = []
    prompt = f"Based on the topic '{topic}', please suggest 5 SEO-optimized long-tail keywords that could help enhance search engine visibility."
    keywords_str = chat_with_gpt3(prompt)
    keywords = keywords_str.split('\n')  # split the keywords into a list assuming they are comma-separated
    keywords = [keyword.replace('"', '') for keyword in keywords]
    keywords = [re.sub(r'^\d+\.\s*', '', keyword) for keyword in keywords]
    keyword_clusters.extend(keywords)
    print("Keywords Generated")
    return keyword_clusters

def generate_title(keyword_clusters):
    titles = []
    for keywords in keyword_clusters:
        prompt = f"Could you create a concise, engaging, and grammatically correct title for a company that relates to these keywords: '{keywords}'?"
        title = chat_with_gpt3(prompt)
        titles.append(title)
    titles = [title.replace('"', '') for title in titles]
    print("Titles Generated")
    return titles

def generate_content(name, topic, industry, audience, keyword, title):
    print("Generating Content...")
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    base_prompt = f"""
    Please create website content for a company with the following specifications:
    Company Name: {name}
    Industry: {industry}
    Target Audience: {audience}
    Title: {title}.
    Core Keywords: {topic}
    Long-Tail Keywords: {keyword}
    Requirements:
    1) Make sure the content length is 500 words.
    2) Add headers and subheaders where appropriate.
    3) The keywords should be incorporated into the headings, subheadings and spread evenly throughout the content. 
    4) The content should be engaging and unique.
    """
    # Old Template
    # Generate a wesbsite with 1500 words of content in HTML format for a company that provides services related to these {topic}
    # The keywords should be incorporated into the headings, subheadings, meta descriptions, and spread evenly throughout the website. The website should be engaging and unique.
    # Use styles such fonts, colors, and animations. Use the Bootstrap library (https://getbootstrap.com/docs/5.3/components) for HTML components and styling. Ensure the CSS styles are properly formatted and included in the <style> tag inside the HTML file.
    # Include placeholders for brands and logos if none is provided. Make sure to replace � with proper characters or punctuation

    # New Template
    # Company Name:
    # Industry:
    # Target Audience: Describe your target audience or interested customers so I can better focus on generating suitable content.
    # Core Keywords: Provide 5-10 core keywords closely related to your business and products/services that you want to be optimized.
    # Long-Tail Keywords: Provide any number of desired long-tail keywords or simply ask me to generate them for you based on the core keywords you've provided.
    # Content Preferences: Specify if there are certain content types or topics on which you would like the site to focus, such as blog articles, case studies, product descriptions, etc.
    # Additional Features: Indicate if there are any additional features that should be incorporated into the site (e.g., social media integration, e-commerce functionality, multimedia elements).
        
    content = chat_with_gpt3(base_prompt)
    content = generate_html(content)
    filename = sanitize_filename(title)  # use the first keyword as the filename
    with open(os.path.join(directory_path, f'{filename}.html'), 'w', encoding='utf-8') as f:
        f.write(content)
    print ("Finished file for " + title)

def generate_html(content):
    # Generate HTML code for the website
    print("Generating HTML code for the website...")
    prompt = f"""
    Generate a website in HTML format for a company using the following content. The generated HTML should be properly structured, starting with a <!DOCTYPE html> declaration, followed by a <html> element, meta description and then the <head> and <body> elements.:
    {content}
    Requirements:
    """
    website = chat_with_gpt3(prompt)
    website = add_styles_and_components(website)
    return website

def add_styles_and_components(website):
    # Add styles and components to the website
    print("Adding styles and components to the website...")
    prompt = f"""
    Add CSS styles, animation and HTML components in the HTML code to enhance its appearance and functionality.
    1) Use components from Tailwind libraries (https://tailwindcss.com/) or (https://tailwindui.com/?ref=top) for HTML styles and components. 
    2) Add a navigation bar and footer with proper alignment to the website
    3) Add animations such as on-hover animations
    4) Use scrolling animations from this website (https://michalsnik.github.io/aos/) or (https://www.sliderrevolution.com/resources/css-animations-on-scroll/)
    5) Look through the code and recheck the syntax and format of the HTML code, add any missing symbols and replace mistyped symbols.
    6) Make sure the alignments are proper.
    7) Make sure the website is responsive.
    8) Respond with the HTML code only.
    
    {website}
    
    """ 
    # Call the chat_with_gpt3 function to generate the styles and components
    updated_website = chat_with_gpt3(prompt)

    # Write the updated HTML content back to the file
    return updated_website

def sanitize_filename(filename):
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    return re.sub(r'[^A-Za-z0-9]+', '_', filename)

def main():
    name = input("Company Name: ")
    topic = input("Your Keywords: ")
    industry = get_industry(topic)
    print(industry)
    audience = get_target(topic)
    print(audience)
    keyword_clusters = generate_keyword_clusters(topic)
    print(keyword_clusters)
    titles = generate_title(keyword_clusters)
    print(titles)
    threads = []
    for keyword, title in zip(keyword_clusters, titles):
        t = Thread(target=generate_content, args=(name, topic, industry, audience, keyword, title))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()    

if __name__ == "__main__" :
    main()

