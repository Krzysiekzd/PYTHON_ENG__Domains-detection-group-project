# Overview  
The goal of the project was to create an algorithm for detecting TADs in the Hi-C data with the best precision possible.  
TADs (Topologically Associating Domains) are self-interacting genomic regions and detecting them is crucial for further development of research on the complex chromatin structure. Our initial goal was simple. We decided to analyze two different algorithms in more depth and possibly modify them. The final result was modified version of a TopDom algorithm, with additional *sensitivity* parameter that allows specifing how precisely TADs are detected.  
Short summary can be found in **digest.pdf** file and longer description in **summary_record.pdf**. This project was part of the 4EU+ Alliance.  
This repository was copied from: https://github.com/meet-eu-21/Team-WA1  
*Note: due to some technical issues I did not make many commits to the original repository. However, my code was commited by other team members.*  
This project was created in cooperation with Leszek Troc (https://github.com/Lechuuu000), Sebastian Kot (https://github.com/kot-sebastian) and Ignacy Makowski (https://github.com/Ilidan).  
   
   
   
   
# Team-WA1

Meet-EU Team WA1

Topic A : Prediction of TADs

## How to download repo? (Linux / MacOS)
1. Create GitHub account
2. Provide email to get access.
3. Create ssh key
* `cd /home/my-user/.ssh`
* `ssh-keygen -t rsa -b 4096`
* provide name and optional password
* `cat <given-name>.pub`
* copy retrieved
* GitHub settings
* SSH and GCP keys tab
* add ssh key
* type any name
* paste result of `cat`-a
* navigate to terminal
* `ssh -T git@github.com -i ~/.ssh/<given-name>`
* now I can:
* `git clone git@github.com:<scope-user>/<project-name>.git`, in our case `git clone git@github.com:meet-eu-21/Team-WA1.git`

## Data description:
1. HiC - data to our algorithms
2. TAD - additional metadata + results

## Downloading data:
1. All (approx. 25 gb) - `./scripts/download_all.sh`
2. Only GM12878 (approx. 11 gb) - `./scripts/download_GM12878.sh`

## Run:
1. install `python3`
2. install required packages
3. download and unpack data (can use scripts directory)
4. in src directory `python3 main.py {args}` (available args and their behaviour can be found in `summary_report.pdf`)
* example: `python3 main.py--results-path=../results --resolution=100k --data-path=../data/www.lcqb.upmc.fr/meetu/dataforstudent/HiC/GM12878/100kb_resolution_intrachromosomal --run-topdom=True --with-metrics-results=True --with-results-coordinates=True --topdom-sensitivity=0.04 --topdom-window-size=5 --chromosomes=1,22,X`

## Results:
1. Results should be available in `{desired directory}/topdom` / `{desired directory}/arrowhead` directory
2. Remember to change resolution if you change data

