from pdf2image import convert_from_path
import os
import glob


# folder_name/images is where all the converted images are saved
def convert_pdf_to_images(input_pdf, folder_name, page_limit):
    # EAFP based method
    try:  # if folder already exists then exception occurs
        os.mkdir(f"./{folder_name}/images")
    except:  # else remove all the content in the folder
        for file in glob.glob(f"./{folder_name}/images/*"):
            os.remove(file)
    print(folder_name)
    print("pdf name:", input_pdf)
    images = convert_from_path(f'./{folder_name}/{input_pdf}',
                               dpi=200)  # input pdf
    processed_pages = min(len(images), page_limit)
    for i in range(processed_pages):

        # Save pages as images in the pdf
        images[i].save(f'./{folder_name}/images/page' + str(i) + '.png', 'PNG')

    return processed_pages