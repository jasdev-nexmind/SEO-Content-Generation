import csv
import concurrent.futures
import io
import json
import os
import openai
import re
import random
import requests
import sys
import time
import torch
import io
from PIL import Image
from dotenv import load_dotenv
from threading import Thread
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, wait
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# Load .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1-base"
headers = {"Authorization": f"Bearer {os.getenv('STABILITY_KEY')}"}

# Use the API key
openai.api_key = openai_api_key
openai.Model.list()


#==================================================================================================
# API Interaction
#==================================================================================================
 

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


def stabilityai_generate(prompt: str,
                         size: str,
                         section: str) -> None:
    print("Generating " + section + " image...")
    image_bytes = query({
        "inputs": f"{prompt}",
        "width":1280,
        "height":800,
    })

    image = Image.open(io.BytesIO(image_bytes))
    print("Done")
    directory = "./content"  # Change this to your directory
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    image.save(os.path.join(directory, f'{section}.jpg'))
    return (f'{section}.jpg')
    

def generate_content_response(prompt: str,
                      temp: float,
                      p: float,
                      freq: float,
                      presence: float,
                      retries: int,
                      max_retries: int,
                      model: str) -> tuple:
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
                            retries: int,
                            max_retries: int) -> list:
    try:
        print("Generating image...")
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size,
        )
        # print (response)
        return response['data'][0]['url']

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
                     section: str) -> list:
    max_retries = 5
    for retries in range(max_retries):
        url: list = generate_image_response(prompt, size, retries, max_retries)
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


# ##==================================================================================================
# JSON Functions
# ##==================================================================================================

def deep_update(source, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict):
            # get node or create one
            node = source.setdefault(key, {})
            deep_update(node, value)
        else:
            source[key] = value
    return source

def correctjson(jsonfile: Dict):
    prompt = f"""
    Correct this json file:
    {jsonfile}
    """
    correctedjson = chat_with_gpt3("JSON Correction", prompt, temp=0.2, p=0.1)
    return correctedjson

def sanitize_filename(filename: str) -> str:
    """Remove special characters and replace spaces with underscores in a string to use as a filename."""
    return re.sub(r'[^A-Za-z0-9]+', '_', filename)


# def fail_safe(website: str) -> str:
#     if website.find('<!DOCTYPE html>') == -1:
#         website = htmlcode
#     return website


# ##===================================================================================================
# Content Generation Methods
# ##===================================================================================================


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


def generate_long_tail_keywords(topic: str) -> List[str]:
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
            "h2": "",
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
                       title: str) -> dict:
    description = generate_meta_description(company_name, topic, keyword)
    print (description)
    content = generate_content(company_name, topic, industry, keyword, title)
    contentjson = json.loads(content)
    updated_json = {"meta": {"title": title, "description": description}}
    updated_json.update(contentjson)
    print("Content Generated")
    # print(json.dumps(updated_json, indent=4))
    return updated_json


# =======================================================================================================================
# Image Generation
# =======================================================================================================================

def get_image_context(company_name: str,
                      keyword: str,
                      section: str,
                      topic: str,
                      industry: str) -> str:
    context_json = """
        {
            "context":"..."
            "size":"...(eg. 1024x1024)"
        }
    """
    prompt = f"""
    Please generate a description of an image for the {section} section about {keyword} and {topic}. 
    The company name is {company_name} and the scope of the image is  {industry}
    Format: {context_json}
    """
    image_context = chat_with_gpt3("Image Context Generation", prompt, temp=0.7, p=0.8)
    image_context.join("hi")
    print(image_context)
    startindex = image_context.find("{")
    endindex = image_context.rfind("}")
    if startindex == -1 or endindex == -1:
        return ("False")
    else:
        image_context = image_context[startindex:endindex+1]
    imagecontext = json.loads(image_context)
    
    imageurl = stabilityai_generate(imagecontext["context"], imagecontext["size"], section)
    return imageurl


def generate_gallery_images(company_name: str,
                            keyword: str,
                            topic: str, 
                            industry: str) -> List[str]:
    gallery = []
    for i in range(8):
        gallery.append(get_image_context(company_name, keyword, f"gallery {i}", topic, industry))

    print(gallery)
    return gallery
    
def image_generation(company_name: str,
                     topic: str,
                     industry: str,
                     keyword: str) -> Dict:
    print("Generating Images...")
    image_json = {
        "banner": 
            {
                "image": ""
            },
        "about": 
            {
                "image": ""
            },
        "gallery": 
            {"image": []
            }
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the threads and collect the futures for non-gallery sections
        for section in ["banner", "about"]:
            futures = {executor.submit(get_image_context, company_name, keyword, section, topic, industry): section}

        # Add the gallery futures
        image_json["gallery"]["image"] = (generate_gallery_images(company_name, keyword, topic, industry))

        for future in concurrent.futures.as_completed(futures):
            section = futures[future]
            try:
                image_url: list = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (section, exc))
            else:
                if image_url:
                    image_json[section]["image"] = image_url
    print("Images Generated")
    return image_json
    
    
#=======================================================================================================================
# Main Function
# =======================================================================================================================

def main():
    # Get the company name and topic from the user
    # pic = stabilityai_generate("An image of a beautiful bouquet of flowers arranged in a vase, with a tagline that says 'Affordable online flower shop in Malaysia'. The image showcases a variety of flowers in different colors and sizes, with a focus on the affordability of the shop's offerings.", "512x512")
    try:
        company_name = sys.argv[1]
        topic = sys.argv[2]
    except IndexError:
        company_name = input("Company Name: ")
        topic = input("Your Keywords: ")
        
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
    long_tail_keywords = generate_long_tail_keywords(topic)
    for number, keyword in enumerate(long_tail_keywords):
        print(f"{number+1}. {keyword}")

    # Generate title from keyword
    selected_keyword = long_tail_keywords[random.randint(0, 4)]
    print("Selected Keyword: " + selected_keyword)
    title = generate_title(company_name, selected_keyword)
    print(title)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_future = executor.submit(image_generation, company_name, topic, industry, selected_keyword)
        content_future = executor.submit(content_generation, company_name, topic, industry, selected_keyword, title)
        futures = [image_future, content_future]
        done, not_done = concurrent.futures.wait(futures, timeout=60, return_when=concurrent.futures.ALL_COMPLETED)
        try:
            image_result = image_future.result()
            content_result = content_future.result()
        except Exception as e:
            print("An exception occurred during execution: ", e)
        merged_dict = deep_update(content_result, image_result)

    directory_path = "content"
    os.makedirs(directory_path, exist_ok=True)
    with open(os.path.join(directory_path, f'data.json'), 'w', encoding='utf-8') as f:
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
#         
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


{
    "meta": {
        "title": "Experience Sustainable Luxury: Hertz's Eco-Friendly Lodges in the Heart of Malaysian Rainforest",
        "description": "Looking for the best hotel in Malaysia? Look no further than Hertz! Our eco-friendly lodges in the Malaysian rainforest offer a unique and sustainable travel experience. Book your stay now and enjoy the natural beauty of Malaysia while minimizing your environmental impact."
    },
    "banner": {
        "h1": "Experience Sustainable Luxury: Hertz's Eco-Friendly Lodges in the Heart of Malaysian Rainforest",
        "h2": "Discover the Best Hotel in Malaysia",
        "button": [
            "About Us",
            "Learn More"
        ]
    },
    "about": {
        "h2": "About Us",
        "p": "At Hertz, we believe in providing sustainable luxury experiences for our guests. Nestled in the heart of the Malaysian rainforest, our eco-friendly lodges offer a unique opportunity to connect with nature while enjoying the utmost comfort and convenience. With a commitment to environmental conservation and responsible tourism, we strive to create a harmonious balance between luxury and sustainability."
    },
    "blogs": {
        "h2": "Latest Articles",
        "post": [
            {
                "h3": "Exploring the Biodiversity of the Malaysian Rainforest",
                "p": "Embark on a journey through the lush greenery of the Malaysian rainforest and discover its incredible biodiversity. From rare flora and fauna to breathtaking waterfalls, our expert guides will take you on an unforgettable adventure, providing insights into the delicate ecosystem that surrounds our lodges."
            },
            {
                "h3": "The Benefits of Eco-Friendly Tourism",
                "p": "Learn about the positive impact of eco-friendly tourism and how it contributes to the preservation of natural resources. Discover how our lodges incorporate sustainable practices such as solar power, waste management, and local community engagement to minimize our environmental footprint."
            },
            {
                "h3": "Indulge in Luxury: The Amenities at Hertz's Eco-Friendly Lodges",
                "p": "Experience the ultimate in luxury at our eco-friendly lodges. From spacious rooms with panoramic rainforest views to gourmet dining options featuring locally sourced ingredients, our lodges offer an unparalleled level of comfort and relaxation. Unwind at our spa, take a dip in the infinity pool, or simply enjoy the tranquility of nature."
            }
        ]
    },
    "faq": {
        "h2": "Frequently Asked Questions",
        "question": [
            {
                "h3": "Are the lodges fully sustainable?",
                "p": "Yes, our lodges are designed with sustainability in mind. We utilize renewable energy sources such as solar power, implement efficient waste management systems, and prioritize the use of eco-friendly materials in our construction and operations."
            },
            {
                "h3": "What activities are available for guests?",
                "p": "There are plenty of activities to choose from during your stay at our lodges. Explore the rainforest on guided nature walks, embark on thrilling wildlife safaris, or simply relax and rejuvenate in the serene surroundings. Our knowledgeable staff can assist in planning personalized itineraries based on your interests."
            },
            {
                "h3": "How can I make a reservation?",
                "p": "Making a reservation is easy. Simply visit our website or contact our friendly customer service team. We recommend booking in advance to secure your preferred dates as our lodges are in high demand."
            }
        ]
    }
}

{
    "banner": {
        "image": "banner.jpg"},
    "about": {
        "image": "about.jpg"
        },
    "gallery": {
        "image": ["gallery0.jpg",
        "gallery1.jpg",
        "gallery2.jpg",
        "gallery3.jpg",
        "gallery4.jpg",
        "gallery5.jpg",
        "gallery6.jpg",
        "gallery7.jpg"  
        ]
    }
}
        