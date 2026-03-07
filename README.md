# smart-locators-playwright

🔍 A smart, resilient way to locate elements in Playwright for Python — reduce flakiness, simplify locators, and write cleaner test code.

[![PyPI version](https://img.shields.io/pypi/v/smart-locators-playwright.svg)](https://pypi.org/project/smart-locators-playwright/)

## 🚀 What is it?

**smart-locators-playwright** is a utility wrapper around Playwright's native locator system. It allows you to define multiple locator strategies at once, and it will automatically try each until one succeeds — no more writing fallback logic or suffering flaky tests due to minor DOM changes.

### Why Smart Locators?

Element location is often the most brittle part of web automation. Web UIs change frequently, and a single broken locator can cascade failures across your entire test suite. Smart Locators solves this by providing:

- **Unified API**: One simple `find()` method instead of chaining multiple Playwright methods
- **Automatic Fallback Strategy**: Tries multiple locators in sequence until one succeeds
- **Custom Attribute Support**: Locate elements by any HTML attribute automatically converted to XPath
- **Reduced Maintenance**: When UI changes occur, your tests can still pass using fallback locators
- **Both Sync & Async Support**: Works seamlessly with `playwright.sync_api` and `playwright.async_api`
- **Self-Healing Locators**: Automatically extract and store element attributes for easy updates

## 📦 Installation

Install **smart-locators-playwright** with pip:

```bash
pip install smart-locators-playwright
```

## ✅ Key Features

### 1. 🔗 Unified Element Location API

Instead of writing multiple locator calls:

```python
# Traditional Playwright (brittle)
element = page.get_by_role("button")
element_2 = page.locator("//button[@id='submit_btn']")
```

Use a single, intuitive `find()` method:

```python
# Smart Locators (resilient)
element = smart.find(id="submit", text="Submit", role="button")
```

### 2. 🧩 Multiple Location Strategies

The `find()` method supports all standard Playwright locators, plus custom strategies:

**✅ Built-in Playwright Strategies:**
- `role` - ARIA role (button, textbox, etc.)
- `text` - Text content
- `label` - Associated label text
- `alt` - Alt text (for images)
- `placeholder` - Placeholder text
- `title` - Title attribute

**🛠️ Additional Custom Strategies:**
- `id` - ID attribute (auto-converted to XPath)
- `name` - Name attribute (auto-converted to XPath)
- `css` - CSS selector
- `xpath` - XPath expression
- **Any custom attribute** - Auto-converted to XPath (e.g., `data-testid`, `data-cy`)

### 3. 🔄 Automatic Fallback Strategy

Locators are tried sequentially until one succeeds. This makes your tests resilient to DOM changes:

```python
# Will try: id → name → text (in that order)
element = smart.find(id="loginBtn", name="submitLogin", text="Login")
```

If the element's ID changes, the library automatically falls back to the name attribute, then text content. Your test remains stable without refactoring.

### 4. 👥 Support for Multiple Elements

By default, `find()` returns the first matching element. Set `first_match=False` to retrieve all matching elements:

```python
# Get the first matching button (default)
button = smart.find(role="button", first_match=True)
button.click()

# Get all matching buttons
all_buttons = smart.find(role="button", first_match=False)

# Iterate through all buttons
for button in all_buttons.all():
    print(button.text_content())
```

### 5. 🔧 Self-Healing Locators

Smart Locators can automatically extract and store element attributes for a self-healing mechanism:

```python
# Enable self-healing: save element attributes to JSON

# Read locators.json
with open("./tests/locators.json", "r", encoding="utf-8") as f:
    locators_data = json.load(f)

# Extract ID value
element_id = locators_data["submit_btn"]["id"]

element = smart.find(
    id=element_id,
    name="submit",
    text="Submit",
    first_match=True,
    locator_update=True,              # Enable extraction
    element_name="submit_button",     # Locator entry name
    locators_file="./locators/app_locators.json"
)

element.click()
```

**Generated JSON file (default location: `{cwd}/SmartLocatorsLogs/default.json`):**

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

**Benefits:**
- Maintain a centralized locator library
- Document all available attributes for each element
- Make updates quick when UI changes
- Share locators across multiple test files
- Automatic XPath generation for custom attributes

## 📚 Usage Examples

### Finding a Single Element

```python
from playwright.sync_api import sync_playwright
from smart_locators_playwright import SmartLocators

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    smart = SmartLocators(page)

    # Try multiple strategies
    element = smart.find(
        id="submit-btn",
        name="submit",
        text="Submit",
        role="button",
        first_match=True
    )

    element.click()
    browser.close()
```

### Finding Multiple Elements

```python
# Return all matching elements
buttons = smart.find(
    role="button",
    first_match=False
)

# Iterate through elements
for button in buttons.all():
    print(button.text_content())
```

### Custom Attributes with Auto XPath Conversion

```python
# Find by data attributes or any custom attribute
# These are automatically converted to XPath expressions
element = smart.find(
    data_testid="submit-button",
    role="button"
)

# Auto-converted to: //*[@data-testid='submit-button']
element.click()
```

### Combining with Playwright's Chain API

The returned object is a standard Playwright Locator that can be further refined:

```python
# Find a button with additional filtering
button = smart.find(role="button", text="Submit").filter(has_text="Submit")

# Find all table rows
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

### Self-Healing with Locator Update

```python
# Automatically extract and save element attributes

# Read locators.json
with open("./tests/locators.json", "r", encoding="utf-8") as f:
    locators_data = json.load(f)

# Extract ID value
element_id = locators_data["submit_btn"]["id"]

button = smart.find(
    id=element_id,
    name="submit_button",
    text="Submit",
    element_name="submit_btn",
    locator_update=True,
    locators_file="./tests/locators.json"
)

# Element attributes are now saved to ./tests/locators.json
button.click()
```

### Async Support

```python
from playwright.async_api import async_playwright
from smart_locators_playwright import SmartLocators

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")

        smart = SmartLocators(page)
        element = smart.find(role="button", text="Submit")
        await element.click()
        await browser.close()

import asyncio
asyncio.run(main())
```

## 📖 Supported Locators

| Locator Type | Description | Playwright Native | Auto-Conversion |
|--------------|-------------|-------------------|-----------------|
| `role` | ARIA role (button, textbox, etc.) | ✅ | — |
| `text` | Element text content | ✅ | — |
| `label` | Associated label text | ✅ | — |
| `alt` | Alt attribute (images, media) | ✅ | — |
| `placeholder` | Input placeholder text | ✅ | — |
| `title` | Title attribute | ✅ | — |
| `id` | ID attribute | ❌ | XPath |
| `name` | Name attribute | ❌ | XPath |
| `css` | CSS selector | ✅ | — |
| `xpath` | XPath expression | ✅ | — |
| Custom attributes | Any HTML attribute | ❌ | XPath |

## 🔌 API Reference

### `SmartLocators(page)`

Initializes the Smart Locators instance.

**Parameters:**
- `page` (`playwright.sync_api.Page` or `playwright.async_api.Page`): The Playwright page object.

**Attributes:**
- `_playwright_allowed_locators`: List of native Playwright locator types
- `_custom_locators`: List of custom locator types (css, xpath)
- `_locators_file`: Default locators file path (`{cwd}/SmartLocatorsLogs/default.json`)

**Example:**
```python
from playwright.sync_api import sync_playwright
from smart_locators_playwright import SmartLocators

with sync_playwright() as p:
    page = p.chromium.launch().new_page()
    smart = SmartLocators(page)
```

### `find(...)`

Locates web elements using one or more locator strategies with automatic fallback.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | None | Element's id attribute |
| `name` | str | None | Element's name attribute |
| `css` | str | None | CSS selector expression |
| `xpath` | str | None | XPath expression |
| `label` | str | None | Associated label text |
| `alt` | str | None | Alt text (images, media) |
| `placeholder` | str | None | Input placeholder text |
| `role` | str | None | ARIA role (button, textbox, etc.) |
| `text` | str | None | Element text content |
| `title` | str | None | Element title attribute |
| `first_match` | bool | True | Return first match only; if False, returns all matches |
| `locator_update` | bool | False | [Self-Healing] Enable automatic attribute extraction |
| `element_name` | str | "" | [Self-Healing] Key name for locator entry in JSON |
| `locators_file` | str | "" | [Self-Healing] Path to JSON file (uses default if empty) |
| `**kwargs` | dict | {} | Custom HTML attributes (auto-converted to XPath) |

**Returns:**
- `Locator`: A Playwright Locator object
  - When `first_match=True`: Returns single element Locator
  - When `first_match=False`: Returns Locator collection (use `.all()` to iterate)

**Raises:**
- `custom_exceptions.NoSuchElementException`: If no element matches any provided locators

**Example:**
```python
# Single element
button = smart.find(role="button", text="Submit")

# Multiple elements
all_buttons = smart.find(role="button", first_match=False)

# With self-healing
element = smart.find(
    id="test-id",
    role="button",
    element_name="my_button",
    locator_update=True,
    locators_file="./locators.json"
)
```

### `update_locators(element_name, webelement, locators_file)`

Manually updates a locator by extracting and saving element attributes.

**Parameters:**
- `element_name` (str): Key name for the locator entry
- `webelement` (Locator): The Playwright Locator object
- `locators_file` (str): Path to the JSON file

**Returns:**
- `bool`: True if successful, False if failed

**Example:**
```python
element = smart.find(role="button")
smart.update_locators("submit_button", element, "./locators.json")
```

### `extract_html_attributes(html_string)`

Parses HTML string and extracts all attributes.

**Parameters:**
- `html_string` (str): HTML content to parse

**Returns:**
- `dict`: Dictionary of attribute name-value pairs

**Example:**
```python
html = '<button id="btn" class="primary" data-test="submit">Click</button>'
attrs = smart.extract_html_attributes(html)
# {'id': 'btn', 'class': 'primary', 'data-test': 'submit'}
```

### `write_locators_to_json(element_name, attributes, locators_file)`

Writes element attributes to a JSON file with validation.

**Parameters:**
- `element_name` (str): Key name for the locator entry
- `attributes` (dict): Element attributes dictionary
- `locators_file` (str): Path to JSON file (creates if doesn't exist)

**Returns:**
- `bool`: True if successful, False otherwise

**Features:**
- Auto-creates parent directories
- Validates inputs
- Appends to existing JSON files
- Formatted with 2-space indentation
- Handles UTF-8 encoding

**Example:**
```python
attrs = {"id": "btn-1", "class": "primary"}
success = smart.write_locators_to_json("my_button", attrs, "./locators.json")
```

## 🎯 Advanced Use Cases

### Smart Fallback for Dynamic IDs

```python
# If element ID changes dynamically, fallback to other strategies
element = smart.find(
    id="dynamic-id-12345",  # Tried first
    name="login_button",     # Fallback
    role="button",           # Fallback
    text="Login"             # Fallback
)
```

### Centralized Locator Repository

```python
# Define once, use everywhere
LOGIN_BUTTON = {
    "id": "login-btn",
    "role": "button",
    "text": "Login"
}

element = smart.find(**LOGIN_BUTTON)
```

### Maintaining Locator Library

```python
# Build locator library on first run
element = smart.find(
    role="button",
    text="Submit",
    element_name="submit_button",
    locator_update=True,
    locators_file="./tests/locators/main.json"
)

# Library automatically grows as you test
```

## 🐛 Error Handling

The library raises `NoSuchElementException` when no locator strategy succeeds:

```python
from smart_locators_playwright import custom_exceptions

try:
    element = smart.find(
        id="nonexistent",
        name="also-nonexistent"
    )
except custom_exceptions.NoSuchElementException:
    print("Element not found with any locator")
```

## 📝 Logging

The library uses Python's `logging` module for debugging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
# View detailed locator extraction and file operations
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request on [GitHub](https://github.com/thereal-manish/smart-locators-playwright).

## 📝 License

This project is licensed under the Apache License - see the LICENSE file for details.

## 🐛 Issues & Support

Found a bug or have a feature request? Please open an issue on [GitHub](https://github.com/thereal-manish/smart-locators-playwright/issues).

## 🎓 Best Practices

1. **Start with most specific locators**: Place exact identifiers first (id, role) before generic ones (text)
2. **Use self-healing for critical elements**: Enable `locator_update=True` for elements that frequently change
3. **Maintain a centralized locator file**: Keep all `locators_file` paths consistent across tests
4. **Combine strategies**: Use multiple locators to create resilient element location
5. **Regular maintenance**: Review and update JSON locator files when UI changes occur