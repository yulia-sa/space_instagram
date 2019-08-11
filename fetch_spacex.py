import os
import requests


IMAGES_DIR_NAME = "images"
SPACEX_LAST_LAUNCH_URL = "https://api.spacexdata.com/v3/launches/latest"


def fetch_spacex_last_launch(images_dir_name, spacex_last_launch_url):
    image_name = "spacex{}.jpg"
    image_path = os.path.join(images_dir_name, image_name)

    last_launch_response = requests.get(spacex_last_launch_url)

    if not last_launch_response.ok:
        return None

    try:
        last_launch_images = last_launch_response.json()["links"]["flickr_images"]

        if len(last_launch_images) == 0:
            return None

        for image_number, image_link in enumerate(last_launch_images):
            image_response = requests.get(image_link)

            if not image_response.ok:
                continue

            with open(image_path.format(image_number + 1), 'wb') as image_file:
                image_file.write(image_response.content)

        return True

    except ValueError:
        return None

    except KeyError:
        return None


def main():
    os.makedirs(IMAGES_DIR_NAME, exist_ok=True)

    if fetch_spacex_last_launch(IMAGES_DIR_NAME, SPACEX_LAST_LAUNCH_URL) is None:
        exit("Last launch {} doesn't have images or error was occurred while downloading".format(SPACEX_LAST_LAUNCH_URL))


if __name__ == "__main__":
    main()
