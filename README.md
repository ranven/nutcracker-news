
# :chestnut: Nutcracker-news :chestnut:

Idea: Social site/discussion forum similar to <a href="https://news.ycombinator.com/">Hacker News</a>. 

<h3>Features</h3>
<ul>
<li>
  Authentication; user can create an account and log in/out.</li>
  <li>User can read posts on the main feed.</li>
 <li>User can sort main feed posts by votes, number of comments or time.</li>
  <li>User can search for posts with keywords.</li>
  <li>User can create posts for the main feed.</li>
  <li>User can comment on posts.</li>
  <li>User can edit their posts and comments.</li>
  <li>User can upvote or downvote posts.</li>
  <li>User has an user profile page and they can edit their profile. </li>
  <li>Users' posts and comments can be viewed from their profile page.</li>
  </ul>
  
<h3>Testing in production</h3>

Deployed site is available at https://nutcracker-news.fly.dev/ 

Due to fly.io's free tier's limitations, the front page might occasionally display no posts or other strange errors might appear. In case this occurs, please refresh the page. (might take a few attempts...)

<h3>Local testing</h3>

After cloning the repository, run the following commands in the root folder to install dependencies and activate the virtual environment: 

<code>$ python3 -m venv venv</code><br/>
<code>$ source venv/bin/activate</code><br/>
<code>$ pip install -r requirements.txt </code><br/>

Local psql database should also be created and the credentials added to a local .env file in the following format:

<code>DATABASE_URL=[insert url here]</code><br/>
<code>SECRET_KEY=[insert key here]</code><br/>

After completing these steps, start the app with <code>flask run</code>. The app runs the schema.sql file automatically on start.

