import os
import shutil
import genanki

# Create model for anki images
my_model = genanki.Model(
  1607392319,
  'Derm Image',
  fields=[
    {'name': 'Image'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Image}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

# Create deck
deck = genanki.Deck(
  2059400110,
  'Derm Deck')
# Create package for the deck
derm_package = genanki.Package(deck)

# Get the list of all subdirectories inside the images folder
subdirs = [d for d in os.listdir('images') if os.path.isdir(os.path.join('images', d))]

# Loop through each subdirectory and get the list of image files in it
images = []
for subdir in subdirs:
    image_files = [f for f in os.listdir(os.path.join('images', subdir)) if os.path.isfile(os.path.join('images', subdir, f))]
    for image_file in image_files:
        images.append((subdir, image_file))

# Copy all the image files to the main directory because anki doesn't like when they are in a folder
for subdir, image_file in images:
    src_path = os.path.join('images', subdir, image_file)
    dst_path = os.path.join('.', image_file)
    shutil.copy(src_path, dst_path)

# Add cards to the deck based on folder they are in
for image in images:
    card_note = genanki.Note(
        model=my_model,
        fields=['<img src="' + image[1] + '">', image[0]])
    deck.add_note(card_note)
    derm_package.media_files.append(image[1])

# Write package file
derm_package.write_to_file('Derm_Deck.apkg')

# Delete all the silly copied image files
for subdir, image_file in images:
    dst_path = os.path.join('.', image_file)
    os.remove(dst_path)