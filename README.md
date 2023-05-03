
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

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">python -m venv venv
</code></div></div></pre>

5. Activate the virtual environment:

* On Windows:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">venv\Scripts\activate
</code></div></div></pre>

* On macOS/Linux:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">source venv/bin/activate
</code></div></div></pre>

6. Install required Python libraries:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install -r requirements.txt
</code></div></div></pre>

*Note: The requirements.txt file is not shown, but it can be generated based on the libraries needed for the scripts.

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
