import os
import requests


IMAGES_DIR_NAME = "images"
HUBBLE_IMAGE_URL = "http://hubblesite.org/api/v3/image/{}"
HUBBLE_COLLECTION_URL = "http://hubblesite.org/api/v3/images/stsci_gallery"


def get_file_extension(url):
    file_extension = url.split(".")[-1]
    return file_extension


def fetch_hubble_images(hubble_image_url, images_dir_name, image_id):
    image_info_response = requests.get(hubble_image_url.format(image_id))

    try:
        image_files = image_info_response.json()["image_files"]

        best_quality_image_file = image_files[-1]
        image_url_for_download = "https:" + best_quality_image_file["file_url"]
        image_extension = get_file_extension(image_url_for_download)
        image_name_for_saving = str(image_id) + "." + image_extension
        image_path = os.path.join(images_dir_name, image_name_for_saving)

        image_response = requests.get(image_url_for_download, verify=False)

        if image_response.ok:
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
        else:
            return print("Can't download image with image_id={} by url {}".format(
                                                                            image_id,
                                                                            image_url_for_download))
    except KeyError:
        exit("Photos for image_id={} don't exist".format(image_id))


def download_from_collection(collection_url):
    collection_images_response = requests.get(collection_url)

    if len(collection_images_response.json()) == 0:
        exit("Collection {} is empty".format(collection_url))

    collection_images = []
    for image in collection_images_response.json():
        image_id = image["id"]
        collection_images.append(image_id)

    return collection_images


def main():
    os.makedirs(IMAGES_DIR_NAME, exist_ok=True)

    collection_images = download_from_collection(HUBBLE_COLLECTION_URL)

    for image_id in collection_images:
        print("=" * 5 + " Image {} in process...".format(image_id))
        fetch_hubble_images(HUBBLE_IMAGE_URL, IMAGES_DIR_NAME, image_id)
        print("=" * 5 + " Done!")

    print("*" * 5 + " All images from the collection {} were processed! ".format(HUBBLE_COLLECTION_URL) + "*" * 5)


if __name__ == "__main__":
    main()
