#!/usr/bin/env python
# coding: utf-8

# # Tracking Dual Profitability in the Apple App Store and the Google Play Market
# ---
# 
# For this project, I'm acting as a researcher for a company that builds Android and iOS apps. These apps are available on both platforms. We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. 
# 
# Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.
# 
# 
# ## Finding Relevant Data
# To avoid spending resources on collecting new data ourselves, we should first try to see if we can find any relevant existing data at no cost.
# 
# - A data set containing data about approximately 10,000 Android apps from Google Play; the data was collected in August 2018. You can download the data set directly from this [link](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv).
# - A data set containing data about approximately 7,000 iOS apps from the App Store; the data was collected in July 2017. You can download the data set directly from this [link](https://dq-content.s3.amazonaws.com/350/AppleStore.csv).
# 
# I began by opening the data:

# In[1]:


from csv import reader

#Google Play Data#
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android_data = android[1:]

#Apple Store Data#
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
apple = list(read_file)
apple_header = apple[0]
apple = apple[1:]


# The above lines will import the data. Next, I'll define a funtion `explore_data()` to make the data easier to navigate. It will also tell us the # of rows and columns of the data set. 

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # adds new line after each row
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        
print(apple_header)
print('\n')
explore_data(apple, 0, 4, True)


# **The above output reveals:**
# * 16 columns of data for each app
# * columns like 'prime_genre' are probably important, while the unique 'id' isn't
# * I displayed the first 4 rows after the header to preview the data set
# * There's a total of 7,197 apps in this data set
# 
# **I'm going to do the same for the Android data to preview:**

# In[3]:


print(android_header)
print('\n')
explore_data(android, 1, 5, True)


# **The above output reveals:**
# * 13 columns of data for each app
# * Like the Apple data, `'Genres'` is probably imporant, but we could disregard columns like `'current ver'`
# * I displayed the first 4 rows after the header to preview the data set
# * There's a total of 10,842 apps in this data set
# 
# **Observing both data sets at a glance reveals:**
# * The Android set is larger, but the difference is within reason
# * Both data sets have similar columns, but a little cleaning will be necessary

# ## Data Cleaning
# 
# In general, inaccurate and duplicate data needs to be corrected or removed. Specific to this analysis, we're only looking at free apps that utilize English as the primary language. I'll need to:
# * Remove non-English apps
# * Remove paid apps
# 
# 
# **Android Cleaning**
# 
# The discussion section for the data set on Kaggle revealed that there's a lot of duplicate entries and one specific app has a rating of 19 stars (out of 5). This should probably be 1.9 stars, but since we have so many, we'll delete it (row 10472).

# In[4]:


print(android_data[10472])


# In[5]:


print(len(android_data)) #checking the length before deleting
del android_data[10472]
print(len(android_data)) #checking the length after deleting


# Next, I'll remove duplicate entries. For example, Twitter is actually three several times in the data set. The first two are likely exact duplicates and the earlier one (July 30th) might have been an earlier version that wasn't removed upon being updated.

# In[6]:


for app in android:
    name = app[0]
    if name == 'Twitter':
        print(app)


# I'm going to run a similar loop to determine exactly how many apps are duplicates:

# In[7]:


duplicate_apps = []
unique_apps = []

for app in android_data:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else: 
        unique_apps.append(name)

print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:5])
print('Examples of unique apps:', unique_apps[:5])
    


# Since approximiately 1 in 10 (1181 out of ~10,000) android apps are duplicates, the averages and medians of the data are going to be skewed because of the duplicate results. The duplicates need to be removed, however: 
# * We don't want to remove the duplicates randomly (i.e. if there are 4x entries for Facebook, we don't want to guess to remove #1, #2, #3, or #4). 
# * Rather, we want to keep the Facebook with the *most* ratings, since it is the most recent
# 

# **Removing The Duplicates**
# 
# To remove the duplicates, we will:
# * Create a dictionary, where each dictionary key is a unique app name and the corresponding dictionary value is the highest number of reviews of that app.
# * Use the information stored in the dictionary and create a new data set, which will have only one entry per app (and for each app, we'll only select the entry with the highest number of reviews).
# 

# In[8]:


reviews_max = {}

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# I'm going to compare the `reviews_max` to the total reviews minus duplicate reviews to see if the `reviews_max is` accurate:

# In[9]:


print('Expected Length:', len(android_data) - 1181)
print('Actual Length:', len(reviews_max))


# Since 9659 = 9659, the `reviews_max` is accurate and created the correct output. Since `reviews_max` is accurate, we'll utilize it to remove the duplicate rows.
# * I'll begin by created empty lists: `android_clean` (for the cleaned data set) and `android_duplicated` (for just names of duplicates)
# * Loop through the Android data and append the originals to `android_clean` using the `reviews_max` dictionary.

# In[10]:


android_clean = []
android_duplicated = []

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in android_duplicated):
        android_clean.append(app)
        android_duplicated.append(name)


# I'm now going to run the `Explore_data` on the `Android_clean` to see if the number of rows is 9659:

# In[11]:


explore_data(android_clean, 0, 3, True)


# ### Cleaning: Removing Non-English Apps
# 
# Remember we use English for the apps we develop at our company, and we'd like to analyze only the apps that are directed toward an English-speaking audience. However, if we explore the data long enough, we'll find that both data sets have apps with names that suggest they are not directed toward an English-speaking audience.

# In[12]:


print(apple[813][1])
print(android_clean[4412][0])


# We're not interested in keeping these apps, so we'll remove them. One way to go about this is to remove each app with a name containing a symbol that is not commonly used in English text — English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;), and other symbols (+, *, /).
# 
# All these characters that are specific to English texts are encoded using the ASCII standard. Each ASCII character has a corresponding number between 0 and 127 associated with it, and we can take advantage of that to build a function that checks an app name and tells us whether it contains non-ASCII characters.
# We built this function below, and we use the built-in ord() function to find out the corresponding encoding number of each character.

# In[13]:


def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
    
    return True

print(is_english('Instagram'))


# 
# The function seems to work fine, but some English app names use emojis or other symbols (™, 😂, etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form.
# 
# **To minimize deleting English apps, we'll only remove an app if its name has more than three non-ASCII characters:**

# In[14]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True

#Let's check the is_english function with some examples#
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Instachat 😜'))
print(is_english('Facebook'))


# In[15]:


android_english = []
apple_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in apple:
    name = app[1]
    if is_english(name):
        apple_english.append(app)


# **Isolating The Free Apps**
# 
# I am only analyzing apps that are free to download and install. The data sets contain both free and non-free apps; I'll need to isolate only the free apps for the analysis.

# In[16]:


android_final = []
apple_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in apple_english:
    price = app[4]
    if price == '0.0':
        apple_final.append(app)
        
print(len(android_final))
print(len(apple_final))


# Our cleaned data set consists of 8,864 free Enligh Android apps and 3,222 free English Apple apps.

# ## Finding Successful Apps in Both Markets
# 
# ### Intro
# 
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# * Build a minimal Android version of the app, and add it to Google Play.
# * If the app has a good response from users, we develop it further.
# * If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets. I'll begin the analysis by getting a sense of what are the most common genres for each market:
# * `prime_genre` for Apple App Store data
# * `Genres` and `Category` for Google Play data
# 
# ### Creating Functions for Analyzing:
# 
# I'll build two functions to analyze the frequency tables:
# * One function to generate frequency tables that show percentages
# * Another function to display percentages in a descending order

# In[17]:


def freq_table (dataset, index):
    table = {}
    total = 0
    
    for row in dataset: 
        total +=1 
        value = row[index]
        if value in table:
            table[value] += 1
            
        else: 
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total * 100)
        table_percentages[key] = percentage
        
    return table_percentages

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# ### Initial Analyzation
# 
# I'll begin by analyzing the `prime_genre` column of the App Store data set. I'll be looking for:
# * most common genres
# * other patterns
# * general impressions and recommendations

# In[18]:


display_table(apple_final, -5) #Genre


# Over half of the free English apps are games. However, this does not reveal the number of users. For example, Instagram and Facebook probably have more downloads than most games. In recent years, games also are usually free and generate revenue through in app purchases. 

# In[19]:


display_table(android_final, 1) #Category


# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.

# # Most Popular Apps by Genre on the App Store¶
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# Below, we calculate the average number of user ratings per app genre on the App Store:

# In[20]:


genres_ios = freq_table(apple_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in apple_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together. Many apps also prompt users to leave ratings.

# In[21]:


for app in apple_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[22]:


for app in apple_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# Upon looking into the Finance apps, it appears that most apps are either banks or fintech (credit score or tax refund calculators that would require serious development). There is a few apps that are generic for saving money with tips, so this could be a potential if the current apps seemed to be lacking in features or usability. 

# In[23]:


for app in apple_final:
    if app[-5] == 'Finance':
        print(app[1], ':', app[5])


# ## Most Popular Apps by Genre on Google Play

# In[24]:


display_table(android_final, 5) # the Installs columns


# Although the Android data includes the number of installs, it is not entirely ideal since it is a range and not a definite number of downloads. For simplicity and consistancy, I'll round each number of installs off. (ex. 100,000+ becomes 100,000.)
# 
# To perform computations, however, I'll need to convert each install number to float — this means that I need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error. I'll do this directly in the loop below, where I also compute the average number of installs for each genre (category).

# In[25]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
            
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# The main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# Let's take a look at some of the apps from this genre and their number of installs:

# In[26]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# In[27]:


for app in android_final:
    if app[1] == 'BEAUTY':
        print(app[0], ':', app[5])


# In[28]:


for app in apple_final:
    if app[-5] == 'Lifestyle':
        print(app[1], ':', app[5])


# Both Apple and Android have a significant number of apps in the beauty section. An example of a beauty app that would work well on both Apple and Android would be one that featured high quality videos of tutorials and product reviews (like youtube), but could also have account and a social functionality like Pintrest.

# # Conclusions
# 
# In this project, I analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# Here are some reccomendations that I learned from this project:
# * The most popular apps are in categories that would be hard to penetrate
# * App categories like Finance are popular, but would require extensive development (i.e. connecting a bank account) to make a relevant one today. For example, when the iPhone first came out, a mortgage calculator app would have been profitable, but now that can be done in a Google search.
# * Lifestyle categories have lots of opportunity for new apps because the users are more likely to try new apps and these apps could require less up front infrustructure
