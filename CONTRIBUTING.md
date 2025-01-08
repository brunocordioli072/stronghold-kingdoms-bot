# Stronghold Kingdoms Bot Contributing Guide

Hi! We're really excited that you're interested in contributing to Stronghold Kingdoms Bot! Before submitting your contribution, please read through the following.

## Repo Setup

To develop locally, fork the Stronghold Kingdoms Bot repository and clone it in your local machine. You will need Node.js 18+ and Python 3.4+.

To develop and test the Stronghold Kingdoms Bot:

1. Follow the [Getting Started](https://github.com/brunocordioli072/stronghold-kingdoms-bot?tab=readme-ov-file#getting-started) of README to install all dependencies.
2. To use the bot, run `make run` on the root folder of the `stronghold-kingdoms-bot` with the Stronghold Kingdoms app open on Emulator.

## Observations

- To add new templates, use the processed_image.png output when the program is running. Its a screenshot of how the opencv sees the screen. Use Windows Photos to get the correct resolution of the photo and take a screenshot of the template you want to use. After that put it in the /stronghold-kingdoms-bot/stronghold-kingdoms-bot/templates. After that add the new template on the template_service.py.

## Pull Request Guidelines

- Checkout a topic branch from a base branch (e.g. `main`), and merge back against that branch.

- If adding a new feature:

  - Add accompanying test case.
  - Provide a convincing reason to add this feature. Ideally, you should open a suggestion issue first, and have it approved before working on it.

- If fixing a bug:

  - If you are resolving a special issue, add `(fix #xxxx[,#xxxx])` (#xxxx is the issue id) in your PR title for a better release log (e.g. `fix: update entities encoding/decoding (fix #3899)`).
  - Provide a detailed description of the bug in the PR. Live demo preferred.

- It's OK to have multiple small commits as you work on the PR. GitHub can automatically squash them before merging.