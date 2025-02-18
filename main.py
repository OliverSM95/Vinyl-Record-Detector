import matplotlib.pylab as plt

import src.google_search as gs
import src.image_processing as ip
import src.openCVFunctions as cvF
import src.site_scrape as ss
import cv2




#load photos
record_images = cvF.load_images_folder()
# Load an image from file
image = cvF.load_image(record_images,0)
#resize the image
image = cv2.resize(image,(750,750))

edge_image = cvF.edge_detector(image)

# Display the image
cv2.imshow('Image', image)
cv2.imshow("Edge Detector", edge_image)

gs.manual_reverse_image_search()





#-----------------loading images-----------------
print("----------------"+record_images[0]+"------------------")

#-----------------detect images----------------------#
# Step 1: Detect Labels

'''
detected_label = ip.detect_labels(record_images[0])
# Step 2: Detect Text (Better for albums)
album_text = ip.detect_text(record_images[0])
print(album_text)



# Step 3: Improve search query
if album_text:
    query = f"{album_text} vinyl album cover"
    print(f"1 Query: {query}")
elif "album" in detected_label.lower():

    query = f"{detected_label} vinyl record cover"
    print(f"2 Query: {query}")
else:
    query = f"{detected_label} music record"
    print(f"3 Query: {query}")

'''

#--------------Run functions---------------------
# Step 4: Search for relevant images



#scrape_site("https://teamstage.io/motivation-statistics/")
#google_image_search(query)
#google_image_search("Miles Davis Kind of Blue Vinyl Album Cover")
#gs.google_reverse_image_search(record_images[0])
gs.google_link_search("Best of Dean Martin Vinyl Record")





# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

