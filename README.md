# Product Trend Analysis Tool

## Description
This tool is designed to assist users in identifying trending products based on specific markets, niches, or user-defined guidelines. It leverages OpenAI's GPT-3 to generate product ideas, retrieves Google Trends data for these products, and performs analysis and visualization on this data. The results can help users make informed decisions on product selection and market trends.

## Features
- **Product Idea Generation**: Generates product ideas based on user input or guidelines.
- **Google Trends Analysis**: Retrieves and analyzes Google Trends data for the generated products.
- **Data Visualization**: Provides visual representation of product interest over time.
- **In-Memory Database**: Utilizes an SQLite in-memory database for temporary data storage and retrieval.
- **User Interaction**: Allows users to input their own product markets, niches, or guidelines.

## Requirements
This tool requires Python 3.6 or later. All required libraries and dependencies are listed in the `requirements.txt` file. Additionally, users need to have access to OpenAI's GPT-3 API and Google Trends API, and must securely handle the respective API keys.

## Setup and Installation
1. Clone this repository to your local machine.
2. Install the required libraries using the command: `pip install -r requirements.txt`
3. Set up your OpenAI GPT-3 API key and other required credentials.

## Usage
1. Run the script using the command: `python product_trend_analysis.py`
2. Follow the on-screen prompts to input your product market, niche, or guideline.
3. The tool will generate product ideas, retrieve Google Trends data, and provide visualizations and analysis results.

## Disclaimer
This tool is provided "as is" without any warranty of any kind, either expressed or implied. The user assumes the entire risk as to the quality and performance of the software. The authors are not liable for any direct, indirect, incidental, special, exemplary, or consequential damages that may result from the use or inability to use the software.

## License
This project is open source and available under the [MIT License](LICENSE).

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact
For any inquiries or issues, please open an issue on the GitHub repository.
