import os
import requests


IMAGES_DIR_NAME = "images"
SPACEX_LAST_LAUNCH_URL = "https://api.spacexdata.com/v3/launches/latest"


def create_images_folder(images_dir_name):
    if not os.path.exists(images_dir_name):
        try:
            os.makedirs(images_dir_name)
        except FileExistsError:
            pass
    return


def fetch_spacex_last_launch(images_dir_name, spacex_last_launch_url):
    image_name = "spacex{}.jpg"
    image_path = os.path.join(images_dir_name, image_name)

    last_launch_response = requests.get(spacex_last_launch_url)

    try:
        last_launch_images = last_launch_response.json()["links"]["flickr_images"]

        if len(last_launch_images) == 0:
            exit("Launch {} doesn't have images".format(spacex_last_launch_url))

        for image_number, image_link in enumerate(last_launch_images):
            image_response = requests.get(image_link)

            if image_response.ok:
                with open(image_path.format(image_number + 1), 'wb') as image_file:
                    image_file.write(image_response.content)
            else:
                print("Can't download image by url {}".format(image_link))
                continue

    except KeyError:
        exit("Can't download launch images by url {}".format(spacex_last_launch_url))


def main():
    create_images_folder(IMAGES_DIR_NAME)
    fetch_spacex_last_launch(IMAGES_DIR_NAME, SPACEX_LAST_LAUNCH_URL)


if __name__ == "__main__":
    main()
