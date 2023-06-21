import csv
import os
import openai
import re
import sys
import time
import json
from threading import Thread
from typing import List, Dict
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
                      max_retries: int,
                      model: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=f"{model}",
            messages=[
                    {"role": "system", "content": "You are an web designer with the objective to identify search engine optimized long-tail keywords and generate contents, with the goal of generating website contents and enhance website's visibility, driving organic traffic, and improving online business performance."},
                    {"role": "user", "content": prompt}
                ],
            temperature=temp,
            # max_tokens=2500,
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
                   presence: float = 0,
                   model: str = "gpt-3.5-turbo-16k") -> str:
    max_retries = 5
    for retries in range(max_retries):
        response, prompt_tokens, completion_tokens, total_tokens = generate_response(prompt, temp, p, freq, presence, retries, max_retries, model)
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


##==================================================================================================
# HTML Template Methods
##==================================================================================================


def generate_html(company_name: str, filename: str, description: str, title: str) -> None:
    website = create_template(company_name, filename, description, title)
    directory_path = "test"
    os.makedirs(directory_path, exist_ok=True)
    start_index = website.find('<!DOCTYPE html>')
    end_index = website.find('</html>', start_index+1)
    if start_index == -1 and end_index == -1:
        pass
    new_website = website[start_index:end_index+7]      
    with open(os.path.join(directory_path, f'test.html'), 'w', encoding='utf-8') as f:
        f.write(new_website)


def create_template(company_name: str,
                    filename: str,
                    description: str,
                    title: str) -> str:
    print("Creating template...")
    website= f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Brands</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="{description}">
        <title>{title}</title>
        <!-- CSS stylesheets -->
        <link rel="stylesheet" href="{filename}.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
        <script src="https://cdn.lordicon.com/bhenfmcm.js"></script>
    </head>
    <body>
            <nav class="navbar navbar-expand-lg bg-body-tertiary">
                <div class="container-fluid shadow-2xl">
                    <a class="navbar-brand flex items-center" href="#">
                        <img src="https://via.placeholder.com/50x50" alt="Logo" class="d-inline-block align-text-top" />
                        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">{company_name}</span>
                    </a>
                <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <lord-icon
                        src="https://cdn.lordicon.com/dfjljsxr.json"
                        trigger="morph"
                        colors="outline:#121331,primary:#ffffff"
                        style="width:50px;height:50px">
                    </lord-icon>
                </button>
                <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                    <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">About Us</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contact Us</a>
                    </li>
                    </ul>
                </div>
                </div>
            </nav>
        </body>
    </html>	
    """    
    return website


def preprocess(contentjson: List[str]) -> List[str]:
    print("Preprocessing content...")
    for cont in contentjson["section"]:
        cont["content"] = tag_wrapper(cont["type"], cont["content"])
    print (contentjson)
        
        

def tag_wrapper(tag: str, cont: str) -> None:
    print("Wrapping content...")
    return(f"""<{tag}>{cont}</{tag}>""")
   

def insert_cont(website: str, content: str) -> str:
    print("Inserting content...")
    start_index = website.find('<body>')
    end_index = website.find('</body>', start_index+1)
    if start_index == -1 and end_index == -1:
        pass
    new_website = website[:start_index+6] + content + website[end_index:]
    return new_website


def compile_files(website: str,
                  content: str,
                  filename: str,
                  add_style: bool) -> str:
    print("Compiling files...")    
    end_index = website.find('</body>')
    if end_index == -1:
        new_website = website
    else:
        new_website = website[:end_index] + content + '\n' + website[end_index:]
    return new_website


def compile_css(website: str, filename: str) -> str:
    print("Compiling CSS...")
    start_index = website.find('</head>')
    a_style = f'<link rel="stylesheet" href="{filename}.css">'
    if start_index == -1:
        new_website = website
    else:
        new_website = website[:start_index] + a_style + '\n' + website[start_index:]
    return new_website
        

def sanitize_filename(filename: str) -> str:
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    return re.sub(r'[^A-Za-z0-9]+', '_', filename)

    
    
def fail_safe(website: str) -> str:
    if website.find('<!DOCTYPE html>') == -1:
        website = htmlcode
    return website


#===================================================================================================
## Content Generation Methods
#===================================================================================================


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


def generate_title(company_name: str, keyword: str) -> str:
    prompt = f"Suggest 1 catchy headline about '{keyword}' for the company {company_name}"
    title = chat_with_gpt3("Title Generation", prompt, temp=0.7, p=0.8)
    title = title.replace('"', '')
    print("Titles Generated")
    return title


def generate_outline(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str,
                     title: str,
                     index: int) -> None:
    prompt = f"""
    Please create a comprehensive content outline for a landing page dedicated to {company_name} that centers around the topic of '{title}' and the keyword '{keyword}'. Your outline should consist of no more than seven bullet points, each preceded by a dash ("-"). Please refrain from including any concluding statements in your outline.
    """
    outline = chat_with_gpt3("Outline Generation", prompt, temp=0.7, p=0.8)
    filename = f"Outline {index+1}"  # use the first keyword as the filename
    directorypath = "outline"
    os.makedirs(directorypath, exist_ok=True)
    with open(os.path.join(directorypath, f'{filename}.txt'), 'w') as f:
        f.write(outline)
        
        
def generate_meta_description(company_name: str,
                              topic: str,
                              keywords: str) -> str:
    print("Generating meta description...")
    prompt = f"""
    Generate a meta description for {company_name} based on this topic: '{topic}'.
    Use these keywords in the meta description: {keywords}
    """
    meta_description = chat_with_gpt3("Meta Description Generation", prompt, temp=0.7, p=0.8)
    return meta_description


def generate_content(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str,
                     title: str,
                     outline: str) -> str:
    
    print("Generating Content...")
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    json1 = """{
        "section": {
            {
                "type": "title",
                "content": "...."
            },
            {
                "type": "h1",
                "content": "...."
            },
            {
                "type": "h2",
                "content": "...."
            },
            {
                "type": "p",
                "content": "...."
            }
        }
    }
    """
    prompt = f"""
    Create website content for a company with the following specifications:
    Company Name: {company_name}
    Title: {title}
    Industry: {industry}
    Core Keywords: {topic}
    Keywords: {keyword}
    Outline: {outline}
    Format: {json1}
    Requirements:
    1) Make sure the content length is 700 words.
    2) The content should be engaging and unique.
    3) Include headers and subheaders.
    4) Don't include any conclusion
    """
    content = chat_with_gpt3("Content Generation", prompt, temp=0.7, p=0.8, model="gpt-3.5-turbo-16k")
    return content


def main():
    # Get the company name and topic from the user
    keychoice = True
    outchoice = True
    try:
        company_name = sys.argv[1]
        topic = sys.argv[2]
    except IndexError:
        company_name = input("Company Name: ")
        topic = input("Your Keywords: ")
        keychoice = False
        outchoice = False
        
    # Open token.csv to track token usage
    file_exists = os.path.isfile('token_usage.csv')  # Check if file already exists
    with open('token_usage.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Keyword', 'Iteration', 'Stage', 'Prompt Tokens', 'Completion Tokens', 'Total Tokens', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Company Name': company_name, 'Keyword': topic, 'Iteration': 0, 'Stage': 'Initial', 'Prompt Tokens': 0, 'Completion Tokens': 0, 'Total Tokens': 0, 'Price': 0})
        
    # Generate industry 
    industry = get_industry(topic)
    print(industry)
    
    # Generate target audience
    audience = get_target(topic)
    for number, aud in enumerate(audience):
        print(f"{number+1}. {aud}")
    
    # Generate SEO keywords
    keyword_clusters = generate_keyword_clusters(topic)
    for number, keyword in enumerate(keyword_clusters):
        print(f"{number+1}. {keyword}")
            
    # Generate title from keyword
    if keychoice:
        keyword_choice = int(sys.argv[3])
    else:
        keyword_choice = int(input("Choose a keyword: "))

    selected_keyword = keyword_clusters[keyword_choice-1]
    titles = generate_title(company_name, selected_keyword)
    print(titles)
    
    # Generate an 5 outlines
    threads = []
    for i in range(5):
        t = Thread(target=generate_outline, args=(company_name, topic, industry, selected_keyword, titles, i))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
    print("Outlines generated")
    
    # Generate meta description and template
    if outchoice:
        outline_choice = int(sys.argv[4])
    else:
        outline_choice = int(input("Choose an outline: "))

    filename = f"Outline {outline_choice}"
    directory_path = "outline"
    # outlines = []
    with open(os.path.join(directory_path, f'{filename}.txt'), 'r', encoding='utf-8-sig') as f:
        outline = f.read()
    description = generate_meta_description(company_name, topic, keyword)
    print (description)
    website = create_template(company_name, filename, description, titles)
    content = generate_content(company_name, topic, industry, selected_keyword, titles, outline)
    contentjson = json.loads(content)
    contentcode = preprocess(contentjson)
    
    # Comvert content into HTML
    global htmlcode
    htmlcode = contentcode
    # htmlcode = convert_to_html(content)

    
    # Write into file
    # directory_path = "content"
    # os.makedirs(directory_path, exist_ok=True)
    # start_index = website.find('<!DOCTYPE html>')
    # end_index = website.find('</html>', start_index+1)
    # if start_index == -1 and end_index == -1:
    #     new_website = htmlcode
    # else:
    #     new_website = htmlcode[start_index:end_index+7]      
    # with open(os.path.join(directory_path, f'{sanitize_filename(titles)}.html'), 'w', encoding='utf-8') as f:
    #     f.write(new_website)
        
    # print(f"Finish file for {titles}")
    
    # End procedures
    with open('token_usage.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Keyword', 'Iteration', 'Stage', 'Prompt Tokens', 'Completion Tokens', 'Total Tokens', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Stage': 'Complete', 'Prompt Tokens': 0, 'Completion Tokens': 0, 'Total Tokens': 0, 'Price': 0})


if __name__ == "__main__":
    main()


