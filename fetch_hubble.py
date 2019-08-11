import os
import requests


IMAGES_DIR_NAME = "images"
HUBBLE_IMAGE_URL = "http://hubblesite.org/api/v3/image/{}"
HUBBLE_COLLECTION_URL = "http://hubblesite.org/api/v3/images/news"


def get_file_extension(url):
    file_extension = url.split(".")[-1]
    return file_extension


def fetch_hubble_images(hubble_image_url, images_dir_name, image_id):
    image_info_response = requests.get(hubble_image_url.format(image_id))

    if not image_info_response.ok:
        return None

    try:
        image_files = image_info_response.json()["image_files"]

        best_quality_image_file = image_files[-1]
        image_url_for_download = "https:" + best_quality_image_file["file_url"]
        image_extension = get_file_extension(image_url_for_download)
        image_name_for_saving = str(image_id) + "." + image_extension
        image_path = os.path.join(images_dir_name, image_name_for_saving)

        image_response = requests.get(image_url_for_download, verify=False)

        if not image_response.ok:
            return None

        if image_response.text == "{}":  # {} возвращается при несуществующем id фото
            return None

        with open(image_path, 'wb') as image_file:
            return image_file.write(image_response.content)

    except KeyError:
        return None


def download_from_collection(collection_url):
    collection_images_response = requests.get(collection_url)

    if not collection_images_response.ok:
        return None

    try:
        collection_images_list = collection_images_response.json()

        if len(collection_images_list) == 0:  # получаем [] если в коллекции нет фото или нет такого названия коллекции
            return None

        collection_images_ids = [image["id"] for image in collection_images_list]
        return collection_images_ids

    except ValueError:
        return None


def main():
    os.makedirs(IMAGES_DIR_NAME, exist_ok=True)

    collection_images_ids = download_from_collection(HUBBLE_COLLECTION_URL)

    if collection_images_ids is None:
        exit("Collection {} is empty, doesn't exist or error was occurred while downloading".format(HUBBLE_COLLECTION_URL))

    for image_id in collection_images_ids:
        print("=" * 5 + " Image {} in process...".format(image_id))

        if fetch_hubble_images(HUBBLE_IMAGE_URL, IMAGES_DIR_NAME, image_id) is None:
            print("Can't download image with image_id={}".format(image_id))
            print("=" * 5 + " Failed!")
            continue

        print("=" * 5 + " Done!")

    print("*" * 5 + " All images from the collection {} were processed! ".format(HUBBLE_COLLECTION_URL) + "*" * 5)


if __name__ == "__main__":
    main()
