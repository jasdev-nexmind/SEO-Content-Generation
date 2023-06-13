import os
import re
import time
import openai
import csv
from threading import Thread
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the API key
openai.api_key = openai_api_key
openai.Model.list()


def generate_response(prompt: str,
                      temp: float, 
                      p: float,
                      freq: float,
                      presence: float,
                      retries: int,
                      max_retries: int):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are an AI designed to adeptly identify, generate, and implement search engine optimized long-tail keywords and align pertinent content, with the ultimate goal of enhancing your website's visibility, driving organic traffic, and improving your online business performance."},
                    {"role": "user", "content": prompt}
                ],
            temperature=temp,
            # max_tokens=1000,
            top_p=p,
            frequency_penalty=freq,
            presence_penalty=presence,
        )
        # print (response)
        return response.choices[0].message['content'], response['usage']['prompt_tokens'], response['usage']['completion_tokens'], response['usage']['total_tokens']
    
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
    return None, None, None, None  # return None if an exception was caught


def chat_with_gpt3(stage: str,
                   prompt: str,
                   temp: float = 0.5,
                   p: float = 0.5,
                   freq: float = 0,
                   presence: float = 0) -> str:
    max_retries = 5
    for retries in range(max_retries):
        response, prompt_tokens, completion_tokens, total_tokens = generate_response(prompt, temp, p, freq, presence, retries, max_retries)
        if response is not None:   # If a response was successfully received
            write_to_csv((stage, prompt_tokens, completion_tokens, total_tokens))
            return response
    raise Exception(f"Max retries exceeded. The API continues to respond with an error after " + str(max_retries) + " attempts.")


def write_to_csv(data: tuple):
    file_exists = os.path.isfile('token_usage.csv')  # Check if file already exists
    with open('token_usage.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Keyword', 'Iteration', 'Stage', 'Prompt Tokens', 'Completion Tokens', 'Total Tokens', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # If file doesn't exist, write the header
        with open('token_usage.csv', 'r') as f:
            last_row = None
            for last_row in csv.DictReader(f):
                pass  # The loop will leave 'last_row' as the last row
            iteration = int(last_row['Iteration']) + 1 if last_row else 1  # If there is a last row, increment its 'Iteration' value by 1. Otherwise, start at 1
        price = 0.000002 * data[3]  # Calculate the price of the request
        writer.writerow({'Iteration': iteration, 'Stage': data[0], 'Prompt Tokens': data[1], 'Completion Tokens': data[2], 'Total Tokens': data[3], 'Price': float(price)})


def get_industry(topic) -> str:
    prompt = f"Generate an industry for these keywords, no explanation is needed: {topic}"
    industry = chat_with_gpt3("Industry Identification", prompt, temp=0.2, p=0.1)
    print("Industry Found")
    return industry


def get_target(topic: str) -> List[str]:
    audienceList = []
    prompt = f"Generate a list of target audience for these keywords, no explanation is needed: {topic}"
    audience = chat_with_gpt3("Target Search", prompt, temp=0.2, p=0.1)
    audiences = audience.split('\n')  # split the keywords into a list assuming they are comma-separated
    audiences = [target.replace('"', '') for target in audiences]
    audiences = [re.sub(r'^\d+\.\s*', '', target) for target in audiences]
    audienceList.extend(audiences)
    print("Target Audience Generated")
    return audienceList


def generate_keyword_clusters(topic: str) -> List[str]:
    keyword_clusters = []
    prompt = f"Generate 5 SEO-optimized long-tail keywords related to the topic: {topic}."
    keywords_str = chat_with_gpt3("Keyword Clusters Search", prompt, temp=0.2, p=0.1)
    keywords = keywords_str.split('\n')  # split the keywords into a list assuming they are comma-separated
    keywords = [keyword.replace('"', '') for keyword in keywords]
    keywords = [re.sub(r'^\d+\.\s*', '', keyword) for keyword in keywords]
    keyword_clusters.extend(keywords)
    print("Keywords Generated")
    return keyword_clusters


def generate_title(keyword_clusters: List[str]) -> List[str]:
    titles = []
    for keywords in keyword_clusters:
        prompt = f"Suggest a catchy headline for '{keywords}'"
        title = chat_with_gpt3("Title Generation", prompt, temp=0.7, p=0.8)
        titles.append(title)
    titles = [title.replace('"', '') for title in titles]
    print("Titles Generated")
    return titles


def generate_outline(company_name: str,
                     topic: str,
                     industry: str,
                     audience: List[str],
                     keyword: str,
                     title: str) -> None:
    prompt = f"""
    Generate a content outline for a home web page for {company_name} based on this topic, don't include conclusion: '{title}'
    Use this website as reference: https://milanote.com/templates/website-design/website-content
    """
    outline = chat_with_gpt3("Outline Generation", prompt, temp=0.7, p=0.8)
    print("Outlines Generated")
    filename = sanitize_filename(title)  # use the first keyword as the filename
    directorypath = "outline"
    os.makedirs(directorypath, exist_ok=True)
    with open(os.path.join(directorypath, f'{filename}.txt'), 'w') as f:
        f.write(outline)
    generate_content(company_name, topic, industry, keyword, title, True, True, outline)


def generate_content(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str,
                     title: str,
                     html_output: bool,
                     add_style: bool,
                     outline: str) -> None:
    
    print("Generating Content...")
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    prompt = f"""
    Create a content for a website using this outline: {outline}, include the company name:{company_name}, the title:{title}, the core keywords:{topic}, the long-tail keywords {keyword}, headers and subheaders.
    """
    # Template 1
    # Generate a website with 1500 words of content in HTML format for a company that provides services related to these {topic}
    # The keywords should be incorporated into the headings, subheadings, meta descriptions, and spread evenly throughout the website. The website should be engaging and unique.
    # Use styles such fonts, colors, and animations. Use the Bootstrap library (https://getbootstrap.com/docs/5.3/components) for HTML components and styling. Ensure the CSS styles are properly formatted and included in the <style> tag inside the HTML file.
    # Include placeholders for brands and logos if none is provided. Make sure to replace � with proper characters or punctuation

    # Template 2
    # Company Name:
    # Industry:
    # Target Audience: Describe your target audience or interested customers so I can better focus on generating suitable content.
    # Core Keywords: Provide 5-10 core keywords closely related to your business and products/services that you want to be optimized.
    # Long-Tail Keywords: Provide any number of desired long-tail keywords or simply ask me to generate them for you based on the core keywords you've provided.
    # Content Preferences: Specify if there are certain content types or topics on which you would like the site to focus, such as blog articles, case studies, product descriptions, etc.
    # Additional Features: Indicate if there are any additional features that should be incorporated into the site (e.g., social media integration, e-commerce functionality, multimedia elements).

    # Template 3
    # Please create website advertisement for a company with the following specifications:
    # Company Name: {company_name}
    # Industry: {industry}
    # Title: {title}.
    # Core Keywords: {topic}
    # Long-Tail Keywords: {keyword}
    # Requirements:
    # 1) Make sure the content length is 500 words.
    # 2) Include headers and subheaders
    # 3) The keywords should be incorporated into the headings, subheadings and spread evenly throughout the content. 
    # 4) The content should be engaging and unique.
    # 5) Content should be SEO optimized.
    # 6) Conclusion is not needed
    
    content = chat_with_gpt3("Content Generation", prompt, temp=0.7, p=0.8)
    filename = sanitize_filename(title)  # use the first keyword as the filename
    if html_output:
        content = generate_html(content)
        if add_style:
            content = add_styles_and_components(content, filename)
    with open(os.path.join(directory_path, f'{filename}.html'), 'w', encoding='utf-8') as f:
        f.write(content)
    print("Finished file for " + title)


def generate_html(content: str) -> str:
    # Generate HTML codes for the website
    print("Generating HTML code for the website...")
    prompt = f"""
    Generate a website in HTML format for a company using the following content. The generated HTML should be properly structured, starting with a <!DOCTYPE html> declaration, followed by a <html> element, meta description and then the <head> and <body> elements:
    {content}
    """
    website = chat_with_gpt3("HTML Conversion", prompt, temp=0.2, p=0.1)
    return website


def add_styles_and_components(website: str, filename: str) -> str:
    # Add styles and components to the website 
    # Call the chat_with_gpt3 function to generate the styles and components
    website = add_components(website)
    website = add_footer(website)
    add_styles(filename)
    website = compile_files(website, filename)
    
    # Write the updated HTML content back to the file
    print("Finished adding styles and components to the website")
    return website


def add_components(website: str) -> str:
    print("Adding components...")
    prompt = f""" 
    Add components to the website with proper alignment. Use components from Tailwind libraries (https://tailwindcss.com/) or (https://tailwindui.com/?ref=top):
    {website}
    """
    website = chat_with_gpt3("Adding Components", prompt, temp=0.2, p=0.1)
    return website


def add_footer(website: str) -> str:
    print("Adding footer...")
    prompt = f""" 
    Add a footer to this HTML file with proper alignment:
    {website}
    """
    website = chat_with_gpt3("Adding footer", prompt, temp=0.2, p=0.1)
    return website


def add_styles(filename: str) -> None:
    print("Adding styles...")
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    styles_file = change_font()
    styles_file = add_animation(styles_file)
    with open(os.path.join(directory_path, f'{filename}.css'), 'w') as f:
        f.write(styles_file)
    print("Finished adding styles ")


def change_font() -> str:
    print("Changing font...")
    prompt = f""" 
    Add a unique font family, color and background color CSS style for a website to make it stand out from other websites. Use the Google Fonts library (https://fonts.google.com/) to find a suitable font for this
    """
    styles_file = chat_with_gpt3("Changing font", prompt, temp=0.2, p=0.1)
    return styles_file


def add_animation(styles_file: str) -> str:
    print("Adding animation...")
    prompt = f""" 
    Add animations for each tag to the CSS file. Use animations from these styles_files (https://michalsnik.github.io/aos/) and (https://animate.style/):
    {styles_file}
    """
    styles_file = chat_with_gpt3("Adding animation", prompt, temp=0.2, p=0.1)
    return styles_file


def compile_files(website: str, styles_file: str) -> str:
    print("Compiling files...")
    prompt = f""" 
    Add a reference to the styles file "{styles_file}.css" in the HTML file:
    {website}
    """
    website = chat_with_gpt3("Compiling files", prompt, temp=0.2, p=0.1)
    return website


def sanitize_filename(filename: str) -> str:
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    return re.sub(r'[^A-Za-z0-9]+', '_', filename)


def main():
    company_name = input("Company Name: ")
    topic = input("Your Keywords: ")
    file_exists = os.path.isfile('token_usage.csv')  # Check if file already exists
    with open('token_usage.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Keyword', 'Iteration', 'Stage', 'Prompt Tokens', 'Completion Tokens', 'Total Tokens', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Company Name': company_name, 'Keyword': topic, 'Iteration': 0, 'Stage': 'Initial', 'Prompt Tokens': 0, 'Completion Tokens': 0, 'Total Tokens': 0, 'Price': 0})
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
        t = Thread(target=generate_outline, args=(company_name, topic, industry, audience, keyword, title))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()    


if __name__ == "__main__":
    main()
