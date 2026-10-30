# WaterTAP Academy Installation Guide

This guide will step through the processes to get started with the WaterTAP Academy. Accessing the content for the WaterTAP Academy will require that you have (1) an Integrated Development Environment (IDE) to write and run Python code - we will be using Microsoft's [VSCode](https://code.visualstudio.com/) but other IDEs are available, (2) Python and WaterTAP installed on your local machine, and (3) the graphical user interface (GUI) to run and visualize flowsheets outside of Python. Likewise, this installation guide will be broken down into the following parts:

- **Part 1: Installing Miniforge**
  - Installing Miniforge

- **Part 2: Installing Miniforge, Python, and WaterTAP**
    - Installing VSCode
    - Installing VSCode extensions
    - Creating the conda environment
    - Cloning the WaterTAP Academy repo
    - Installing WaterTAP
    - Setting up Jupyter Lab
    - Installing Reaktoro

- **Part 3: Installing the IDAES Flowsheet Processor (Graphical User Interface)**

- **Part 4: Optional Steps**
  - Creating a GitHub account

Alternatively, [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/watertap-org/watertap_academy_2026/main) can be used to access WaterTAP Academy materials through a web browser without having to install anything. Binder is an online service providing a short-lived temporary sandbox environment on public cloud resources where Jupyter notebooks can be run, free of charge, without having to install any software locally.

## Part 1: Installing Miniforge

### 1. Install Miniforge

Miniforge is a tool for managing Python packages and environments. Download Miniforge for your system from this [website](https://conda-forge.org/download/). The "latest" version is recommended.

> [!NOTE]  
> Take note of where Miniforge is being installed. For most users, it will default to a folder named miniforge3
> within the C:\Users\YourUsername directory. **If it defaults to C:\Users\YourUsername\AppData\Local,
> move the installation inside of C:\Users\YourUsername to avoid potential issues with the file path length.

![Miniforge Download](https://github.com/user-attachments/assets/83b467f9-c2d6-499f-97ce-1cf00e31d32e)

Run the downloaded installer to start the guided installation process. When prompted to choose options, it is OK to use the default (i.e. already selected) value(s).

> [!NOTE]  
> Be sure to install for "Just Me (recommended)" as opposed to "All Users (requires admin privileges)".
  
![Miniforge Install](https://github.com/user-attachments/assets/f021af65-4cc0-429f-a8a7-b05987dbaca6)

## Part 2: Installing VSCode, Python, and WaterTAP

VSCode is the free Microsoft integrated development environment (IDE) we will be using for the WaterTAP Academy. In addition to installing the VSCode application, we need to install the Python and GitHub extensions. For an introductory tutorial on VSCode, visit their official [Getting Started](https://code.visualstudio.com/docs/getstarted/getting-started) page.

### 2. [Download the VSCode installer](https://code.visualstudio.com/download) for your operating system and install VSCode.


### 3. Create WaterTAP Academy Directory

In File Explorer, create a folder where you'd like to store all of your WaterTAP Academy content. Let's create a folder called watertap_academy and store it under Users/your_username.
![img.png](img.png)

### 4. Open VSCode. 

On the left side of the application is the Activity Bar:

<img width="280" height="328" alt="Screenshot 2025-10-17 at 2 31 13 PM" src="https://github.com/user-attachments/assets/f9f727e2-805b-47c8-893b-b69b8723a36e" />

Click the icon with four squares <img width="55" height="50" alt="Screenshot 2025-10-17 at 2 43 34 PM" src="https://github.com/user-attachments/assets/6c69ba9a-9bf5-4ff3-a16e-f3a112f1bc72" /> to open the Extension browser:

<img width="315" height="337" alt="Screenshot 2025-10-17 at 2 45 19 PM" src="https://github.com/user-attachments/assets/854b5203-eb28-4888-87ea-f0b3b8225b72" />

### 5. Install extensions

VSCode extensions are add-ons that allow users to customize their workflow by integrating additional capabilities. Follow the instructions [here](https://code.visualstudio.com/docs/getstarted/extensions) to find and install the Python and Jupyter extensions. To be sure you install the right extensions, paste the following Extension IDs into the search bar: ms-python.python and ms-toolsai.jupyter.

<img width="581" height="83" alt="Python Extension badge" src="https://github.com/user-attachments/assets/193979fc-90d8-44d8-8120-903d66d07313" />

<img width="574" height="85" alt="Jupyter Extension badge" src="https://github.com/user-attachments/assets/c19cbeb9-421b-4c16-9206-02e9366d83cb" />

### 6. Open the watertap-academy folder
Under the Explorer, click "Open Folder" and navigate to the path where you stored the watertap_academy folder. This will be empty for now, but as the course progresses, we'll gradually populate it with material.

![img_3.png](img_3.png)

### 7. Open a terminal window

Open a Miniforge terminal window in VSCode by clicking the dropdown arrow in the terminal and selecting "Miniforge". If the terminal is not already open, click on "Terminal" in the top banner and select "New Terminal".
![img_1.png](img_1.png)

### 8. Create the Conda environment

At the terminal prompt, run the following command to create the Conda environment:

```sh
conda create --yes --name watertap-academy -c conda-forge python=3.12 git
```

> [!NOTE]  
> If you encounter a "the term conda is not recognized" error, try running `conda init --all` in the Miniforge terminal. If this does not resolve the issue, open VSCode, press **Ctrl + Shift + P**, type **"Preferences: Open Settings (JSON)"** or **"Preferences: Open User Settings (JSON)"** into the command palette at the top of the screen, and then insert the following into the dictionary. The following code assumes Miniforge is installed under your %USERPROFILE% (C:\Users\YourUsername). The safest choice is to open a "Command Prompt" terminal in VSCode; "Powershell" terminals can be problematic.
> 
> ```json
> {
>     "terminal.integrated.profiles.windows": {
>         "Miniforge": {
>             "path": "C:\\Windows\\System32\\cmd.exe",
>             "args": ["/K", "%USERPROFILE%\\miniforge3\\Scripts\\activate.bat"]
>         }
>     },
>     "terminal.integrated.defaultProfile.windows": "Miniforge"
> }
> ```

### 9. Activate the Conda environment

Run the following command to activate the newly created `watertap-academy` environment:

```
conda activate watertap-academy
```

The name of the active environment should be shown at the bottom left before the prompt:

![img_2.png](img_2.png)

> [!NOTE]
> The environment will need to be reactivated every time you need to open another terminal window.

### 10. Install WaterTAP 
Now we'll install the WaterTAP codebase. 

In the terminal, run the following cell to install WaterTAP inside your "watertap-academy" environment:

```
pip install watertap
```

### 11. Install the IDAES solvers

Run the following command to install the IDAES solvers:

```
idaes get-extensions --verbose
```


### 12. Install the Jupyter dependencies

Run the following command to install the dependencies needed to run notebooks:

```
pip install "watertap[notebooks]"
```

### 13. Register the WaterTAP Academy conda environment with Jupyter

Run the following command to configure Jupyter to recognize the current WaterTAP environment:

```
python -m ipykernel install --user --name watertap-academy
```


### 14. Start the Jupyter server

Run the following command to start the Jupyter server from the current directory, specifying the introductory tutorial as the starting notebook:
    
```
jupyter lab [insert name of a notebook - they will need to add to this folder first]
```


### 15. Test the installation

As a way to quickly test if the installation process above was successful, you can run the `[insert name of notebook]` notebook automatically (i.e. not interactively). To do so, select `Kernel > Restart Kernel and Run All Cells` from the menu bar.

![Restart Kernel](https://github.com/user-attachments/assets/280b4c6d-f9c2-4818-91ee-f0f618a94fc6)

- The notebook should take a few minutes to finish running
- While running, the kernel indicator near the top-right corner will become "busy" (solid gray circle); when finished, it will switch back to the "idle" state (white with gray border)
- If there are no errors, all the cells of the notebooks should be populated with various outputs
- If there are errors, error messages (typically in red color) will be shown instead
- To "reset" the notebook to the initial empty state and run it again, select `Kernel > Restart Kernel and Run All Cells` from the menu bar


### 16. Select the WaterTAP kernel to use to run the notebook

In the "Select Kernel" pop-up menu, select the `watertap-academy` entry (which corresponds to the registration command in Step 8).

![Select Kernel](https://github.com/user-attachments/assets/5c060bbf-fdef-4a9a-aff4-7b5634ebc499)

> [!NOTE]
> You might have to repeat this selection and/or ensure that the `wta26` kernel is being used when launching (opening) other notebooks. The current kernel selection can be seen in the top-right corner of the notebook page.


### 17. Install Reaktoro

Run the following commands to install Reaktoro, which is a tool that enables detailed chemistry integration. This will be necessary to run the tutorials for the Week 8 lecture. If prompted with "Proceed ([y]/n)?", type the letter y.

```
conda install -c conda-forge reaktoro=2.13.0 cyipopt=1.7.0
pip install git+https://github.com/watertap-org/reaktoro-pse.git
```


## Part 3: Installing the IDAES Flowsheet Processor (Graphical User Interface)

Users can interact with WaterTAP through two interfaces. The primary method is through our code-based interface, which is built on top of Pyomo and IDAES and utilizes the full capabilities of WaterTAP, but there can be a steep learning curve. Alternatively, users can access our graphical user interface (GUI), which requires pre-built WaterTAP flowsheets and has less flexibility, but is much easier to use. This GUI is still in the early stages of its development and currently has the following capabilities:

1.  Simulation and/or optimization of flowsheets built in WaterTAP
2.  Sensitivity analysis for user-defined and ranges
3.  Scenario analysis to compare results across various operating conditions
4.  Basic visualization of simulation outputs.

To access the IDAES Flowsheet Processor, visit the [documentation page](https://prommis.github.io/idaes-flowsheet-processor-ui/docs/Download/watertap) for a one-click native install. Note that there are separate applications for WaterTAP, IDAES, and PrOMMiS flowsheets.

![GUI Install](https://github.com/user-attachments/assets/f9a83036-a767-4a56-a440-1bd1869ab55d)

## Part 4: Optional Steps

### 18. Create a GitHub account

You can create a GitHub account if you want to interact with issues, pull requests, and discussion boards. Visit the [GitHub Getting Started](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github#signing-up-for-a-new-personal-account) page for instructions on how to create an account.

