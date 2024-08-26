<!-- PROJECT TITLE -->
<h1 align="center">WatsMyTax</h1>
<div id="header" align="center">
</div>
<h2 align="center">
 Description
</h2>
<p align="center"><strong>Introducing WatsMyTax:</strong>
   WatsMyTax is a powerful tax optimization tool designed to help individuals maximize their tax savings by providing personalized strategies based on their financial information. With an intuitive user interface, WatsMyTax simplifies the process of optimizing tax liability, making it accessible to users across various financial backgrounds.</p>

## Table of Contents

<details>
<summary>WatsMyTax</summary>

- [Application Description](#application-description)
- [Try the App](#try-the-app)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Using Docker](#using-docker)
  - [Deploying with Kubernetes](#deploying-with-kubernetes)
  - [Continuous Integration with SonarQube](#continuous-integration-with-sonarqube)
- [Authors](#authors)
- [License](#license)

</details>

## Try the App

You can try the deployed app here: [WatsMyTax](https://aitaxoptimizer.streamlit.app/)

## Technology Stack

| Technology   | Description                                      |
| ------------ | ------------------------------------------------ |
| Streamlit    | Open-source app framework for data science       |
| Python       | Programming language used for backend processing |
| Pandas       | Data manipulation and analysis library           |
| NumPy        | Fundamental package for scientific computing     |
| HTML/CSS     | For structuring and styling the app's interface   |
| Docker       | A platform designed to help developers build, share, and run container applications.    |
| Kubernetes   | An open-source container orchestration system for automating software deployment   |
| SonarQube    | An open-source platform for continuous inspection of code quality.   |

## Features

- **Personalized Tax-Saving Strategy**:<br> WatsMyTax generates tailored tax-saving strategies based on user input, optimizing tax liability.
- **User-Friendly Interface**:<br> Input fields allow users to easily provide information such as earnings, tax rates, and investments, making tax optimization accessible.
- **Real-Time Feedback**:<br> The app offers immediate feedback and recommendations to help users maximize their tax savings.
- **Cross-Platform Compatibility**:<br> WatsMyTax is designed to work seamlessly across different devices, ensuring accessibility and ease of use.

## Usage

### Running Locally

To run the app locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/WatsMyTax.git
   cd WatsMyTax

2. **Install dependencies:**
Make sure you have Python 3.9 installed. Then install the required Python packages:

 ```bash
  pip install -r requirements.txt

3. **Install dependencies:**
Make sure you have Python 3.9 installed. Then install the required Python packages:

 ```bash
 pip install -r requirements.txt

### Using Docker

To run the app using Docker, follow these steps:

1. **Build the Docker image**

```bash
 docker build -t watsai:latest .

2. **Run the Docker container:**

```bash
 docker run -p 8501:8501 watsmytax:latest

### Deploying with Kubernetes

1. **Ensure you have a Kubernetes cluster available.**

2. **Apply the Kubernetes manifests:**

```bash
 kubectl apply -f k8s/deployment.yaml
 kubectl apply -f k8s/service.yaml

## Authors

| Name               | Link                                      |
| ------------------ | ----------------------------------------- |
| Sandra Ashipala     | [GitHub](https://github.com/sandramsc) |
| Hoang Nguyen Van | [GitHub](https://github.com/hoangnv170752) |
| Prasad Khare | [GitHub](https://github.com/pakhare) |
| Yash Thakre | [GitHub](https://github.com/yash9904) |

## License

[![GitLicense](https://img.shields.io/badge/License-Apache-lime.svg)](https://github.com/pakhare/WatsMyTax/blob/main/LICENSE)
