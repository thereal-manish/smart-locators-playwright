# 🔍 smart-locators-playwright

**A smart, resilient way to locate elements in Playwright for Python — reduce flakiness, simplify locators, and write cleaner test code. - Now with self-healing capabilities**

[![PyPI version](https://badge.fury.io/py/smart-locators-playwright.svg)](https://pypi.org/project/smart-locators-playwright/)

## 🚀 What is it?

`smart-locators-playwright` is a utility wrapper around Playwright’s native locator system. It allows you to define **multiple locator strategies at once**, and it will **automatically try each until one succeeds** — no more writing fallback logic or suffering flaky tests due to minor DOM changes.

## Why Smart Locators?

Element location is often the most brittle part of web automation. Web UIs change frequently, and a single broken locator can cascade failures across your entire test suite. Smart Locators solves this by providing:

- **Unified API**: One simple `find()` method instead of chaining multiple Playwright methods
- **Automatic Fallback Strategy**: Tries multiple locators in sequence until one succeeds — your tests survive minor DOM changes
- **Custom Attribute Support**: Locate elements by any HTML attribute (data attributes, custom attributes, etc.) automatically converted to XPath
- **Reduced Maintenance**: When UI changes occur, your tests can still pass using fallback locators instead of requiring immediate refactoring
- **Both Sync & Async Support**: Works seamlessly with both `playwright.sync_api` and `playwright.async_api`
## Installation

Install smart-locators-playwright with pip

```bash
  pip install smart-locators-playwright
```
    

## ✅ Key Features

### 1. 🔗 Unified Element Location API

Instead of writing multiple locator calls and chaining methods:

```python
# Traditional Playwright approach (brittle)
element = page.get_by_role("button") ## Find an element by role
element_2 = page.locator("//button[@id='submit_btn']") ## Find an element using xpath
```

Use a single, intuitive `find()` method that accepts multiple strategies:

```python
# Smart Locators approach (resilient)
element = smart.find(id="submit", text="Submit", role="button")
```

This is cleaner, more readable, and handles all the fallback logic internally.

---

### 2. 🧩 Multiple Location Strategies

The `find()` method supports all standard Playwright locators, plus custom strategies:

#### ✅ Built-in Playwright Strategies:
- `id`: Element ID attribute
- `text`: Text content
- `role`: ARIA role
- `label`: Associated label text
- `placeholder`: Placeholder text
- `alt`: Alt text (for images)
- `title`: Title attribute

#### 🛠️ Additional Custom Strategies:
- `name`: Name attribute
- `css`: CSS selector
- `xpath`: XPath expression
- `any other attribute`: Will be auto-converted to XPath

---

### 3. 🔄 Automatic Fallback Strategy

Locators are tried sequentially until one succeeds. This makes your tests **resilient to DOM changes** without requiring test refactoring:

```python
# Will try: id → name → text (in that order)
element = smart.find(id="loginBtn", name="submitLogin", text="Login")
```

If the element's `id` changes or is removed, the library automatically falls back to the `name` attribute, then the text content. Your test remains stable despite UI modifications.

---

### 4. 👥 Support for Multiple Elements

By default, `find()` returns the first matching element. Set `first_match=False` to retrieve all matching elements:

```python
# Get the first matching button (default)
button = smart.find(role="button", first_match=True)
button.click()

# Get all matching buttons as a Locator collection
all_buttons = smart.find(role="button", first_match=False)

# Iterate through all buttons
for button in all_buttons.all():
    print(button.text_content())
```

---

### 5. 🔧 Self-Healing Locators

Smart Locators can automatically **extract and store element attributes** after finding them. This enables a self-healing mechanism where you can maintain a centralized locator repository and easily update locators when your application changes.

```python
# Enable self-healing: automatically save element attributes to a JSON file
element = smart.find(
    id="submit-btn",
    name="submit",
    text="Submit",
    first_match=True,
    locator_update=True,  # Enable locator extraction
    element_name="submit_button",  # Name for the locator entry
    locators_file="./locators/app_locators.json"  # Where to save the locators
)

element.click()
```

When `locator_update=True`, the found element's HTML attributes are automatically extracted and saved to the specified JSON file. This creates a reusable locator repository that can be updated over time, reducing maintenance overhead when your application's UI evolves.

**Generated JSON file example:**
```json
{
  "submit_button": {
    "id": "submit-btn",
    "class": "btn btn-primary",
    "type": "button",
    "data-testid": "submit-button",
    "aria-label": "Submit form"
  }
}
```

This feature is particularly useful for:
- Maintaining a centralized locator library
- Documenting all available attributes for each element
- Making updates quick and painless when the UI changes
- Sharing locators across multiple test files

---

## Usage/Examples

```python
## Finding single element

from playwright.sync_api import sync_playwright
from smart_locators_playwright import SmartLocators

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    smart = SmartLocators(page)

    # Try locating using multiple strategies
    element = smart.find(
        id="submit-btn",
        name="submit",
        text="Submit",
        role="button",
        first_match=True  # Stop at the first successful match
    )

    element.click()
    browser.close()

```


```python
## Finding multiple element

# Return all matching elements instead of just the first
buttons = smart.find(
    role="button",
    first_match=False
)

# Iterate through elements
for button in buttons:
    print(button.text_content())
```

```python
## Custom Attributes

# Find by data attributes or any custom attribute
element = smart.find(
    data_testid="submit-button",  # Converted to XPath
    data_cy="login"               # Converted to XPath
)
```

```python
## Combining with Playwright's Chain API
## The returned object is a standard Playwright Locator that can be further refined:

# Find a button inside a specific container
button = smart.find(role="button", text="Submit").filter(has_text="Submit")
```

```python
# Find all rows in a table
rows = smart.find(
    css="table#users tr",
    first_match=False
)

# Process each row
for row in rows.all():
    username = row.locator("td").nth(0).text_content()
    email = row.locator("td").nth(1).text_content()
    print(f"User: {username}, Email: {email}")
```
## Supported Locators

| Locator Type | Description                                                    |
|--------------|----------------------------------------------------------------|
| `id`         | Locate by `id` attribute.                                    |
| `name`       | Locate by `name` attribute.                                  |
| `css`        | Locate by a CSS selector.                                    |
| `xpath`      | Locate by an XPath expression.                               |
| `label`      | Locate by the associated `label` attribute.                  |
| `alt`        | Locate by `alt` attribute (for images and other media).       |
| `placeholder`| Locate by `placeholder` attribute (for form inputs).         |
| `role`       | Locate by `role` attribute (ARIA roles, such as "button", "textbox", etc.). |
| `text`       | Locate by text content (useful for buttons, links, etc.).    |
| `title`      | Locate by `title` attribute (often used for tooltips, hover text, etc.). |


## 📚 API Reference

### `SmartLocators(page)`

Initializes the Smart Locators instance.

#### Parameters:
- `page` (playwright.sync_api.Page | playwright.async_api.Page): The Playwright page object. Supports both synchronous and asynchronous page instances.

#### Example:
```python
from playwright.sync_api import sync_playwright
from smart_locators_playwright import SmartLocators

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    smart = SmartLocators(page)  # Initialize Smart Locators
```

---

### `find(id=None, name=None, css=None, xpath=None, label=None, alt=None, placeholder=None, role=None, text=None, title=None, first_match=True, **kwargs)`

Locates web elements using one or more locator strategies, trying each in sequential order until a match is found.

#### Parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | None | Element's `id` attribute |
| `name` | str | None | Element's `name` attribute |
| `css` | str | None | CSS selector expression |
| `xpath` | str | None | XPath expression |
| `label` | str | None | Associated label text |
| `alt` | str | None | Alt text (images, media) |
| `placeholder` | str | None | Input placeholder text |
| `role` | str | None | ARIA role (button, textbox, etc.) |
| `text` | str | None | Element text content |
| `title` | str | None | Element title attribute |
| `first_match` | bool | True | If `True`, returns the first match; if `False`, returns all matches as a Locator collection |
| `locator_update` | bool | False | **[Self-Healing]** If `True`, automatically extracts and saves element attributes to a JSON file |
| `element_name` | str | "" | **[Self-Healing]** Name/key for the locator entry in the JSON file (required when `locator_update=True`) |
| `locators_file` | str | "C:/SmartLocatorsLogs/" | **[Self-Healing]** Path to the JSON file where locator attributes will be saved |
| `**kwargs` | dict | {} | Any custom HTML attributes (auto-converted to XPath) |

#### Returns:
- **Locator**: A Playwright Locator object representing the found element(s).
  - When `first_match=True`: Returns a single element Locator
  - When `first_match=False`: Returns a Locator collection that can be iterated with `.all()`

#### Raises:
- **NoSuchElementException**: If no element matches any of the provided locators.
