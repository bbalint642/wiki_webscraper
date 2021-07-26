#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Importing libs


# In[12]:


##Task: #1 Get info box for Toy Story 3


# In[13]:


from bs4 import BeautifulSoup as bs
import requests


# In[14]:


r = requests.get("https://en.wikipedia.org/wiki/Toy_Story_3")

# Convert to a beautifulsoup object
soup = bs(r.content)

# Print out the HTML
contents = soup.prettify()
print(contents)


# In[15]:


info_box = soup.find(class_="infobox vevent")
info_rows = info_box.find_all("tr")
for row in info_box:
    print(row.prettify())


# In[16]:


def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip = True).replace("\xa0", " ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ", strip = True).replace("\xa0", " ")

movie_info = {}

for index, row in enumerate(info_rows):
    if index == 0:
        movie_info['title'] = row.find("th").get_text(" ", strip = True)
    elif index == 1:
        continue
    else:
        content_key = row.find("th").get_text(" ", strip = True)
        content_value = get_content_value(row.find("td"))
        movie_info[content_key] = content_value
    

movie_info


# In[18]:





# In[19]:


##Task: #2 Get info box for all disney movies


# In[31]:


r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")

# Convert to a beautiful soup object
soup = bs(r.content)

# Print out the HTML
contents = soup.prettify()
print(contents)


# In[32]:


movies = soup.select(".wikitable.sortable i")
movies[0:10]


# In[33]:


def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip = True).replace("\xa0", " ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ", strip = True).replace("\xa0", " ")

def get_info_box(url):
    
    r = requests.get(url )
    # Convert to a beautifulsoup object
    soup = bs(r.content)
    info_box = soup.find(class_="infobox vevent")
    info_rows = info_box.find_all("tr")

    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip = True)
        elif index == 1:
            continue
        else:
            content_key = row.find("th").get_text(" ", strip = True)
            content_value = get_content_value(row.find("td"))
            movie_info[content_key] = content_value
    
    return movie_info


# In[46]:


r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
soup = bs(r.content)
movies = soup.select(".wikitable.sortable i a")

base_path = "https://en.wikipedia.org/"

movie_info_list = []
for index, movie in enumerate(movies):

    try:
        relative_path = movie['href']
        full_path = base_path + relative_path
        title = movie['title']
        
        movie_info_list.append(get_info_box(full_path))
    except Exception as e:
        print(movie.get_text())
        print(e)

    


# In[47]:


len(movie_info_list)


# In[48]:


import json

def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# In[49]:


import json

def load_data(title):
    with open(title, encoding="utf-8") as f:
        return json.load(f)


# In[51]:


save_data("disney_data.json", movie_info_list)

