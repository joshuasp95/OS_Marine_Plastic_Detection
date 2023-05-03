# Sentinel-2 Plastic Detection Tools

This repository contains tools and resources for performing atmospheric correction and generating applicable indices for detecting plastic from Sentinel-2 satellite images. The primary scripts process the images using the Sen2Cor and Acolite tools and Python libraries.

## Features

- Atmospheric correction using the Sen2Cor and Acolite tools
- Different index generation for plastic detection
- Processing of Sentinel-2 satellite images in .SAFE format
- Exporting processed images as GeoTIFF files

## Requirements

- Python 3.x
- Sen2Cor 2.11.0 or later
- Acolite
- Libraries: os, re, and subprocess (additional libraries required for Acolite)

## Installation

1. Download and install the Sen2Cor tool from the official website ([https://step.esa.int/main/third-party-plugins-2/sen2cor/](https://step.esa.int/main/third-party-plugins-2/sen2cor/)).
2. Download and set up Acolite ([https://odnature.naturalsciences.be/remsem/software-and-data/acolite](https://odnature.naturalsciences.be/remsem/software-and-data/acolite)).
3. Clone this repository or download it as a ZIP file.
4. Create a virtual environment:

```
python -m venv venv
`` `

5. Activate the virtual environment:

- On Windows:

```
sh venv\Scripts\activate
```

- On macOS/Linux:

```
source venv/bin/activate
```

6. Install required Python libraries:

```
pip install -r requirements.txt
```

\*Note: The requirements.txt file is not shown, but it can be generated based on the libraries needed for the scripts.

## Usage

1. Place your Sentinel-2 satellite images in a directory.
2. Update the `sen2cor` variable in the `sen2cor_script.py` script to point to your Sen2Cor executable file.
3. Update the Acolite path in the `acolite_script.py` script (replace the example path with the path to your Acolite folder).
4. Run the scripts using Python:

```
python sen2cor_script.py
```

```
python acolite_script.py
```

5. Enter the directory containing the .SAFE files and the output directory when prompted.

The scripts will process the Sentinel-2 images using Sen2Cor and Acolite, generate output files containing atmospheric-corrected images, and calculate indices for plastic detection.

## Contributing

Please feel free to open issues, submit pull requests, or provide feedback to improve this repository. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
