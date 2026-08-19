# Playwright AI Self-Healing Automation Framework

An AI-assisted UI automation framework built with **Python, Playwright, Pytest, Sentence Transformers, and Jenkins**.

The framework demonstrates **self-healing locator recovery**: when a predefined locator fails, the framework analyzes the current page DOM, compares the failed element's stored profile against candidate elements using semantic similarity, identifies the most similar candidate, and retries the action using the recovered locator.

The project also includes **automatic DOM profile generation**, **browser-independent execution**, and **Jenkins CI integration** so that smoke tests can automatically execute after changes are pushed to GitHub.

---------------------------

## Key Features

* Python + Playwright UI automation
* Pytest test framework
* Page Object Model (POM)
* AI-based locator recovery
* SentenceTransformer semantic similarity
* `all-MiniLM-L6-v2` embedding model
* Automatic DOM element profile generation
* JSON-based element profiles
* ProfileStore for loading stored element metadata
* Candidate extraction from the current DOM
* Locator recovery when original locator fails
* Supports Chromium, Firefox and WebKit
* Configurable browser execution from command line
* Smoke test execution using Pytest markers
* Automatic screenshots on test failure
* HTML test reports
* Centralized logging
* Git/GitHub integration
* Jenkins CI
* GitHub webhook triggering through ngrok
* Environment configuration support
* Reproducible dependency installation using `requirements.txt`

----------------

#  Architecture


                         GitHub
                           │
                           │ git push
                           ▼
                    GitHub Webhook
                           │
                           ▼
                         Jenkins
                           │
                           ▼
                  Checkout latest code
                           │
                           ▼
                  Install dependencies
                           │
                           ▼
                  Run Pytest Smoke Tests
                           │
                           ▼
                    Playwright Tests
                           │
                           ▼
                    Page Object Model
                           │
                           ▼
                    BasePage Actions
                           │
                 ┌─────────┴─────────┐
                 │                   │
          Normal Locator       Locator Failure
                 │                   │
                 ▼                   ▼
             Playwright        RecoveryEngine
                                     │
                                     ▼
                              SimilarityEngine
                                     │
                                     ▼
                           SentenceTransformer
                                     │
                                     ▼
                             Candidate Elements
                                     │
                                     ▼
                              Best Match
                                     │
                                     ▼
                           Recovered Locator
                                     │
                                     ▼
                              Retry Action
```

---

#  Project Structure


PlaywrightAutomate/
│
├── ai/
│   ├── __init__.py
│   ├── candidate_extractor.py
│   ├── dom_parser.py
│   ├── element_profile.py
│   ├── profile_generator.py
│   ├── profile_store.py
│   ├── recovery_engine.py
│   └── similarity_engine.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
│
├── profiles/
│   ├── login_page.json
│   ├── inventory_page.json
│   └── cart_page.json
│
├── tests/
│   ├── test_cart.py
│   ├── test_inventory.py
│   ├── test_login.py
│   └── test_profile_generator.py
│
├── test_data/
│
├── utils/
│   └── logger.py
│
├── screenshots/
│
├── reports/
│
├── config.py
├── conftest.py
├── requirements.txt
└── README.md
```

---

#  Framework Components

## 1. Page Object Model

Application pages are represented using Page Object classes.

Example:


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.cart_title = ".title"
        self.cart_item_name = ".inventory_item_name"
        self.checkout_button = "[data-test='checkout']"
        self.continue_shopping_button = "[data-test='continue-shopping']"
        self.remove_backpack_button = "[data-test='remove-sauce-labs-backpack']"
```

The page object contains application-specific locators and actions.

---

# 2. BasePage

`BasePage` contains common browser actions such as:


click()
fill()
get_text()
is_visible()
wait_for()
get_url()
```

It also contains AI-assisted actions such as:


click_with_recovery()
fill_with_recovery()
```

This keeps the self-healing logic centralized instead of duplicating it in every page object.

---

#  AI Locator Recovery

The main purpose of the framework is to recover from locator failures.

Normally:


Test
 ↓
Page Object
 ↓
Locator
 ↓
Playwright
```

If the locator still exists:

```text
Click succeeds
```

If the locator fails:


Locator failure
      ↓
Load stored element profile
      ↓
Parse current DOM
      ↓
Extract candidate elements
      ↓
Generate candidate profiles
      ↓
Generate embeddings
      ↓
Calculate semantic similarity
      ↓
Select highest-scoring candidate
      ↓
Recover locator
      ↓
Retry action
```

---

# 🧠 Similarity Engine

The framework uses:

```text
SentenceTransformer
```

with:

```text
all-MiniLM-L6-v2
```

The model is loaded only once using a class-level instance:

```python
class SimilarityEngine:

    model = None

    def __init__(self):

        if SimilarityEngine.model is None:
            print("Loading AI model...")
            SimilarityEngine.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        self.model = SimilarityEngine.model
```

This avoids repeatedly loading the model whenever a locator recovery occurs.

---

# 🔎 Element Profiles

Each important UI element has a stored profile.

Example:

```json
{
  "checkout_button": {
    "locator": "#checkout",
    "tag": "button",
    "text": "Checkout",
    "role": "",
    "element_id": "checkout",
    "element_type": "",
    "aria_label": "",
    "placeholder": "",
    "css_class": "btn btn_action btn_medium checkout_button",
    "parent_tag": "div"
  }
}
```

The profile contains multiple characteristics rather than relying only on the locator.

This is important because the locator itself may become invalid.

The AI can use characteristics such as:

* Tag
* Role
* Element type
* ID
* Placeholder
* CSS class
* Parent tag
* Visible text

---

# 🗃️ JSON Profile Generation

Profiles do not need to be manually created.

The framework contains a DOM parser and profile generator.

Conceptually:

```text
Application Page
      ↓
DOMParser
      ↓
Extract DOM elements
      ↓
ElementProfile
      ↓
ProfileGenerator
      ↓
page_name.json
```

For example:

```text
profiles/
├── login_page.json
├── inventory_page.json
└── cart_page.json
```

A profile-generation test can navigate to the required page, parse the DOM and generate the corresponding JSON profile.

---

# 🔄 Recovery Example

Suppose the original locator is:

```python
self.checkout_button = "#checkout"
```

and the application changes it to:

```html
<button id="checkout-button">
    Checkout
</button>
```

The original locator:

```text
#checkout
```

fails.

Instead of immediately failing the test, the framework:

1. Loads the stored `checkout_button` profile.
2. Examines the current DOM.
3. Creates candidate profiles.
4. Calculates semantic similarity.
5. Selects the best candidate.
6. Retrieves its locator.
7. Performs the action using the recovered locator.

Example output:

```text
item_4_title_link -> 0.6658
 -> 0.5778
 -> 0.6079
 -> 0.5026

Recovered using #checkout with score 1.0
PASSED
```

The important point is that the recovery mechanism is based on the **element profile**, not simply a hard-coded alternative locator.

---

# 🧪 Test Execution

The framework uses Pytest.

Run all tests:

```bash
pytest
```

Run smoke tests:

```bash
pytest -m smoke
```

Run a specific test:

```bash
pytest tests/test_cart.py
```

Run a specific test function:

```bash
pytest tests/test_cart.py::test_add_backpack_to_cart
```

---

# 🌐 Multi-Browser Execution

The framework supports:

* Chromium
* Firefox
* WebKit

Browser selection is available through the command line.

### Chromium

```bash
pytest -m smoke --browser=chromium
```

### Firefox

```bash
pytest -m smoke --browser=firefox
```

### WebKit

```bash
pytest -m smoke --browser=webkit
```

This means the same test code can execute on different machines and different browsers without modifying the test cases.

---

# ⚙️ Environment Configuration

The framework supports environment selection.

Example:

```bash
pytest -m smoke --env=qa
```

The environment URL is configured through `config.py`.

This allows the same automation code to be used against different application environments.

---

# 📸 Failure Screenshots

When a test fails, the Pytest hook captures a screenshot.

Screenshots are stored under:

```text
screenshots/
```

Example:

```text
screenshots/
└── test_add_backpack_to_cart_20260819_120530.png
```

This helps investigate UI failures in CI environments.

---

# 📊 Test Reports

The framework generates an HTML report.

Example:

```text
reports/report.html
```

The report can be opened after test execution to inspect:

* Passed tests
* Failed tests
* Execution duration
* Test details
* Failure information

---

# 📝 Logging

Centralized logging is provided through:

```text
utils/logger.py
```

This avoids relying exclusively on `print()` statements and provides a consistent way of recording test execution information.

---

# 📦 Installation

## Prerequisites

Install:

* Python 3.x
* Git

Playwright manages its own browser binaries, so the required Playwright browsers can be installed using the Playwright command.

---

## Clone the repository

```bash
git clone https://github.com/sunildutt28/PlaywrightAutomate.git
```

Move into the project:

```bash
cd PlaywrightAutomate
```

---

## Create virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright browsers

```bash
python -m playwright install
```

---

# 🚀 Running the Framework

Example:

```bash
pytest -m smoke --browser=chromium
```

For Firefox:

```bash
pytest -m smoke --browser=firefox
```

For WebKit:

```bash
pytest -m smoke --browser=webkit
```

---

# 🔧 CI/CD with Jenkins

The project is integrated with Jenkins for Continuous Integration.

The current CI workflow is:

```text
Developer
   │
   │ git push
   ▼
GitHub
   │
   │ webhook
   ▼
Jenkins
   │
   ▼
Checkout latest code
   │
   ▼
Install dependencies
   │
   ▼
Run smoke tests
   │
   ▼
Generate test report
   │
   ▼
Build SUCCESS / FAILURE
```

The Jenkins job executes the smoke suite after a new change is pushed to GitHub.

---

# 🔗 GitHub Webhook

For local Jenkins development, the Jenkins server can be exposed through an ngrok tunnel.

Example:

```text
GitHub
   │
   │ HTTPS webhook
   ▼
ngrok
   │
   ▼
localhost:8080
   │
   ▼
Jenkins
```

The GitHub webhook endpoint is:

```text
/github-webhook/
```

The trailing endpoint is important.

Example:

```text
https://<ngrok-domain>/github-webhook/
```

---

# 🔐 Repository Security

The repository can be maintained as either public or private.

For a private repository, Jenkins requires appropriate GitHub credentials to clone the repository.

For a public repository, cloning does not require authentication, but write access remains controlled by GitHub repository permissions.

---

# 🖥️ Running on Another Machine

The framework is designed to be portable.

On another machine:

```bash
git clone <repository>
cd PlaywrightAutomate

python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

Then execute:

```bash
pytest -m smoke --browser=firefox
```

The same project can therefore run on another machine with a different supported browser.

---

# 🧪 Example Test

Example cart test:

```python
@pytest.mark.smoke
def test_add_backpack_to_cart(page, base_url):

    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)

    login.open(base_url)

    login.login("standard_user", "secret_sauce")

    inventory.verify_inventory_loaded()

    inventory.add_backpack_to_cart()

    assert inventory.get_cart_count() == "1"

    inventory.open_cart()

    cart.verify_cart_loaded()

    cart.verify_product_present("Sauce Labs Backpack")
```

The test follows the Page Object Model and keeps application-specific implementation out of the test itself.

---

# 🎯 Design Goals

The framework is designed to demonstrate how AI can complement traditional test automation.

Traditional automation:

```text
Locator changes
      ↓
Test fails
      ↓
Engineer updates locator
      ↓
Test passes
```

AI-assisted automation:

```text
Locator changes
      ↓
Original locator fails
      ↓
Analyze current DOM
      ↓
Compare element profiles
      ↓
Find best candidate
      ↓
Recover locator
      ↓
Retry action
```

The objective is not to eliminate deterministic automation, but to introduce a recovery layer for locator changes that can otherwise cause avoidable test failures.

---

# ⚠️ Current Limitations

The current implementation has several limitations:

* Locator recovery depends on the quality of the stored element profile.
* Semantic similarity does not guarantee that the recovered element is functionally correct.
* A similarity threshold should be introduced to prevent low-confidence recovery.
* Dynamic pages may produce many similar candidate elements.
* The current profile contains a limited set of DOM attributes.
* Recovery should be carefully validated for critical business actions.
* AI recovery should not silently hide genuine application defects.

For production use, recovery decisions should be logged and preferably reported separately from normal test execution.

---

# 🔮 Future Enhancements

Potential future improvements include:

### 1. Confidence threshold

Instead of recovering every candidate:

```text
score = 0.91
→ Recover

score = 0.48
→ Fail test
```

This prevents unsafe low-confidence healing.

### 2. Recovery logging

Record:

```text
Original locator
Recovered locator
Similarity score
Page
Element
Timestamp
```

### 3. Jenkins Pipeline as Code

Move Jenkins configuration into:

```text
Jenkinsfile
```

with stages such as:

```text
Checkout
   ↓
Install Dependencies
   ↓
Install Playwright
   ↓
Smoke Tests
   ↓
Publish Report
   ↓
Archive Screenshots
```

### 4. Cross-browser CI

Run:

```text
Chromium
Firefox
WebKit
```

as separate Jenkins stages or agents.

### 5. Parallel execution

Execute independent tests in parallel to reduce CI execution time.

### 6. Better candidate filtering

Filter candidates before semantic comparison using deterministic characteristics such as:

```text
Tag
Element type
Role
Visibility
Enabled state
```

This reduces unnecessary embedding calculations.

### 7. Embedding caching

Cache candidate embeddings where possible to reduce repeated model inference.

### 8. Pull Request validation

Configure Jenkins to execute smoke tests automatically for Pull Requests before merging into `main`.

---

# 🧭 Recommended CI/CD Evolution

The project can evolve from the current setup:

```text
GitHub
   ↓
Webhook
   ↓
Jenkins
   ↓
Smoke Tests
```

towards:

```text
                    GitHub
                       │
             Pull Request / Push
                       │
                       ▼
                    Jenkins
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          Smoke                Regression
             │                   │
             ▼                   ▼
         Chromium          Cross Browser
             │
             ▼
       Test Reports
             │
             ▼
       QA Environment
```

---

# 🏆 Project Highlights

This project demonstrates experience with:

* UI automation
* Playwright
* Python
* Pytest
* Page Object Model
* DOM parsing
* Semantic embeddings
* Sentence Transformers
* AI-assisted test automation
* Locator self-healing
* JSON-based test metadata
* Browser-independent execution
* Git/GitHub
* Jenkins
* CI/CD
* Webhooks
* Automated smoke testing
* Test reporting
* Failure diagnostics

---

# 📌 Project Status

**Current version:** `v1.0`

The current version demonstrates a working AI-assisted Playwright automation framework with locator recovery and Jenkins-based CI execution.

Future versions can extend the framework with stronger recovery confidence, improved candidate filtering, Pipeline as Code, cross-browser CI, and enhanced reporting.
