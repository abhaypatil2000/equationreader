from pdf2image import convert_from_path
import os
import glob


# folder_name/images is where all the converted images are saved
def convert_pdf_to_images(input_pdf, folder_name):
    # EAFP based method
    try:  # if folder already exists then exception occurs
        os.mkdir(f"./{folder_name}/images")
    except:  # else remove all the content in the folder
        for file in glob.glob(f"./{folder_name}/images/*"):
            os.remove(file)

    images = convert_from_path(f'./{folder_name}/{input_pdf}',
                               dpi=150)  # input pdf
    for i in range(len(images)):

        # Save pages as images in the pdf
        images[i].save(f'./{folder_name}/images/page' + str(i) + '.png', 'PNG')
    return len(images)