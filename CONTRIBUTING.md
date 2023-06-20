# Contributing

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

- [Types of Contributions](#types-of-contributions)
- [Contributor Setup](#setting-up-the-code-for-local-development)
- [Contributor Guidelines](#contributor-guidelines)

## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at [https://github.com/datasciencecampus/uk-parliament-stats/issues](https://github.com/datasciencecampus/uk-parliament-stats/issues).

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- If you can, provide detailed steps to reproduce the bug.
- If you don't have steps to reproduce the bug, just note your observations in as much detail as you can.
  Questions to start a discussion about the issue are welcome.
  
### Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "please-help" is open to whoever wants to implement it.

Please do not combine multiple feature enhancements into a single pull request.

Note: this project is very conservative, so new features that aren't tagged with "please-help" might not get into core.
We're trying to keep the code base small, extensible, and streamlined.
Whenever possible, it's best to try and implement feature ideas as separate projects outside of the core codebase.

### Submit Feedback

The best way to send feedback is to file an issue at [https://github.com/datasciencecampus/uk-parliament-stats/issues](https://github.com/datasciencecampus/uk-parliament-stats/issues).

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Setting Up the Code for Local Development
** TO DO **

## Contributor Guidelines

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request should be contained:
   if it's too big consider splitting it into smaller pull requests.
3. If the pull request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
4. The pull request must pass all CI/CD jobs before being ready for review.
5. If one CI/CD job is failing for unrelated reasons you may want to create another PR to fix that first.

### Coding Standards

- PEP8
- Functions over classes except in tests
- Quotes via [http://stackoverflow.com/a/56190/5549](http://stackoverflow.com/a/56190/5549)

  - Use double quotes around strings that are used for interpolation or that are natural language messages
  - Use single quotes for small symbol-like strings (but break the rules if the strings contain quotes)
  - Use triple double quotes for docstrings and raw string literals for regular expressions even if they aren't needed.
  - Example:

    ```python
    LIGHT_MESSAGES = {
        'English': "There are %(number_of_lights)s lights.",
        'Pirate':  "Arr! Thar be %(number_of_lights)s lights."
    }
    def lights_message(language, number_of_lights):
        """Return a language-appropriate string reporting the light count."""
        return LIGHT_MESSAGES[language] % locals()
    def is_pirate(message):
        """Return True if the given message sounds piratical."""
        return re.search(r"(?i)(arr|avast|yohoho)!", message) is not None
    ```
Acknowledgement: 
This contribution guidance has been mostly replicated from a great example in the [cookiecutter](https://github.com/cookiecutter/cookiecutter/blob/main/CONTRIBUTING.md) repository. 
