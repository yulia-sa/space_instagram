import os
from instabot import Bot
from dotenv import load_dotenv


load_dotenv()

IMAGES_DIR_NAME = "images"
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
FILES_TYPES_FOR_UPLOAD = ('.jpg', '.png')


def get_images_list(path):
    files = os.listdir(path=path)
    images = list(filter(lambda x: x.endswith(FILES_TYPES_FOR_UPLOAD), files))
    return images


def upload_image_to_instagram(bot, image_path):
    bot.upload_photo(image_path)
    return


def main():
    bot = Bot()
    bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

    images_for_upload = get_images_list(IMAGES_DIR_NAME)

    for image_name in images_for_upload:
        image_path = os.path.join(IMAGES_DIR_NAME, image_name)
        upload_image_to_instagram(bot, image_path)


if __name__ == "__main__":
    main()
