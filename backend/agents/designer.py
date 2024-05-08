import os
from io import BytesIO
from PIL import Image
import requests
import numpy as np
from tavily import TavilyClient
import os

from backend.agents import SearchAgent

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

search_agent = SearchAgent()


class DesignerAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def load_html_template(self):
        relative_path = "../templates/index.html"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(dir_path, relative_path)
        with open(html_file_path) as f:
            html_template = f.read()
        return html_template

    def designer(self, email):
        html_template = self.load_html_template()
        # image = email["image"]
        content = email["email_content"]
        # html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{content}}", content)
        email["html"] = html_template
        return email

    def load_and_preprocess_image(self, image_url, target_height=50, background_color=(255, 255, 255)):
        response = requests.get(image_url, None)
        image = Image.open(BytesIO(response.content))
        image = image.convert('RGB')

        # Calculate new width to maintain aspect ratio
        aspect_ratio = image.width / image.height
        new_width = int(target_height * aspect_ratio)

        # Resize image to have the target height
        image = image.resize((new_width, target_height), Image.LANCZOS)

        # Create a new image with a white background and the target height
        final_image = Image.new('RGB', (new_width, target_height), background_color)

        # Calculate left position to center the image
        left = (final_image.width - image.width) // 2
        final_image.paste(image, (left, 0))  # Paste resized image onto white background
        # image_array = np.array(final_image) / 255.0  # Normalize to range [0, 1]
        return final_image #image_array

    # def combine_images(self, logo1, xmark, logo2):
    #     combined_image = np.concatenate([logo1, xmark, logo2], axis=1)
    #     return combined_image
    def combine_images(self, logo1, xmark, logo2):
        widths, height = logo1.width + xmark.width + logo2.width, logo1.height
        combined_image = Image.new('RGB', (widths, height))
        combined_image.paste(logo1, (0, 0))
        combined_image.paste(xmark, (logo1.width, 0))
        combined_image.paste(logo2, (logo1.width + xmark.width, 0))
        return combined_image

    def run(self, email: dict):
        html_template = self.load_html_template()

        # Generate composite image with the obtained logo URLs
        logo1_url = email['logo']  # our logo
        logo2_url = email['image']  # target logo
        xmark_url = ('https://images.squarespace-cdn.com/content/v1/55ece940e4b048d1ed401c11/1450136257542-4DATU4KR'
                     'B70MDENGJXJX/X%3A++The+Unknown')  # xmark image

        if logo1_url and logo2_url:
            # print('Merging images..')
            logo1 = self.load_and_preprocess_image(logo1_url)
            xmark = self.load_and_preprocess_image(xmark_url)
            logo2 = self.load_and_preprocess_image(logo2_url)

            composite_image = self.combine_images(logo1, xmark, logo2)
            image_filename = f'composite_{email["title"].replace(" ", "_")}.png'
            composite_image_path = os.path.join(self.output_dir, image_filename)
            composite_image.save(composite_image_path)
            # print(self.output_dir)
            # Image URL is saved in email dictionary
            email['merged_logos'] = f'{composite_image_path.replace('frontend/static/', '')}'
            # print(email['merged_logos'])

        # Update the HTML with the new image
        content = email["email_content"]
        # print(content)
        html_template = html_template.replace("{{content}}", content)
        # print(html_template)

        # Write the HTML to a file
        output_html_path = os.path.join(self.output_dir, 'email.html')
        with open(output_html_path, 'w') as f:
            f.write(html_template)

        # Return the path to the HTML file or the HTML content itself
        return email
