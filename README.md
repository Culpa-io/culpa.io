<img width="1362" alt="Screen Shot 2021-08-30 at 8 12 43 AM" src="https://user-images.githubusercontent.com/22382740/131337168-55d5cb55-b174-4ec2-bf29-26d927187b92.png">

# Culpa.io

Culpa.io is an open source resource for students at Columbia to anonymously review courses, professors, and more. It's been used over 100,000 times since its inception in September 2021, and is growing fast! If you attend Columbia, culpa.io is yours: there are no secretive owners or administrators, just the open source maintainers you see here. 

If you are looking to review a class or read reviews about a professor, you can check out the website here: https://www.culpa.io/ 

If you want to contribute to the project and learn more about how it's run, keep reading below.

## Setup 

To get started, clone this repository using the following command: 

`git clone https://github.com/Culpa-io/culpa.io`

If you are not familiar with git, that's fine! Check out [these resources](https://docs.github.com/en/get-started) and head back when you are all set up. You can also join the Culpa [discord](https://discord.com/invite/adWZA6Qwq6) here for assistance.

To run this project, you will need [Python 3](https://www.python.org/downloads/) installed on your computer. Before attempting to run the project, you must install the required packages by running `python3 -m pip install -r requirements.txt`.

**Note:** The above command can result in a lot of scary looking errors, especially if it's your first time running a python project. Don't fret. You can either [create an issue](https://github.com/Culpa-io/culpa.io/issues/new) describing your problem, or join the [discord](https://discord.com/invite/adWZA6Qwq6). There are other students who will be happy to assist you.

## Development

To run your local version of culpa, type `python3 manage.py runserver` in your terminal and hit enter. Paste the following URL (`http://127.0.0.1:8000/`) in your browser to use the site.

[Branches](https://en.wikipedia.org/wiki/Branching_(version_control)) are an important part of software development. If you make a change to culpa, please open a pull request so that others can double check your work. It is never a good idea to push directly to master.