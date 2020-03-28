#!/usr/bin/env python
# coding: utf-8

# # Hacker News Analysis
# 
# This is a project to disect and draw conclusions from Hacker News.

# In[1]:


import csv

f = open('hacker_news.csv')
hn = list(csv.reader(f))
print(hn[:5])


# ### Step 1: Remove Column Headers

# In[2]:


headers = hn[0]
hn = hn[1:]
print(headers)
print(hn[:5])


# ### Step 2: Extract `Ask HN` and `Show HN` Titles

# In[3]:


ask_posts = []
show_posts = []
other_posts = []

for post in hn:
    title = post[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(post)
    elif title.lower().startswith("show hn"):
            show_posts.append(post)
    else:
        other_posts.append(post)
        
print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))


# ### Step 3: Finding AVG Comments for `Ask HN` vs `Show HN`

# In[4]:


total_ask_comments = 0

for post in ask_posts:
    total_ask_comments += int(post[4])

avg_ask_comments = total_ask_comments / len(ask_posts)
print(avg_ask_comments)


# In[5]:


total_show_comments = 0
for post in show_posts:
    total_show_comments += int(post[4])

avg_show_comments = total_show_comments / len(show_posts)
print(avg_show_comments)


# Both `ask hn` and `show hn` receive a good number of comments, but `ask hn` receives significantly more on average.

# ### Step 4: Calculating AVG Comments Per Hour for `Ask HN`

# In[9]:


import datetime as dt

result_list = []

for post in ask_posts:
    result_list.append([post[6], int(post[4])])

counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for row in result_list:
    date = row[0]
    comment = row[1]
    time =dt.datetime.strptime(date, date_format).strftime("%H")
    if time not in counts_by_hour:
        comments_by_hour[time] = comment
        counts_by_hour[time] = 1
    else:
        comments_by_hour[time] += comment
        counts_by_hour[time] += 1
        
print(comments_by_hour)


# In[11]:


avg_by_hour = []

for hr in comments_by_hour:
    avg_by_hour.append([hr, comments_by_hour[hr] / counts_by_hour[hr]])
    
print(avg_by_hour)


# ### Step 5: Finding the Hours with the Most Comments

# In[16]:


swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])

print(swap_avg_by_hour)
print('\n')
sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print(sorted_swap)


# In[17]:


print("Top 6 Hours for Ask Posts Comments")

for avg, hr in sorted_swap[:6]:
    print("{}: {:.2f} average comments per post".format(
            dt.datetime.strptime(hr, "%H").strftime("%H:%M"),avg))


# 3:00pm is the time for which an `ask hn` post receives the most comments. This time is in EST according to the data documentation. 
