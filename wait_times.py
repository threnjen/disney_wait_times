#!/usr/bin/env python
# coding: utf-8

# # Get Soup

# In[52]:


from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd
from time import sleep


while True:
  # In[53]:


  page = requests.get("https://www.laughingplace.com/w/p/disneyland-current-wait-times/")
  dland = BeautifulSoup(page.content, 'html.parser')


  # In[54]:


  page2 = requests.get("https://www.laughingplace.com/w/p/disney-california-adventure-current-wait-times/")
  dca = BeautifulSoup(page2.content, 'html.parser')


  # ## Get Attractions Table

  # In[71]:


  waits = []


  # In[72]:


  check = dland.find('div', class_='header').text
  check


  # In[73]:


  check = check.split('\n')


  # In[74]:


  pattern = 'Operating Hours For '
  date_string = re.sub(pattern, '', check[0])
  date_string = date_string[5:11]
  date = re.sub('[^A-Za-z0-9]+', ' ', date_string).strip()
  


  # In[75]:


  pattern = 'Last Check at '
  mod_string = re.sub(pattern, '', check[2])
  mod_string = mod_string[:6]
  time = re.sub('[^A-Za-z0-9]+', '', mod_string).strip()
  


  # In[76]:


  hours_string = check[0][31:]
  hours_string=hours_string.strip()
  


  # In[77]:


  total_date=date+' '+hours_string+' Pull:'+time
  


  # # Disneyland

  # ## Wait Times

  # In[78]:


  first = dland.find('table', class_='lp_attraction')


  # In[79]:


  wait_times = first.find_all("span", id=re.compile("f"))


  # In[80]:


  for item in wait_times:
    
      if item.find('div', class_='waiticon'):
          raw_time = item.find('td')
          time = raw_time.text[:3].strip(' ')
          if ' ' in time:
              time = time[:1]
      else:
          time = item.text[:3].strip(' ')
          if ' ' in time:
              time = time[:1]
        
      waits.append(time)


  # # DCA

  # ## Wait Times

  # In[81]:


  first = dca.find('table', class_='lp_attraction')


  # In[82]:


  wait_times = first.find_all("span", id=re.compile("f"))
  wait_times


  # In[83]:


  for item in wait_times:
   
      if item.find('div', class_='waiticon'):
          raw_time = item.find('td')
          time = raw_time.text[:3].strip(' ')
          if ' ' in time:
              time = time[:1]
      else:
          time = item.text[:3].strip(' ')
          if ' ' in time:
              time = time[:1]
        
      waits.append(time)


  # ## DataFrame

  # In[84]:


  waits


  # In[85]:


  attraction_waits = pd.read_pickle('attraction_waits.pkl')
  attraction_waits


  # In[86]:


  attraction_waits[total_date] = waits
  attraction_waits


  # In[87]:


  attraction_waits.to_pickle('attraction_waits.pkl')


  # In[ ]:
  sleep(900)



