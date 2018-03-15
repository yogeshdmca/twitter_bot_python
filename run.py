from twitterbotpython import TwitterBot


if __name__ == "__main__":
    twi = TwitterBot()
    print('''
    Select Option that you need to execute:
    1. retweet like follow by the kewords given on settings.
    2. Unfollow users that don't follow you back.
    3. Delete Retweets of last 2 days.
    4. Search user by keyword and follow users. 
    10. Quit.
    '''
          )
    userChoice = input('Enter the number of the action that you want to take: ')
    choices = {
        1: twi.retweet_like_follow_by_kewords,
        2: twi.unfollow_back,
        3: twi.delete_tweet,
        4: twi.search_and_follow_user,
        10: quit
    }

    choices[int(userChoice)]()