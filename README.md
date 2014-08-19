<h1>Hawk</h1>
<h2>Introduction</h2>
<p>Hawk is a really simple app that aims to discover customers given terms. As for <b>FoundationDB</b>
those customers are the ones that has terms like "database, error" but it can be changed anytime.</p>
<h2>Purpose</h2>
<p>Hawk takes the advantage of FoundationDB's blazing speed in order store users with given frequency count of the
words included in the tweets that also mention "database", "error" such terms like that. Then we can discover
what are the most popular words used other our terms in order to get a clear idea what user needs.
<h2>Technology</h2>
<table>
<tr>
  <td><b>Programming Language: </b></td>
  <td>Python</b>
  <td><b>Data: </b></td>
  <td>FoundationDB</b>
  <td><b>Other APIs: </b></td>
  <td>Python-Twitter</b>
</tr>
</table>
<h2>To Do</h2>
<p>Here are some things that could be done in order to improve <b>Hawk</b>;</p>
<ul>
  <li><b>NLP:</b> This app features a simple dummy algorithm that checks for word match however we can apply a custom NLP
  algorithm to tweets brought in order to make sure the tweet somewhat relates to a complaint instead of a good tweet.
  We wouldn't want to bother someone saying "DB X solves all the database errors and problems. I love it!"</li>
  <li><b>No Tweet ID check:</b>Currently tweets are not checked so after each iteration if the API returns the same results,
  the words ranked still increased. So the Tweet ID's must be checked in order
  to prevent rate increase for duplicate tweets returned</li>
  <li><b>Further Options:</b>As we all know we can add many options from hashtags to mentions, geocoding to number of followers
  using Twitter API's when finding our users</li>
  <li><b>Potential Customer Info Storage: </b>API only provides screen names of the potential user, but also full name, email can be provided as well for easier contact.</li>
</ul>
