import praw
import random
import re

reddit = praw.Reddit(
    client_id="<your_client_id_here>",
    client_secret="<your_client_secret_here>",
    user_agent="<your_user_agent_here>",
    username="<your_username_here>",
    password="<your_password_here>"
)

def contains_link(text):
    pattern = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    if re.search(pattern, text):
        return True
    else:
        return False
    

def list_contains_link(string_list):
    for text in string_list:
        if contains_link(text):
            return True
    return False


def get_random_story(subreddit_name, limit=10, nsfw: bool = True, comments_required: int = 50):
    look_again = False
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=limit)

    posts_list = list(posts)

    random_post_number = random.randint(0, len(posts_list) - 1)
    random_post = posts_list[random_post_number]


    used_posts = []
    with open('used_posts.dat', 'r') as file:
        used_posts = [line.strip() for line in file]
    
    if(random_post.id in used_posts):
        reason = f"You have already generated a video for this post. Post's id: {random_post.id}. To view the list of already generated posts view the used_posts.dat (it's in the same directory in which the main.py is)."
        look_again = True

    if(random_post.num_comments < comments_required):
        reason = f"Post contained less than {comments_required} comments."
        look_again = True

    if(random_post.over_18 and nsfw == False):
        reason = f"Post was tagged as nsfw while the nsfw setting had the value of {nsfw}."
        look_again = True

    if(look_again):
        print(f"[-] Something that we don't want to happen, happened when finding a story. Reason: {reason}")
        print("[i] looking for a new story...")

        return get_random_story(subreddit_name=subreddit_name, limit=limit, nsfw=nsfw, comments_required=comments_required)

    return random_post


def get_best_comments(submission_id, limit=10):
    comments = []

    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=0)

    for top_level_comment in submission.comments:
        comments.append(top_level_comment.body)
        
        if(len(comments) >= limit):
            break

        elif(top_level_comment.body == "[deleted]"):
            return None
    
    if(list_contains_link(comments) == True):
        return None

    return comments