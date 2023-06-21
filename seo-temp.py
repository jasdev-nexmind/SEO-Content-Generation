import csv
import os
import openai
import re
import random
import sys
import time
import json
import concurrent.futures
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


def generate_content_response(prompt: str,
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
    except openai.error.ServiceUnavailableError:
        print("Server Overloaded. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
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


def generate_image_response(prompt: str,
                    size: str,
                    n: int,
                    retries: int,
                    max_retries: int) -> str:
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size,
        )
        # print (response)
        if n == 1:
            image_url = response['data'][0]['url']
            return image_url
        else:
            gallery = [response['data'][i]['url'] for i in range(n)]
            return gallery
            
    except openai.error.RateLimitError as e:  # rate limit error
        print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
    except openai.error.Timeout as e:  # timeout error
        print("Request timed out. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
    except openai.error.ServiceUnavailableError:
        print("Server Overloaded. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
    except openai.error.APIError as e:
        if hasattr(e, 'response') and e.response.status_code == 429:  # rate limit error
            print("Rate limit reached. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        elif hasattr(e, 'response') and e.response.status_code == 502:  # bad gateway error
            print("Bad Gateway. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        elif hasattr(e, 'response') and e.response.status_code == 600:  # read timeout error
            print("Read Timeout. Retry attempt " + str(retries + 1) + " of " + str(max_retries) + "...")
        else:
            raise e  # if it's not a rate limit error, re-raise the exception
    time.sleep(60)
    


def chat_with_gpt3(stage: str,
                   prompt: str,
                   temp: float = 0.5,
                   p: float = 0.5,
                   freq: float = 0,
                   presence: float = 0,
                   model: str = "gpt-3.5-turbo") -> str:
    max_retries = 5
    for retries in range(max_retries):
        response, prompt_tokens, completion_tokens, total_tokens = generate_content_response(prompt, temp, p, freq, presence, retries, max_retries, model)
        if response is not None:   # If a response was successfully received
            write_to_csv((stage, prompt_tokens, completion_tokens, total_tokens))
            return response
    raise Exception(f"Max retries exceeded. The API continues to respond with an error after " + str(max_retries) + " attempts.")


def chat_with_dall_e(prompt: str,
                     size: str,
                     n: int) -> str:
    max_retries = 5
    for retries in range(max_retries):
        url = generate_image_response(prompt, size, n, retries, max_retries)
        if url is not None:   # If a response was successfully received
            return url
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
# JSON Functions
##==================================================================================================

def deep_update(source, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict):
            # get node or create one
            node = source.setdefault(key, {})
            deep_update(node, value)
        else:
            source[key] = value
    return source

def sanitize_filename(filename: str) -> str:
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    return re.sub(r'[^A-Za-z0-9]+', '_', filename)
    
    
# def fail_safe(website: str) -> str:
#     if website.find('<!DOCTYPE html>') == -1:
#         website = htmlcode
#     return website


#===================================================================================================
## Content Generation Methods
#===================================================================================================


def get_industry(topic) -> str:
    prompt = f"Generate an industry for these keywords, no explanation is needed: {topic}"
    industry = chat_with_gpt3("Industry Identification", prompt, temp=0.2, p=0.1)
    print("Industry Found")
    return industry


def get_audience(topic: str) -> List[str]:
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


def generate_title(company_name: str,
                   keyword: str) -> str:
    prompt = f"Suggest 1 catchy headline about '{keyword}' for the company {company_name}"
    title = chat_with_gpt3("Title Generation", prompt, temp=0.7, p=0.8)
    title = title.replace('"', '')
    print("Titles Generated")
    return title


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


# def generate_outline(company_name: str,
#                      topic: str,
#                      industry: str,
#                      keyword: str,
#                      title: str,
#                      index: int) -> None:
#     prompt = f"""
#     Please create a comprehensive content outline for a landing page dedicated to {company_name} that centers around the topic of '{title}' and the keyword '{keyword}'. Your outline should consist of no more than seven bullet points, each preceded by a dash ("-"). Please refrain from including any concluding statements in your outline.
#     """
#     outline = chat_with_gpt3("Outline Generation", prompt, temp=0.7, p=0.8)
#     filename = f"Outline {index+1}"  # use the first keyword as the filename
#     directorypath = "outline"
#     os.makedirs(directorypath, exist_ok=True)
#     with open(os.path.join(directorypath, f'{filename}.txt'), 'w') as f:
#         f.write(outline)     
        

def generate_content(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str,
                     title: str) -> str:
    
    print("Generating Content...")
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    json1 = """
    {
        "banner": {
                "h1": "...",
                "h2": "...",
                "button": [
                    "About Us",
                    "Learn More"
                ]
        },
        "about": {
                "h2": "About Us",
                "p": "..."
        },
        "blogs":{
            "h2": "Customer Review",
            "post": [{
                    "h3": "...",
                    "p": "...",
                },
                {
                    "h3": "...",
                    "p": "...",
                },
                {
                    "h3": "...",
                    "p": "...",
                }
            ]
        },
        "faq":{
            "h2": "Frequently Asked Questions",
            "question": [{
                    "h3": "...",
                    "p": "...",
                },
                {
                    "h3": "...",
                    "p": "...",
                },
                {
                    "h3": "...",
                    "p": "...",
                },...
            ]
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
    Format: {json1}
    Requirements:
    1) Make sure the content length is 700 words.
    2) The content should be engaging and unique.
    3) Include headers and subheaders.
    4) Don't include any conclusion
    """
    content = chat_with_gpt3("Content Generation", prompt, temp=0.7, p=0.8, model="gpt-3.5-turbo-16k")
    return content

def content_generation(company_name: str,
                       topic: str,
                       industry: str,
                       keyword: str,
                       title: str) -> None:
    description = generate_meta_description(company_name, topic, keyword)
    print (description)
    content = generate_content(company_name, topic, industry, keyword, title)
    contentjson = json.loads(content)
    updated_json = {"meta":{"title":title,"description":description}}
    updated_json.update(contentjson)
    return (updated_json)
            

#=======================================================================================================================
# Image Generation
#=======================================================================================================================

def get_image_context(company_name: str,
                      keyword: str,
                      section: str) -> str:
    context_json = """
        {
            "context":"..."
            "size":"...(256x256/512x512/1024x1024)"
        }
    """
    prompt = f"""
    Please help {company_name} generate an image context for the {section} section about this keyword: {keyword}
    Format: {context_json}
    """
    image_context = chat_with_gpt3("Image Context Generation", prompt, temp=0.7, p=0.8)
    imagecontext = json.loads(image_context)
    print(imagecontext)
    if section != "gallery":
        imageurl = chat_with_dall_e(imagecontext["context"], imagecontext["size"], 1)
    else:
        imageurl = chat_with_dall_e(imagecontext["context"], imagecontext["size"], 8)
    return imageurl


def image_generation(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str,
                     title: str) -> Dict:
    print("Generating Images...")
    image_json = {
        "banner":{
            "image":"..."
        },
        "about":{
            "image":"..."
        },
        "gallery":{
            "image":[]
        }
    }
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the threads and collect the futures
        futures = {executor.submit(get_image_context, company_name, keyword, i): i for i in image_json.keys()}
        
        for future in concurrent.futures.as_completed(futures):
            section = futures[future]
            try:
                image_url = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (section, exc))
            else:
                if section != "gallery":
                    image_json[section]["image"] = image_url
                else:
                    image_json[section]["image"].extend(image_url)

    return(image_json)
    
    
#=======================================================================================================================
# Main Function
#=======================================================================================================================

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
    
    
    # Generate SEO keywords
    keyword_clusters = generate_keyword_clusters(topic)
    for number, keyword in enumerate(keyword_clusters):
        print(f"{number+1}. {keyword}")
            
    # Generate title from keyword
    selected_keyword = keyword_clusters[random.randint(0, 4)]
    print("Selected Keyword: " + selected_keyword)
    title = generate_title(company_name, selected_keyword)
    print(title)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_future = executor.submit(image_generation, company_name, topic, industry, selected_keyword, title)
        content_future = executor.submit(content_generation, company_name, topic, industry, selected_keyword, title)

        try:
            image_result = image_future.result()
            content_result = content_future.result()
        except Exception as e:
            print("An exception occurred during execution: ", e)
    
    merged_dict = deep_update(content_result, image_result)
    
    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True) 
    with open(os.path.join(directory_path, f'{sanitize_filename(company_name)}.json'), 'w', encoding='utf-8') as f:
        json.dump(merged_dict, f, ensure_ascii=False, indent=4)
    
    # End procedures
    with open('token_usage.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Keyword', 'Iteration', 'Stage', 'Prompt Tokens', 'Completion Tokens', 'Total Tokens', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Stage': 'Complete', 'Prompt Tokens': 0, 'Completion Tokens': 0, 'Total Tokens': 0, 'Price': 0})


if __name__ == "__main__":
    main()







# {
#     "meta": {
#         "title": "...",
#         "description": "..."
#     },
#     "logo": "...",
#     "banner": {
#             "image": "...",
#             "h1": "...",
#             "h2": "...",
#             "button": [
#                 "About Us",
#                 "Learn More"
#             ]
#     },
#     "about": {
#             "image": "...",
#             "h2": "About Us",
#             "p": "..."
#     },
#     "blogs":{
#         "h2": "Customer Review",
#         "post": [{
#                 "h3": "...",
#                 "p": "...",
#             },
#             {
#                 "h3": "...",
#                 "p": "...",
#             },
#             {
#                 "h3": "...",
#                 "p": "...",
#             }
#         ]
#     },
#     "gallery":{
#         "image": []
#     },
#     "faq":{
#         "h2": "Frequently Asked Questions",
#         "question": [{
#                 "h3": "...",
#                 "p": "...",
#             },
#             {
#                 "h3": "...",
#                 "p": "...",
#             },
#             {
#                 "h3": "...",
#                 "p": "...",
#             },...
#         ]
#     },
# }



# {
#     "meta": {
#         "title": "Get on the Road to Financial Freedom with Time - Your Trusted Car Dealership in Malaysia",
#         "description": "Looking for a specialized car dealership in Malaysia for electric vehicles? Look no further than Time. Our dealership offers a wide range of electric vehicles to suit your needs. Visit us today to learn more!"
#     },
#     "banner": {
#         "h1": "Get on the Road to Financial Freedom with Time",
#         "h2": "Your Trusted Car Dealership in Malaysia",
#         "button": [
#             "About Us",
#             "Learn More"
#         ]
#     },
#     "about": {
#         "h2": "About Us",
#         "p": "Welcome to Time, your trusted car dealership in Malaysia. We specialize in providing expert financing options to help you achieve financial freedom while purchasing your dream car. With our extensive knowledge and experience in the automotive industry, we are committed to offering the best solutions tailored to your needs."
#     },
#     "blogs": {
#         "h2": "Why Choose Time for Financing Options?",
#         "post": [
#             {
#                 "h3": "Expert Car Dealership in Malaysia for Financing Options",
#                 "p": "At Time, we pride ourselves on being the expert car dealership in Malaysia when it comes to financing options. Our team of professionals understands the complexities of purchasing a car and the importance of making informed financial decisions. We are here to guide you through the process, ensuring that you make the right choices to achieve your financial goals."
#             },
#             {
#                 "h3": "The Importance of Time in Making Financial Decisions",
#                 "p": "Time plays a crucial role when it comes to making financial decisions, especially when purchasing a car. Making the right choices at the right time can significantly impact your financial well-being. With Time by your side, you can trust us to provide timely advice and assistance, helping you make informed decisions that align with your financial goals."
#             },
#             {
#                 "h3": "How Time's Financing Options Can Help You Achieve Financial Freedom",
#                 "p": "At Time, we offer a range of financing options that are designed to help you achieve financial freedom. Our flexible payment plans and competitive interest rates ensure that you can afford your dream car without compromising your financial stability. With our guidance, you can take control of your finances and drive towards a brighter future."
#             }
#         ]
#     },
#     "testimonials": {
#         "h2": "Testimonials",
#         "testimonial": [
#             {
#                 "h3": "John Doe",
#                 "p": "Thanks to Time's financing options, I was able to purchase my dream car without any hassle. Their team provided excellent support and guided me throughout the process. I am now on the road to financial freedom, all thanks to Time."
#             },
#             {
#                 "h3": "Jane Smith",
#                 "p": "I highly recommend Time to anyone looking for a car dealership that offers financing options. They truly understand the importance of time in making financial decisions. With their help, I was able to make the right choices and achieve my financial goals."
#             }
#         ]
#     },
#     "benefits": {
#         "h2": "Additional Benefits of Purchasing from Time",
#         "p": "When you choose to purchase a car from Time, you not only gain access to expert financing options but also enjoy additional benefits. We provide warranty coverage for your peace of mind, ensuring that you are protected against any unforeseen circumstances. Our after-sales services are top-notch, offering you continued support even after you drive off our dealership. With Time, you can experience a hassle-free car buying experience from start to finish."
#     },
#     "cta": {
#         "h2": "Visit Time's Dealership Today",
#         "p": "Ready to take the first step towards financial freedom? Visit Time's dealership today and explore our wide range of cars and financing options. Our team of experts is here to assist you and help you make the best choices for your financial well-being. Don't wait any longer, start your journey towards financial freedom with Time."
#     }
# }