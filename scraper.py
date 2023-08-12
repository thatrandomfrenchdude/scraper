import os
import json
import requests
from bs4 import BeautifulSoup


class Scraper():
    def __init__(self, url) -> None:
        self.target = url

    def validate_url(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid URL or connection error: {e}")


    def extract_text_content(self, element):
        # Extract visible text content from an HTML element
        if element.string:
            return element.string.strip()
        else:
            return " ".join([self.extract_text_content(child) for child in element.children if child.name != "script"])


    def convert_to_json(self, element):
        # Convert the HTML element and its children to a JSON representation
        json_data = {
            "tag": element.name,
            "text": self.extract_text_content(element),
            "children": []
        }
        for child in element.children:
            if child.name != "script":
                json_data["children"].append(self.convert_to_json(child))
        return json_data


    def save_json_output(self, data, output_directory, filename):
        output_file = os.path.join(output_directory, f"{filename}.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"JSON output saved to: {output_file}")


    def scrape(self, output_directory):
        try:
            self.validate_url(self.url)
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, "html.parser")
            website_name = self.url.split("//")[1].split("/")[0].replace(".", "_").replace("-", "_")
            json_data = self.convert_to_json(soup)
            self.save_json_output(json_data, output_directory, website_name)
        except ValueError as e:
            print(f"Error: {e}")
