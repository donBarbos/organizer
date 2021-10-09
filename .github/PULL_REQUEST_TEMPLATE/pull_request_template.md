# How to create a pull request

1. [Fork the project repository](https://github.com/DONSIMON92/organizer/fork/)
2. Clone your fork: `git clone https://github.com/<YOUR_GITHUB_USERNAME>/organizer.git`
4. Setup your Python enviroment
   - Create a virtual environment and install dependencies using [Poetry](https://python-poetry.org "python package manager"): `poetry install`
   - Setting an environment variables
5. Implement your changes
6. Check it for PEP8: `flake8 organizer`
7. Add files, commit and push:
    ```
    git add <MODIFIED_FILES> ;\
    git commit -m <YOUR_COMMIT_MESSAGE> ;\
    git push
    ```
8. Create a Pull Request on Github. Write a **clear description** for your request, including all the context and relevant information, such as:
   - Motivation: Why did you create this PR? What do you want from this function?
   - Any other useful information: PEP you were guided by; example of a project where this approach was successfully used
