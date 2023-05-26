import os
import re
import time
import openai
import concurrent.futures
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the API key
openai.api_key = openai_api_key
openai.Model.list()


def chat_with_gpt3(prompt):
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                    {"role": "system", "content": "You are an AI designed to adeptly identify, generate, and implement search engine optimized long-tail keywords and align pertinent content, with the ultimate goal of enhancing your website's visibility, driving organic traffic, and improving your online business performance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )
            return response.choices[0].message['content']
        
        except openai.error.RateLimitError as e:  # rate limit error
            print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
            retries += 1
            time.sleep(60)  # wait for 60 seconds before retrying
        except openai.error.Timeout as e:  # timeout error
            print("Request timed out. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
            retries += 1
            time.sleep(60)
        except openai.error.APIError as e:
            if hasattr(e, 'response') and e.response.status_code == 429:  # rate limit error
                print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
                retries += 1
                time.sleep(60)  # wait for 60 seconds before retrying
            elif hasattr(e, 'response') and e.response.status_code == 502:  # rate limit error
                print("Bad Gateway. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
                retries += 1
                time.sleep(60)
            elif hasattr(e, 'response') and e.response.status_code == 600:  # rate limit error
                print("Read Timeout. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
                retries += 1
                time.sleep(60)
            else:
                raise e  # if it's not a rate limit error, re-raise the exception
    raise Exception(f"Max retries exceeded. The API continues to respond with an error after " + max_retries + " attempts.")

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
        prompt = f"Generate a short interesting and engaging title related to these keywords, make sure they are grammatically correct: {keywords}"
        title = chat_with_gpt3(prompt)
        titles.append(title)
    titles = [title.replace('"', '') for title in titles]
    return titles


def generate_content(keyword_clusters, titles, include_styles=False, include_faq=False):
    content = []   
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    for keyword, title in zip(keyword_clusters, titles):
        base_prompt = f"""
        Generate a 1500-word, SEO-optimized website in HTML format on the topic related to these title {title}. Use this keywords as well: {keyword}. The keywords should be incorporated into the headings, subheadings, meta descriptions, and spread evenly throughout the website. The website should be engaging and unique. Include placeholders for brands and logos. Make sure to replace � with proper characters or punctuation"""
        if include_styles:
            base_prompt += "The generated HTML should be properly structured, starting with a <!DOCTYPE html> declaration, followed by a <html> element, and then the <head> and <body> elements. Inside the <head> element, include a <style> tag that contains the CSS styles for the website. The styles should include fonts, colors, and animations. Use the Bootstrap library (https://getbootstrap.com/docs/5.3/components) and (https://getbootstrap.com/docs/5.3/components/navbar) for HTML components and styling. Ensure the CSS styles are properly formatted and included in the <style> tag inside the HTML file."
        
        if include_faq:
            base_prompt += "Include a FAQ section in the website."
        
        website = chat_with_gpt3(base_prompt)
        filename = sanitize_filename(title)  # use the first keyword as the filename
        with open(os.path.join(directory_path, f'{filename}.html'), 'w', encoding='utf-8') as f:
            f.write(website)
    return website

def sanitize_filename(filename):
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    sanitized_filename = re.sub('[^A-Za-z0-9 ]+', '', filename)  # remove special characters
    sanitized_filename = sanitized_filename.replace(' ', '_')  # replace spaces with underscores
    return sanitized_filename

def main():
    topic = input("Your Topic: ")
    include_styles = input("Include styles in the content? (yes/no): ").lower() == "yes"
    include_faq = input("Include a FAQ section in the content? (yes/no): ").lower() == "yes"
    keyword_clusters = generate_keyword_clusters(topic)
    print(keyword_clusters)
    titles = generate_title(keyword_clusters)
    print(titles)
    content = generate_content(keyword_clusters, titles, include_styles, include_faq)
    print("content generated and written to HTML files.")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Use the executor's map method to apply the generate_content function to each set of keywords and titles
        websites = list(executor.map(generate_content, keyword_clusters, titles))

if __name__ == "__main__" :
    main()
