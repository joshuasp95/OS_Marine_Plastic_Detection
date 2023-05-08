# Sentinel-2 Plastic Detection Tools

This repository contains tools and resources for performing atmospheric correction and generating applicable indices for detecting plastic at marine/coastal environments from Sentinel-2 satellite images. The primary scripts process the images using the Sen2Cor and Acolite tools and Python libraries.

## Important

Once the sen2cor script has been applied to the
sentinel-2 image you can't use the acolite script
to process the same image, you must unzip
the original .SAFE file again.

Besides, I noticed when I tried to run the main script in a Linux environment(Ubuntu 22.04, 16gb RAM) that the system collapsed due to the high consumption of resources, so I recommend to use
windows or run the main script in a system which has over 32GB of RAM.

You can also run each script individually if something goes wrong or if you only want process/correction for a image/.tif file.

There are 4 main scripts that I consider useful: acolite_script.py, which can process a batch of Sentinel-2 scenes, and sen2cor_script.py, which does the same, calculate_indices.py which calculates the indices for plastic detection and their thresholds to detect pixels which may contain plastics and the main script that is a combination of the other scripts.

## Features

- Atmospheric correction using the Sen2Cor and Acolite tools
- Different index generation for plastic detection
- Processing of Sentinel-2 satellite images in .SAFE format
- Exporting processed images as GeoTIFF files

## Requirements

- Python 3.x
- Sen2Cor 2.11.0 or later
- Acolite
- Libraries: GDAL, rasterio, numpy...

I had some problems with the GDAL installation. These websites helped me a lot: [lfd.uci.edu](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and [opensourceoptions.com](https://opensourceoptions.com/blog/how-to-install-gdal-for-python-with-pip-on-windows/). There you can find the Windows installers for some needed libraries.

## Installation

1. Download and install the Sen2Cor tool from the official website ([https://step.esa.int/main/third-party-plugins-2/sen2cor/](https://step.esa.int/main/third-party-plugins-2/sen2cor/)).
2. Download and set up Acolite ([https://odnature.naturalsciences.be/remsem/software-and-data/acolite](https://odnature.naturalsciences.be/remsem/software-and-data/acolite)).
3. Clone this repository or download it as a ZIP file.
4. Create a virtual environment:

```
python -m venv venv
```

5. Activate the virtual environment:

- On Windows:

```
venv\Scripts\activate.bat
```

- On macOS/Linux:

```
source venv/bin/activate
```

6. Install required Python libraries:

```
pip install -r requirements.txt
```

## Usage

1. Place your Sentinel-2 satellite images in a directory.
2. Update the `sen2cor` variable in the `sen2cor_script.py` script to point to your Sen2Cor executable file. (the .bat file)
3. Update the Acolite path in the `acolite_script.py` script (replace the example path with the path to your Acolite folder; e.g: "C:\Git\acolite").
4. Run the scripts using Python:

```
python sen2cor_script.py
```

```
python acolite_script.py
```

5. Enter the directory containing the .SAFE files and the output directory when prompted.

The scripts will process the Sentinel-2 images using Sen2Cor and Acolite, generate output files containing atmospheric-corrected images.

## Acknowledgements

I would like to express my gratitude to everyone who has contributed to the success of this project. Your valuable resources, code, and scientific articles have been instrumental in shaping the development of this repository.

- [Open Source Options](https://opensourceoptions.com/) - for their informative website
- [Cole Krehbiel](https://github.com/ckrehbiel) - for the open-source code they provided on GitHub
- [PLP Aegean](https://plp.aegean.gr/) - for their scientific articles and plastic litter projects which made this project possible

Thank you all for your support and contributions. Your knowledge and expertise have truly made a difference in this project.

## Contributing

Please feel free to open issues, submit pull requests, or provide feedback to improve this repository. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
