Demo hosted on GitHub (GitHub Pages):
https://boilerplate.saeidmohadjer.com/

## A boilerplate for building modern HTML Websites

### You can use this boilerplate to build static responsive HTML sites that can be run on any server. 

**Features**
* Uses npm scripts without task runners such as Gulp or Grunt to do a variety of tasks such as support for Sass, transpiling ES6, and minifying CSS and scripts.
* No dependency on CSS or JavaScript frameworks
* Full support of ES6 features including ES6 modules
* Support and precompiling of Handlebars templates
* Automated deployment of built version to GitHub Pages using GitHub Actions after every commit to master

**Requirements**
* Local server capable of serving HTML files
* Latest version of Nodejs and NPM

**Usage**
* Clone repo and run "npm install" from command line.
* Run: "npm start" to serve files from "public" folder on local server
* Run: "npm run build" to build project into the "dist" folder

**Hosting Website on GitHub**

To host your Website on GitHub Pages you need a GitHub account. If you don't have one, you can create an account at: https://github.com/signup

Once you have created and logged into your account you need to create a public repository for your site there. Go to https://github.com/new and for repository name enter website or whatever you like (use a single lowercase word) and then click the green button to create the repository. 

Next you need to push your site to this repository and setup GitHub Pages and GitHub Actions to automate building and delploying of your site after every change. If you don't feel comfortable doing such changes yourself you can invite me as a collaborate to your repository so I will do them. To do this go to Settings tab of your repository and in sidebar select “Manage access”. Then click on “Add people” button and search for username "smohadjer" to invite me as a collaborator.

**Using Custom Domain**

By default a site hosted on GitHub Pages is available at: https://yourusername.github.io/repository/. If you wish to use a custom domain for your site you need to add/edit CNAMW and A (or AAA) records of your domain as instructed on this page:
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain

In short you need two changes:
1. Add an A record to your DNS so domain yourdomain.com points to following ip numbers:
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
2. Add a CNAME record to your DNS so that the subdomain www.yourdomain.com directs to yourusername.github.io.

**Using local build**

When fixing build issues or updating build process it will be easier to use a local build. To allow this clone build repository from github, run npm install in build folder and then in package.json change "build" entry to:
````
	"devDependencies": {
		"build": "file:../build",
	},
````
When you are done with build changes, revert package.json.
