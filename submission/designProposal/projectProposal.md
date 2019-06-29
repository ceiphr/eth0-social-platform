# Eth0 (Project Name)
### Description
This project is reddit built in a week with Django and web frameworks

### Competitive Analysis
One project I might have noticed was reddit. The difference between reddit and my project is that mine will be python based and open source. Reddit is not FOSS. 
Also mine will be limited in features as I am a child with a week and Reddit is a company with teams of devs and years with their project. For instance, they have a community system where posts are submitted to communities. I don't have that. 
They also have a reporting system and a means of monetization which I will not be adding to my project. But my project will act as a federated system where each instance of the app on a VPS will be a community.

### Structural Plan
* Database - Handles all posts, comments, and votes
* Accounts - Handles all account data, sign ups, log ins, etc.
* Templates - Handles all frontend content (html w/ Django)
* Static - All static contents (css, js, images, etc.) that will be served to templates
* Main Project - Handles all url and database queries, and serves templates and static content

### Algorithmic Plan
* Feed sorting - Content will be sorted based on timestamp and vote count.
	* Will use merge sort because recursion is efficient
	* Default Feed: most popular in a week
		* Will sort through all posts within the week from most votes to least
		* If a post is from more than a week ago it isn't sorted for the current week and is instead sorted for the previous week
	* If sorting by new, will provide content based on most recent timestamps within the week
*  Comments will be sorted like feed content

### Timeline Plan
* Monday:
	* Finish account system
	* Have post/votes/comments authenticated
* Tuesday
	* Fix upvoting with AJAX
	* Add ability to delete posts
	* Finish commenting system
		* Commenting on posts
		* Deleting posts
* Wednesday
	* Store assets for posts 
	* Design front page
	* Design post/commenting page
* Thursday
	* Have running prototype on VPS
	* Stress test?
	* Security hardening?

### Version Control Plan
* Backing up everything automatically to my Nextcloud instance
	* https://drive.ceiphr.com/index.php/s/AEkApicGYjJwe2y
* Commiting everything to a GitLAB repo b/c Github got acquired my MS
	* https://gitlab.com/ceiphr/eth0

### TP2 Update
* There was **none**.

### TP3 Update
* No profile system
* I will not be deploying the site to a production VPS for TP3, this will be at a later date
* UI/UX finished with material design
* All sorting functionality finished
* Voting system done and polished
