# smart-locators-playwright

## Description
`smart-locators-playwright` is a utility library for Playwright that simplifies element locating by providing a single method to find elements instead of using various Playwright methods directly. It supports multiple locator types simultaneously, reducing the chances of tests failing due to flaky tests. If locator A doesn't work, it will automatically attempt locator B and return matching elements.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


   
## Installation

Install smart-locators-playwright with pip

```bash
  pip install smart-locators-playwright
```
    
## Usage/Examples

To use smart-locators-playwright, first create an instance of the SmartLocators class with your Playwright page object. Then, call the find() method with the appropriate locators.

```
from smart-locators-playwright import SmartLocators

# Initialize with Playwright page object
smart_locators = SmartLocators(page=my_page)

# Find an element using multiple locators
ele = smart_locators.find(id="foo", name="bar", first_match=False)

```

